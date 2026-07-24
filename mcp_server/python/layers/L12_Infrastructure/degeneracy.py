"""
SeshaAOS - Degeneracy Module
Version: 1.0.0
Description: Redundant subsystems, hot standbys, dual-write, peer health checks.
Biological degeneracy: multiple components can perform the same function.
"""
import copy
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent


class HotStandby:
    """In-memory hot standby that mirrors primary state."""
    
    def __init__(self, name: str, state_getter: Callable, state_setter: Callable):
        self.name = name
        self.state_getter = state_getter
        self.state_setter = state_setter
        self.backup_state = None
        self.last_sync = 0
        self.active = False
    
    def sync(self):
        """Pull current state from primary."""
        try:
            self.backup_state = copy.deepcopy(self.state_getter())
            self.last_sync = time.time()
            return True
        except Exception as e:
            print(f"[{self.name}] sync failed: {e}")
            return False
    
    def activate(self):
        """Activate this standby (promote to primary)."""
        if self.backup_state is not None:
            self.state_setter(self.backup_state)
            self.active = True
            return True
        return False
    
    def get_status(self) -> Dict:
        return {
            "name": self.name,
            "active": self.active,
            "has_backup": self.backup_state is not None,
            "last_sync": self.last_sync,
            "age_seconds": time.time() - self.last_sync if self.last_sync else None
        }


class DualWriter:
    """Writes to two destinations simultaneously for data safety."""
    
    def __init__(self, primary_writer: Callable, secondary_writer: Callable, name: str = "dual_writer"):
        self.primary_writer = primary_writer
        self.secondary_writer = secondary_writer
        self.name = name
        self.write_count = 0
        self.failover_count = 0
        self.secondary_available = True
        self.secondary_failures = 0
        
    def write(self, data: Any) -> Dict:
        """Write to both destinations. Falls back to primary only if secondary fails."""
        self.write_count += 1
        results = {"primary": None, "secondary": None, "used_fallback": False}
        
        # Primary write (always)
        try:
            results["primary"] = self.primary_writer(data)
        except Exception as e:
            results["primary"] = {"error": str(e)}
        
        # Secondary write (best effort)
        if self.secondary_available:
            try:
                results["secondary"] = self.secondary_writer(data)
            except Exception as e:
                self.secondary_failures += 1
                if self.secondary_failures >= 3:
                    self.secondary_available = False
                results["secondary"] = {"error": str(e)}
                results["used_fallback"] = True
        
        return results
    
    def get_status(self) -> Dict:
        return {
            "name": self.name,
            "write_count": self.write_count,
            "secondary_available": self.secondary_available,
            "secondary_failures": self.secondary_failures,
            "failover_count": self.failover_count
        }


class PeerHealthChecker:
    """Monitors health of peer/component processes."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.peers: Dict[str, Dict] = {}
        self.health_dir = base_dir / "core" / "monitoring" / "peer_health"
        self.health_dir.mkdir(parents=True, exist_ok=True)
    
    def register_peer(self, peer_id: str, health_check: Callable, metadata: Dict = None):
        """Register a peer with a health check function."""
        self.peers[peer_id] = {
            "health_check": health_check,
            "metadata": metadata or {},
            "last_check": 0,
            "status": "unknown",
            "consecutive_failures": 0
        }
    
    def check_peer(self, peer_id: str) -> Dict:
        """Check health of a specific peer."""
        if peer_id not in self.peers:
            return {"error": "Peer not found"}
        
        peer = self.peers[peer_id]
        try:
            result = peer["health_check"]()
            peer["status"] = "healthy"
            peer["consecutive_failures"] = 0
            peer["last_check"] = time.time()
            return {"peer_id": peer_id, "status": "healthy", "details": result}
        except Exception as e:
            peer["consecutive_failures"] += 1
            peer["status"] = "unhealthy"
            peer["last_check"] = time.time()
            return {
                "peer_id": peer_id,
                "status": "unhealthy",
                "error": str(e),
                "consecutive_failures": peer["consecutive_failures"]
            }
    
    def check_all_peers(self) -> Dict[str, Dict]:
        """Check health of all registered peers."""
        results = {}
        for peer_id in self.peers:
            results[peer_id] = self.check_peer(peer_id)
        return results
    
    def get_unhealthy_peers(self) -> List[str]:
        """Get list of unhealthy peer IDs."""
        return [pid for pid, p in self.peers.items() 
                if p["status"] == "unhealthy" and p["consecutive_failures"] >= 3]
    
    def get_status(self) -> Dict:
        healthy = sum(1 for p in self.peers.values() if p["status"] == "healthy")
        total = len(self.peers)
        return {
            "total_peers": total,
            "healthy": healthy,
            "unhealthy": total - healthy,
            "peers": {pid: {"status": p["status"], "consecutive_failures": p["consecutive_failures"]} 
                      for pid, p in self.peers.items()}
        }


class DegeneracyManager:
    """Central manager for all degeneracy mechanisms."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.standbys: Dict[str, HotStandby] = {}
        self.dual_writers: Dict[str, DualWriter] = {}
        self.peer_checker = PeerHealthChecker(base_dir)
        self.deg_dir = base_dir / "core" / "monitoring" / "degeneracy"
        self.deg_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.deg_dir / "degeneracy_state.json"
    
    def register_standby(self, name: str, state_getter: Callable, state_setter: Callable):
        """Register a component for hot standby."""
        self.standbys[name] = HotStandby(name, state_getter, state_setter)
        # Initial sync
        self.standbys[name].sync()
    
    def register_dual_writer(self, name: str, primary: Callable, secondary: Callable):
        """Register a dual-write pair."""
        self.dual_writers[name] = DualWriter(primary, secondary, name)
    
    def sync_all_standbys(self):
        """Sync all standbys from their primaries."""
        for standby in self.standbys.values():
            standby.sync()
    
    def activate_standby(self, name: str) -> Dict:
        """Activate a specific standby."""
        if name not in self.standbys:
            return {"success": False, "error": f"Standby {name} not found"}
        success = self.standbys[name].activate()
        return {"success": success, "standby": name, "active": self.standbys[name].active}
    
    def write(self, dual_writer_name: str, data: Any) -> Dict:
        """Write using a dual writer."""
        if dual_writer_name not in self.dual_writers:
            return {"error": f"Dual writer {dual_writer_name} not found"}
        return self.dual_writers[dual_writer_name].write(data)
    
    def check_peer_health(self, peer_id: str) -> Dict:
        """Check health of a peer."""
        return self.peer_checker.check_peer(peer_id)
    
    def check_all_health(self) -> Dict:
        """Check health of all peers and standbys."""
        peer_status = self.peer_checker.check_all_peers()
        standby_status = {name: s.get_status() for name, s in self.standbys.items()}
        dw_status = {name: d.get_status() for name, d in self.dual_writers.items()}
        
        return {
            "timestamp": time.time(),
            "peers": peer_status,
            "standbys": standby_status,
            "dual_writers": dw_status,
            "summary": {
                "total_peers": len(self.peer_checker.peers),
                "healthy_peers": sum(1 for p in peer_status.values() if p.get("status") == "healthy"),
                "active_standbys": sum(1 for s in standby_status.values() if s.get("active"))
            }
        }
    
    def save_state(self):
        """Save degeneracy state to disk."""
        state = {
            "timestamp": time.time(),
            "standby_count": len(self.standbys),
            "dual_writer_count": len(self.dual_writers),
            "peer_count": len(self.peer_checker.peers),
            "standby_names": list(self.standbys.keys()),
            "dual_writer_names": list(self.dual_writers.keys()),
            "peer_ids": list(self.peer_checker.peers.keys())
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)
    
    def get_status(self) -> Dict:
        return {
            "standbys": len(self.standbys),
            "dual_writers": len(self.dual_writers),
            "peers": len(self.peer_checker.peers),
            "standby_names": list(self.standbys.keys()),
            "dual_writer_names": list(self.dual_writers.keys())
        }


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    
    def get_test_state():
        return {"energy": 100, "cortisol": 10}
    
    def set_test_state(state):
        pass
    
    deg = DegeneracyManager(base)
    deg.register_standby("test_standby", get_test_state, set_test_state)
    deg.sync_all_standbys()
    print(json.dumps(deg.check_all_health(), indent=2))
