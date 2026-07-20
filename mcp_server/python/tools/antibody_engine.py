"""
AOS Antibody Engine — adaptive correction (antibodies, WBC patrol, fever response).
Version: 1.0.0
Description: Detects anomalies, generates corrective antibodies, and neutralizes threats.
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

_tools_parent = Path(__file__).resolve().parent.parent
if str(_tools_parent) not in sys.path:
    sys.path.insert(0, str(_tools_parent))

from tools.physiology_engine import PhysiologyEngine
from tools.auto_repair import AutoRepairEngine
from tools.signal_router import SignalRouter


# Antibody templates — pattern -> corrective action
ANTIBODY_CATALOG = {
    "corrupted_json": {"action": "restore_json", "severity": 2.0},
    "missing_pulse": {"action": "alert_supervisor", "severity": 3.0},
    "unauthorized_edit": {"action": "repair_and_quarantine", "severity": 1.5},
    "toxic_load": {"action": "filtrate", "severity": 1.0},
    "logic_drift": {"action": "reforge_dna", "severity": 2.5},
    "orphan_synapse": {"action": "prune_lattice", "severity": 0.5},
}


class AntibodyEngine:
    """Immune correction layer — antibodies neutralize specific threat patterns."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_path = base_dir / "core" / "monitoring" / "immune_cells.json"
        self.physiology = PhysiologyEngine(base_dir)
        self.repair = AutoRepairEngine(base_dir)
        self.signals = SignalRouter(base_dir)
        self._ensure_state()

    def _ensure_state(self):
        if not self.state_path.parent.exists():
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_path.exists():
            self._write_state({
                "wbc_count": 0,
                "rbc_health": 100.0,
                "platelet_clotting": 0,
                "antibodies": [],
                "memory_cells": [],
                "last_patrol": 0,
            })

    def _read_state(self) -> Dict[str, Any]:
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            self._ensure_state()
            return self._read_state()

    def _write_state(self, state: Dict[str, Any]):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

    def _generate_antibody(self, threat_type: str) -> Optional[Dict[str, Any]]:
        template = ANTIBODY_CATALOG.get(threat_type)
        if not template:
            return None
        return {
            "id": f"AB-{int(time.time())}",
            "target": threat_type,
            "action": template["action"],
            "severity": template["severity"],
            "created_at": time.time(),
            "neutralized": False,
        }

    def _execute_antibody(self, antibody: Dict[str, Any]) -> str:
        action = antibody["action"]
        if action == "restore_json":
            for path in self.base_dir.rglob("*.json"):
                if "monitoring" in str(path):
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            json.load(f)
                    except json.JSONDecodeError:
                        backup = path.with_suffix(".json.bak")
                        if backup.exists():
                            backup.replace(path)
                            return f"Restored {path.name} from backup."
            return "No corrupted JSON found."

        if action == "repair_and_quarantine":
            report = self.repair.scan_and_fix()
            self.physiology.register_anomaly("antibody_repair", antibody["severity"])
            return report

        if action == "filtrate":
            from tools.nexus_liver import NexusLiver
            return NexusLiver(self.base_dir).filter_toxins()

        if action == "reforge_dna":
            import subprocess
            for script in ["nlg_compiler.py", "nxp_forge.py"]:
                p = self.base_dir / "mcp_server" / "python" / script
                if p.exists():
                    subprocess.run([sys.executable, str(p)], capture_output=True)
            return "DNA reforge triggered by antibody."

        if action == "prune_lattice":
            from tools.nexus_lattice import LatticeEngine
            lattice_path = self.base_dir / "core" / "monitoring" / "lattice_state.json"
            if lattice_path.exists():
                with open(lattice_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                active = state.get("active_tasks", {})
                now = time.time()
                stale = [k for k, v in active.items() if now - v.get("started_at", now) > 3600]
                for k in stale:
                    del active[k]
                state["active_tasks"] = active
                with open(lattice_path, "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=4)
                return f"Pruned {len(stale)} stale synapse(s)."
            return "Lattice not found."

        if action == "alert_supervisor":
            self.signals.emit_signal("INFLAMMATION", {"event": "Service failure detected"}, ttl_seconds=600)
            return "Supervisor alert emitted."

        return f"Unknown antibody action: {action}"

    def patrol(self) -> List[str]:
        """WBC patrol — scan for threats and deploy antibodies."""
        state = self._read_state()
        results = []
        threats = []

        # Scan JSON integrity
        for path in (self.base_dir / "core" / "monitoring").glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError:
                threats.append("corrupted_json")

        # Check toxic load
        from tools.nexus_liver import NexusLiver
        toxic = NexusLiver(self.base_dir).get_toxic_load()
        if toxic.get("toxicity_pct", 0) > 60:
            threats.append("toxic_load")

        # Check stale synapses
        lattice_path = self.base_dir / "core" / "monitoring" / "lattice_state.json"
        if lattice_path.exists():
            with open(lattice_path, "r", encoding="utf-8") as f:
                ls = json.load(f)
            now = time.time()
            stale = [v for v in ls.get("active_tasks", {}).values() if now - v.get("started_at", now) > 3600]
            if stale:
                threats.append("orphan_synapse")

        # Check service heartbeats
        from tools.service_heartbeat import ServiceHeartbeat
        for svc in ServiceHeartbeat.all_services(self.base_dir):
            if svc.get("stale"):
                threats.append("missing_pulse")

        # Deploy antibodies
        antibodies = state.get("antibodies", [])
        memory = state.get("memory_cells", [])

        for threat in set(threats):
            if threat in memory:
                results.append(f"[MEMORY CELL] {threat} — fast neutralization.")
            ab = self._generate_antibody(threat)
            if ab:
                outcome = self._execute_antibody(ab)
                ab["neutralized"] = True
                ab["outcome"] = outcome[:200]
                antibodies.append(ab)
                if threat not in memory:
                    memory.append(threat)
                results.append(f"[ANTIBODY {ab['id']}] {threat}: {outcome[:100]}")

        state["wbc_count"] = state.get("wbc_count", 0) + len(threats)
        state["antibodies"] = antibodies[-50:]
        state["memory_cells"] = memory[-30:]
        state["last_patrol"] = time.time()
        state["rbc_health"] = max(0, 100 - toxic.get("toxicity_pct", 0))
        state["platelet_clotting"] = len(threats)
        self._write_state(state)

        if threats:
            physio = self.physiology.get_state()
            if physio["immune"]["threat_level"] in ("Fever", "Sepsis"):
                self.signals.emit_signal("NOCICEPTION", {"event": f"Patrol found {len(threats)} threat(s)"}, ttl_seconds=120)

        return results or ["Patrol clear — no threats detected."]

    def get_immune_cells_status(self) -> Dict[str, Any]:
        state = self._read_state()
        physio = self.physiology.get_state()
        return {
            "wbc_count": state.get("wbc_count", 0),
            "rbc_health_pct": state.get("rbc_health", 100),
            "platelet_clotting": state.get("platelet_clotting", 0),
            "active_antibodies": len([a for a in state.get("antibodies", []) if not a.get("neutralized")]),
            "memory_cells": state.get("memory_cells", []),
            "body_temperature": physio["immune"]["temperature"],
            "threat_level": physio["immune"]["threat_level"],
            "last_patrol": state.get("last_patrol", 0),
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = AntibodyEngine(base)
    print(engine.patrol())
    print(json.dumps(engine.get_immune_cells_status(), indent=2))
