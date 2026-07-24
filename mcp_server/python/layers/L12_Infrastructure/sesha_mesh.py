"""
SeshaAOS - Synaptic Mesh Engine
Version: 1.0.0
Description: Manages inter-node communication and discovery (Gossip Simulation).
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

class SeshaMesh:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        # Simulation: nodes are subdirectories in a 'mesh' folder
        self.mesh_dir = base_dir / "core" / "monitoring" / "mesh"
        self.node_id = self._get_node_id()
        self.mesh_dir.mkdir(parents=True, exist_ok=True)
        self.heartbeat_path = self.mesh_dir / f"node_{self.node_id}.json"

    def _get_node_id(self) -> str:
        # In a real system, this might be a UUID or IP.
        # For simulation, we use the process ID or a unique name.
        return f"local_{os.getpid()}"

    def broadcast_heartbeat(self, status: str, energy: float):
        """Announces this node to the mesh."""
        data = {
            "node_id": self.node_id,
            "status": status,
            "energy": energy,
            "last_seen": time.time(),
            "roles": self._get_local_roles()
        }
        with open(self.heartbeat_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def discover_peers(self) -> List[Dict]:
        """Finds other nodes in the mesh."""
        peers = []
        for p in self.mesh_dir.glob("node_*.json"):
            if p.name == self.heartbeat_path.name:
                continue
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Simple TTL: remove if no heartbeat for 5 mins
                    if time.time() - data["last_seen"] < 300:
                        peers.append(data)
                    else:
                        p.unlink() # Cleanup orphaned node
            except Exception:
                continue
        return peers

    def send_synapse(self, target_node_id: str, synapse_data: Dict) -> bool:
        """Relays a synapse to a remote node's inbox."""
        inbox = self.mesh_dir / f"inbox_{target_node_id}.json"
        try:
            # For simulation, we append to a list in the target's inbox
            current = []
            if inbox.exists():
                current = json.loads(inbox.read_text(encoding="utf-8"))
            current.append({**synapse_data, "sender": self.node_id, "timestamp": time.time()})
            inbox.write_text(json.dumps(current, indent=4), encoding="utf-8")
            return True
        except Exception:
            return False

    def _get_local_roles(self) -> List[str]:
        """Queries the active_roles directory for available roles."""
        roles_dir = self.base_dir / "active_roles"
        if roles_dir.exists():
             return [d.name for d in roles_dir.iterdir() if d.is_dir()]
        return ["Orchestrator", "Research", "Motor", "Immune"]

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    mesh = SeshaMesh(base)
    mesh.broadcast_heartbeat("Healthy", 99.0)
    print(f"Node {mesh.node_id} online.")
    print("Peers:", mesh.discover_peers())

