"""
Nexus Corporate OS - Orchestrator Engine (The CPU)
Version: 1.0.0
Description: Autonomous closed-loop: senses -> decision -> lattice -> motor -> memory.
"""

import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

_tools_parent = Path(__file__).resolve().parent.parent
if str(_tools_parent) not in sys.path:
    sys.path.insert(0, str(_tools_parent))

from typing import Dict, Any, List, Optional

from tools.physiology_engine import PhysiologyEngine
from tools.physiological_gate import PhysiologicalGate
from tools.signal_router import SignalRouter
from tools.nexus_senses import NexusSenses
from tools.nexus_lattice import LatticeEngine
from tools.motor_engine import MotorEngine
from tools.memory_synth import MemorySynth
from tools.nexus_liver import NexusLiver
from tools.auto_repair import AutoRepairEngine


DEFAULT_ROUTING = {
    "NOCICEPTION": {"to": "Systems Security", "priority": 10, "action": "heal"},
    "ADRENALINE": {"to": "NCC", "priority": 9, "action": "motor_priority"},
    "GENETIC_PLASTICITY": {"to": "CKO", "priority": 7, "action": "reforge"},
    "GROWTH": {"to": "Research Lead", "priority": 5, "action": "intel"},
    "INFLAMMATION": {"to": "Systems Security", "priority": 8, "action": "heal"},
    "REPRODUCTION_READY": {"to": "COO", "priority": 4, "action": "spore_check"},
    "VIBE": {"to": "NCC", "priority": 2, "action": "observe"},
}


class OrchestratorEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_path = base_dir / "core" / "monitoring" / "orchestrator_state.json"
        self.inbox_path = base_dir / "core" / "monitoring" / "directive_inbox.json"
        self.routing_path = base_dir / "core" / "monitoring" / "routing_weights.json"
        self.log_path = base_dir / "core" / "monitoring" / "orchestrator_log.json"

        self.physiology = PhysiologyEngine(base_dir)
        self.gate = PhysiologicalGate(base_dir)
        self.signals = SignalRouter(base_dir)
        self.senses = NexusSenses(base_dir)
        self.lattice = LatticeEngine(base_dir)
        self.motor = MotorEngine(base_dir)
        self.memory = MemorySynth(base_dir)
        self.liver = NexusLiver(base_dir)
        self.repair = AutoRepairEngine(base_dir)
        self._ensure_state()

    def _ensure_state(self):
        for path, default in [
            (self.state_path, {
                "status": "idle",
                "tick_count": 0,
                "last_tick": 0,
                "last_processed_sensory_ts": 0,
                "recent_decisions": [],
            }),
            (self.inbox_path, {"directives": []}),
            (self.routing_path, {"routes": DEFAULT_ROUTING, "success_counts": {}, "failure_counts": {}}),
            (self.log_path, []),
        ]:
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(default, f, indent=4)

    def _read_json(self, path: Path, default: Any) -> Any:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default

    def _write_json(self, path: Path, data: Any):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def submit_directive(self, text: str, priority: int = 5) -> str:
        inbox = self._read_json(self.inbox_path, {"directives": []})
        directive_id = str(uuid.uuid4())[:8]
        inbox["directives"].append({
            "id": directive_id,
            "text": text,
            "priority": priority,
            "status": "pending",
            "submitted_at": time.time(),
        })
        self._write_json(self.inbox_path, inbox)
        self.signals.emit_signal("ADRENALINE", {"event": f"Sovereign directive: {text[:80]}"}, ttl_seconds=300)
        return f"Directive [{directive_id}] queued: {text[:100]}"

    def _log_decision(self, decision: str, outcome: str, success: bool):
        log = self._read_json(self.log_path, [])
        log.append({
            "timestamp": time.time(),
            "decision": decision,
            "outcome": outcome[:300],
            "success": success,
        })
        if len(log) > 200:
            log = log[-200:]
        self._write_json(self.log_path, log)

        state = self._read_json(self.state_path, {})
        recent = state.get("recent_decisions", [])
        recent.append({"decision": decision, "success": success, "at": time.time()})
        state["recent_decisions"] = recent[-20:]
        self._write_json(self.state_path, state)

    def _bump_routing_weight(self, signal_type: str, success: bool):
        routing = self._read_json(self.routing_path, {"routes": DEFAULT_ROUTING, "success_counts": {}, "failure_counts": {}})
        key = "success_counts" if success else "failure_counts"
        counts = routing.get(key, {})
        counts[signal_type] = counts.get(signal_type, 0) + 1
        routing[key] = counts
        self._write_json(self.routing_path, routing)

    def _execute_action(self, action: str, context: Dict[str, Any]) -> str:
        if action == "heal":
            allowed, msg = self.gate.check("trigger_self_healing")
            if not allowed:
                return f"HEAL SKIPPED: {msg}"
            result = self.repair.scan_and_fix()
            self.physiology.consume_energy(100)
            return result

        if action == "reforge":
            compiler = self.base_dir / "mcp_server" / "python" / "nlg_compiler.py"
            forge = self.base_dir / "mcp_server" / "python" / "nxp_forge.py"
            for script in [compiler, forge]:
                if script.exists():
                    subprocess.run([sys.executable, str(script)], capture_output=True)
            self.physiology.consume_energy(150)
            return "DNA reforge complete (compiler + forge)."

        if action == "intel":
            allowed, msg = self.gate.check("collect_intelligence")
            if not allowed:
                return f"INTEL SKIPPED: {msg}"
            scraper = self.base_dir / "mcp_server" / "python" / "oracle_scraper.py"
            if scraper.exists():
                subprocess.run([sys.executable, str(scraper)], capture_output=True)
                self.physiology.consume_energy(500)
                return "Intelligence collection triggered."
            return "Oracle scraper not found."

        if action == "motor_priority":
            results = self.motor.process_lattice_queue()
            return f"Motor priority: {len(results)} action(s)." if results else "Motor queue empty."

        if action == "filtrate":
            return self.liver.filter_toxins()

        if action == "consolidate":
            return self.memory.consolidate()

        if action == "spore_check":
            allowed, msg = self.gate.check("generate_spore_export")
            if not allowed:
                return f"SPORE SKIPPED: {msg}"
            return "Replication conditions noted. Awaiting sovereign approval for spore export."

        if action == "observe":
            return "Vibe signal observed. No action required."

        if action == "diagnose":
            from tools.system_diagnostics import run_diagnostics
            return run_diagnostics(self.base_dir)

        return f"Unknown action: {action}"

    def _route_signal(self, signal_type: str, payload: Dict[str, Any]) -> Optional[str]:
        routing = self._read_json(self.routing_path, {"routes": DEFAULT_ROUTING})
        route = routing.get("routes", {}).get(signal_type)
        if not route:
            return None

        priority = route.get("priority", 5)
        state = self.physiology.get_state()
        if state["metabolism"]["status"] == "Conserving" and priority < 8:
            return None

        allowed, msg = self.gate.check("dispatch_task")
        if not allowed:
            self._log_decision(f"route:{signal_type}", msg, False)
            return msg

        to_role = route["to"]
        action = route["action"]
        event = payload.get("event", signal_type)

        synapse = self.lattice.fire_synapse("Nexus Orchestrator", to_role, f"AUTO:{action}:{event}")
        outcome = self._execute_action(action, payload)
        success = "SKIPPED" not in outcome and "ERROR" not in outcome.upper()
        self._bump_routing_weight(signal_type, success)
        self._log_decision(f"signal:{signal_type}->{to_role}", outcome, success)
        return f"{synapse} | {outcome}"

    def _process_sensory_events(self) -> List[str]:
        state = self._read_json(self.state_path, {})
        last_ts = state.get("last_processed_sensory_ts", 0)
        results = []
        max_ts = last_ts

        for event in self.senses.get_feed(50):
            if event.get("timestamp", 0) <= last_ts:
                continue
            max_ts = max(max_ts, event.get("timestamp", 0))
            signal = event.get("signal_emitted")
            if signal:
                routed = self._route_signal(signal, {"event": event.get("path", ""), "salience": event.get("salience")})
                if routed:
                    results.append(routed)

        state["last_processed_sensory_ts"] = max_ts
        self._write_json(self.state_path, state)
        return results

    def _process_active_signals(self) -> List[str]:
        results = []
        for signal_type, data in self.signals.get_active_signals().items():
            if signal_type in ("VIBE",):
                continue
            routed = self._route_signal(signal_type, data.get("payload", {}))
            if routed:
                results.append(routed)
        return results

    def _parse_directive(self, text: str) -> str:
        lower = text.lower().strip()
        if any(k in lower for k in ("heal", "repair", "fix")):
            return "heal"
        if any(k in lower for k in ("intel", "scrape", "news", "oracle")):
            return "intel"
        if any(k in lower for k in ("diagnose", "diagnostic", "status")):
            return "diagnose"
        if any(k in lower for k in ("clean", "filtrate", "liver", "toxic")):
            return "filtrate"
        if any(k in lower for k in ("dream", "consolidate", "memory")):
            return "consolidate"
        if any(k in lower for k in ("motor", "execute", "run")):
            return "motor_priority"
        if lower.startswith("motor:"):
            return "motor_direct"
        return "observe"

    def _process_directive_inbox(self) -> List[str]:
        inbox = self._read_json(self.inbox_path, {"directives": []})
        pending = [d for d in inbox["directives"] if d.get("status") == "pending"]
        pending.sort(key=lambda d: -d.get("priority", 5))

        results = []
        for directive in pending[:3]:
            action = self._parse_directive(directive["text"])
            text = directive["text"]

            if action == "motor_direct":
                self.lattice.fire_synapse("Nexus Orchestrator", "Motor", text)
                outcome = "\n".join(self.motor.process_lattice_queue()) or "Motor directive queued."
            else:
                self.lattice.fire_synapse("Nexus Orchestrator", "Sovereign Proxy", f"DIRECTIVE:{text[:120]}")
                outcome = self._execute_action(action, {"directive": text})

            directive["status"] = "completed"
            directive["completed_at"] = time.time()
            directive["outcome"] = outcome[:300]
            success = "SKIPPED" not in outcome and "ERROR" not in outcome.upper()
            self._log_decision(f"directive:{directive['id']}", outcome, success)
            results.append(f"[{directive['id']}] {outcome}")

        self._write_json(self.inbox_path, inbox)
        return results

    def _autonomic_maintenance(self) -> List[str]:
        results = []
        state = self.physiology.get_state()
        orch_state = self._read_json(self.state_path, {})

        toxic = self.liver.get_toxic_load()
        if toxic.get("toxicity_pct", 0) > 75:
            r = self._execute_action("filtrate", {})
            results.append(f"Auto-filtration: {r}")

        if state["immune"]["threat_level"] in ("Fever", "Sepsis"):
            r = self._execute_action("heal", {})
            results.append(f"Fever response: {r}")

        lattice_state = self.lattice._read_state()
        if len(lattice_state.get("history", [])) >= 30:
            allowed, _ = self.gate.check("trigger_memory_consolidation")
            if allowed:
                r = self._execute_action("consolidate", {})
                results.append(f"Auto-dream: {r}")

        motor_pending = self.motor.get_status().get("pending_motor_tasks", 0)
        if motor_pending > 0:
            r = self._execute_action("motor_priority", {})
            results.append(f"Motor drain: {r}")

        # WBC patrol (antibody engine)
        if orch_state.get("tick_count", 0) % 10 == 0:
            try:
                from tools.antibody_engine import AntibodyEngine
                patrol = AntibodyEngine(self.base_dir).patrol()
                if patrol and patrol[0] != "Patrol clear — no threats detected.":
                    results.append(f"WBC patrol: {patrol[0][:80]}")
            except Exception:
                pass

        return results

    def tick(self) -> Dict[str, Any]:
        """Single orchestrator cycle — the closed perception-action loop."""
        state = self._read_json(self.state_path, {})
        physio = self.physiology.get_state()

        if physio["metabolism"]["status"] == "Critical":
            state["status"] = "suspended_critical"
            state["last_tick"] = time.time()
            self._write_json(self.state_path, state)
            return {"status": "suspended", "reason": "Energy critical"}

        state["status"] = "running"
        state["tick_count"] = state.get("tick_count", 0) + 1
        state["last_tick"] = time.time()

        results = {
            "tick": state["tick_count"],
            "sensory": self._process_sensory_events(),
            "signals": self._process_active_signals(),
            "directives": self._process_directive_inbox(),
            "maintenance": self._autonomic_maintenance(),
        }

        self.physiology.synthesize_vibe()
        self.physiology.consume_energy(15)
        self._write_json(self.state_path, state)
        return results

    def get_status(self) -> Dict[str, Any]:
        state = self._read_json(self.state_path, {})
        inbox = self._read_json(self.inbox_path, {"directives": []})
        pending = len([d for d in inbox.get("directives", []) if d.get("status") == "pending"])
        routing = self._read_json(self.routing_path, {})
        return {
            "status": state.get("status", "idle"),
            "tick_count": state.get("tick_count", 0),
            "last_tick": state.get("last_tick", 0),
            "pending_directives": pending,
            "recent_decisions": state.get("recent_decisions", []),
            "routing_success": routing.get("success_counts", {}),
            "routing_failure": routing.get("failure_counts", {}),
            "active_lattice_nodes": len(self.lattice.get_active_nodes()),
            "motor_pending": self.motor.get_status().get("pending_motor_tasks", 0),
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    orch = OrchestratorEngine(base)
    print(json.dumps(orch.tick(), indent=2))
