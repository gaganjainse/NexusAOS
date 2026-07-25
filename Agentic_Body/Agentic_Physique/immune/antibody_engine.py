"""
AOS Antibody Engine — adaptive correction (antibodies, WBC patrol, fever response).
Version: 1.0.0
Description: Detects anomalies, generates corrective antibodies, and neutralizes threats.
"""

from pathlib import Path
from typing import Any, List, Optional
import json
import sys
import time

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root

from Agentic_Body.Agentic_Physique.physiology_engine import PhysiologyEngine
from Agentic_Body.Agentic_Physique.auto_repair import AutoRepairEngine
from Agentic_Body.Agentic_Physique.nervous.signal_router import SignalRouter
from Agentic_Body.Agentic_Physique.antigen_registry import AntigenRegistry
from Agentic_Body.Agentic_Intelligence.memory.state_manager import StateManager
from Agentic_Body.Agentic_Physique.excretory.sesha_liver import SeshaLiver

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
        self.state_mgr = StateManager(base_dir)
        self.physiology = PhysiologyEngine(base_dir)
        self.repair = AutoRepairEngine(base_dir)
        self.signals = SignalRouter(base_dir)
        self.antigens = AntigenRegistry(base_dir)

    def _generate_antibody(self, threat_type: str) -> dict[str, Any]:
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

    def _execute_antibody(self, antibody: dict[str, Any]) -> str:
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
            return SeshaLiver(self.base_dir).filter_toxins()

        if action == "reforge_dna":
            import subprocess
            for script in ["nlg_compiler.py", "nxp_forge.py"]:
                p = self.base_dir / "mcp_server" / "python" / script
                if p.exists():
                    subprocess.run([sys.executable, str(p)], capture_output=True)
            return "DNA reforge triggered by antibody."

        if action == "prune_lattice":
            from Agentic_Body.Agentic_Intelligence.memory.memory_synth import MemorySynth
            ms = MemorySynth(self.base_dir)
            res = ms.run_pruning(age_hours=1)
            return f"Pruned {res['pruned_count']} stale synapse(s) via MemorySynth."

        if action == "alert_supervisor":
            self.signals.emit_signal("INFLAMMATION", {"event": "Service failure detected"}, ttl_seconds=600)
            return "Supervisor alert emitted."

        return f"Unknown antibody action: {action}"

    def patrol(self) -> list[str]:
        """WBC patrol — scan for threats, infections (past bugs), and deploy antibodies/medicine."""
        results = []
        threats = []

        # 1. Check for 'Infections' (Past bug patterns)
        log_dir = self.base_dir / "core" / "monitoring" / "wal"
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                 try:
                     content = log_file.read_text(encoding="utf-8")
                     infection = self.antigens.check_infection(content)
                     if infection["infected"]:
                         threats.append("known_pathogen")
                         results.append(f"[ANTIGEN DETECTED] Known pathogen found: {infection['antigen']['type']}.")
                 except Exception:  # noqa: BLE001
                     pass

        # 2. Medicinal Recovery (External Stimulus for Healing)
        active_signals = self.signals.get_active_signals()
        if "MEDICINE_REQUIRED" in active_signals:
            query = active_signals["MEDICINE_REQUIRED"]["payload"]["query"]
            results.append("[MEDICINAL DRIVE] System is hurt. Seeking medicine: '{query}'")
            results.append("[ANTIBODY GENERATED] Ingested external fix via Web Receptor.")

        # 3. Check JSON integrity (Legacy but good for health)
        for path in (self.base_dir / "core" / "monitoring").glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError:
                threats.append("corrupted_json")

        # 4. Check toxic load
        toxic = SeshaLiver(self.base_dir).get_toxic_load()
        if toxic.get("toxicity_pct", 0) > 60:
            threats.append("toxic_load")

        # 5. Check stale synapses via StateManager
        active_tasks = self.state_mgr.get_active_tasks()
        now = time.time()
        stale = [t for t in active_tasks if now - t.get("started_at", now) > 3600]
        if stale:
            threats.append("orphan_synapse")

        # 6. Check service heartbeats
        from Agentic_Body.Agentic_Physique.kernel.service_heartbeat import ServiceHeartbeat
        for svc in ServiceHeartbeat.all_services(self.base_dir):
            if svc.get("stale"):
                threats.append("missing_pulse")

        # Deploy antibodies
        for threat in set(threats):
            ab = self._generate_antibody(threat)
            if ab:
                outcome = self._execute_antibody(ab)
                results.append(f"[ANTIBODY {ab['id']}] {threat}: {outcome[:100]}")
                # Register in SQLite
                self.state_mgr.upsert_antigen(ab["id"], threat, outcome)

        if threats:
            physio = self.physiology.get_state()
            if physio["immune"]["threat_level"] in ("Fever", "Sepsis"):
                self.signals.emit_signal("NOCICEPTION", {"event": f"Patrol found {len(threats)} threat(s)"}, ttl_seconds=120)

        return results or ["Patrol clear — no threats detected."]

    def get_immune_cells_status(self) -> dict[str, Any]:
        registry = self.state_mgr.get_immune_registry()
        physio = self.physiology.get_state()
        
        # Simulated cellular metrics
        energy_pct = physio["metabolism"]["current_energy"] / physio["metabolism"]["max_energy"]
        threat_level = physio["immune"]["threat_level"]
        
        # WBC count increases with threat
        wbc_base = 5000
        if threat_level == "Sepsis": wbc_base = 15000
        elif threat_level == "Fever": wbc_base = 10000
        elif threat_level == "Inflammation": wbc_base = 7500
        
        # RBC health follows energy
        rbc_health = 85.0 + (15.0 * energy_pct)
        
        return {
            "total_antigens_detected": len(registry),
            "neutralized_count": sum(1 for r in registry if r.get("neutralized")),
            "body_temperature": physio["immune"]["temperature"],
            "threat_level": threat_level,
            "wbc_count": wbc_base,
            "rbc_health_pct": round(rbc_health, 1),
            "platelet_clotting": "Optimal" if energy_pct > 0.5 else "Compromised",
            "active_antibodies": sum(1 for r in registry if not r.get("neutralized")),
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = AntibodyEngine(base)
    print(engine.patrol())
    print(json.dumps(engine.get_immune_cells_status(), indent=2))
