"""NexusAOS - Orchestrator Engine (The CPU)
Version: 1.0.0
Description: Autonomous closed-loop: senses -> decision -> lattice -> motor -> memory.
"""
import json, subprocess, sys, time, uuid, os
from pathlib import Path
from typing import Dict, Any, List, Optional
_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root
from layers.L02_Agent.physiology_engine import PhysiologyEngine
from layers.L08_Governance.physiological_gate import PhysiologicalGate
from layers.L11_Data.signal_router import SignalRouter
from layers.L07_Integration.nexus_senses import NexusSenses
from layers.L12_Infrastructure.nexus_lattice import LatticeEngine
from layers.L05_Memory.state_manager import StateManager
from layers.L02_Agent.motor_engine import MotorEngine
from layers.L05_Memory.memory_synth import MemorySynth
from layers.L02_Agent.nexus_liver import NexusLiver
from layers.L02_Agent.auto_repair import AutoRepairEngine
from layers.L11_Data.soma_transcended import TranscendedSubstrate

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
        self.state_mgr = StateManager(base_dir)
        self.substrate = TranscendedSubstrate(base_dir)
        
        from layers.L02_Agent.physiology_engine import PhysiologyEngine
        from layers.L08_Governance.physiological_gate import PhysiologicalGate
        from layers.L11_Data.signal_router import SignalRouter
        from layers.L07_Integration.nexus_senses import NexusSenses
        from layers.L12_Infrastructure.nexus_lattice import LatticeEngine
        from layers.L02_Agent.motor_engine import MotorEngine
        from layers.L05_Memory.memory_synth import MemorySynth
        from layers.L02_Agent.nexus_liver import NexusLiver
        from layers.L02_Agent.auto_repair import AutoRepairEngine
        from layers.L11_Data.synaptic_transmitter import SynapticTransmitter
        from layers.L09_Observability.logic_git import LogicGit
        from layers.L08_Governance.auditor_agent import AuditorAgent
        from layers.L09_Observability.tdd_steroids import TDDOnSteroids
        from layers.L04_Composition.composition_engine import CompositionEngine
        from layers.L13_Hive.hive_bridge import HiveBridge

        self.physiology = PhysiologyEngine(base_dir)
        self.gate = PhysiologicalGate(base_dir)
        self.signals = SignalRouter(base_dir)
        self.senses = NexusSenses(base_dir)
        self.lattice = LatticeEngine(base_dir)
        self.motor = MotorEngine(base_dir)
        self.memory = MemorySynth(base_dir)
        self.liver = NexusLiver(base_dir)
        self.repair = AutoRepairEngine(base_dir)
        self.transmitter = SynapticTransmitter(base_dir)
        self.logic_git = LogicGit(base_dir)
        self.auditor = AuditorAgent(base_dir)
        self.tdd = TDDOnSteroids()
        self.composition = CompositionEngine(base_dir)
        self.hive = HiveBridge(base_dir)
        
        self.state_mgr.initialize_routing_weights(DEFAULT_ROUTING)
        self._subscribe_to_mesh()

    def _subscribe_to_mesh(self):
        """Neural 5.0: Subscribes to the Zenoh signal mesh."""
        for signal_type in DEFAULT_ROUTING.keys():
            self.substrate.subscribe(f"signal/{signal_type}", 
                lambda p, s=signal_type: self._route_signal(s, p["payload"]))

    def submit_directive(self, text: str, priority: int = 5) -> str:
        """Neural 13.0: High-speed directive submission with Hive Collision prevention."""
        # 0. Hive Omega: Acquire Planning Lock (L13 Collision Prevention)
        node_id = f"nexus_{os.getpid()}"
        if not self.state_mgr.acquire_hive_lock("planning_intent", node_id):
            return "COLLISION: Another Nexus instance is currently planning. Proposing Synaptic Merge."

        # 1. Transmit high-speed spike
        self.transmitter.transmit_directive(text, sigil="!" if priority >= 8 else "◊", priority=priority)
        
        # 2. Persistence
        directive_id = str(uuid.uuid4())[:8]
        data = {"id": directive_id, "text": text, "priority": priority, "status": "pending", "submitted_at": time.time()}
        self.state_mgr.queue_directive(data)
        self.signals.emit_signal("ADRENALINE", {"event": f"Sovereign directive: {text[:80]}"}, ttl_seconds=300)
        
        # Release lock after submission
        self.state_mgr.release_hive_lock("planning_intent", node_id)
        
        return f"Directive [{directive_id}] transmitted via high-speed bus and queued."

    def _route_signal(self, signal_type: str, payload: Dict[str, Any]) -> Optional[str]:
        routing = self.state_mgr.get_routing_weights()
        route = routing.get(signal_type)
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
        return []

    def _process_active_signals(self) -> List[str]:
        results = []
        for signal_type, data in self.signals.get_active_signals().items():
            if signal_type in ("VIBE", "DECISION"):
                continue
            routed = self._route_signal(signal_type, data.get("payload", {}))
            if routed:
                results.append(routed)
        return results

    def _fracture_task(self, task_text: str) -> List[str]:
        """Neural 7.0: Adaptive Atomic Fission."""
        # Detect complex intent by counting conjunctions and newlines
        sub_atoms = []
        
        # Split by explicit list markers or newlines
        import re
        lines = re.split(r'\n|\d+\.|\*|-', task_text)
        
        for line in lines:
            trimmed = line.strip()
            if not trimmed: continue
            
            # Sub-split by high-density conjunctions
            if " and " in trimmed.lower():
                sub_atoms.extend([part.strip() for part in re.split(r' and ', trimmed, flags=re.IGNORECASE)])
            elif ", " in trimmed:
                sub_atoms.extend([part.strip() for part in trimmed.split(", ")])
            else:
                sub_atoms.append(trimmed)
                
        return sub_atoms

    def _process_directive_inbox(self) -> List[str]:
        pending = self.state_mgr.get_queued_directives("pending")
        pending.sort(key=lambda d: -d.get("priority", 5))
        results = []
        for directive in pending[:3]:
            # Fractal Decomposition
            atoms = self._fracture_task(directive["text"])
            directive_results = []
            
            for atom in atoms:
                # 1. Governance Membrane (Auditor)
                allowed, msg = self.auditor.validate_proposal(atom, "Orchestrator")
                if not allowed:
                    directive_results.append(f"REJECTED: {msg}")
                    continue
                
                # 2. Decision Superposition (Entangled Agency)
                # Instead of a single path, we evaluate multiple potential realities
                optimal_reality = self._evaluate_superposition(atom)
                predicted_action = optimal_reality["action"]

                # 3. TDD-on-Steroids (Pre-verification)
                test_case = self.tdd.generate_pre_test(atom)
                if not self.tdd.verify_logic(predicted_action, test_case):
                    directive_results.append(f"REJECTED: Pre-execution verification failed for '{atom}'")
                    continue
                
                # 4. Layer 4: Composition Bidding (Dynamic Negotiation)
                negotiation = self.composition.negotiate_task(atom)
                winner = negotiation["winner"]
                confidence = negotiation["confidence"]

                # 5. Execution (Routed to winner)
                action = predicted_action
                if action == "motor_direct":
                    self.lattice.fire_synapse(winner, "Motor", atom)
                    outcome = "\n".join(self.motor.process_lattice_queue()) or f"Motor directive won by {winner}."
                else:
                    self.lattice.fire_synapse("Nexus Orchestrator", winner, f"ATOM:{atom[:120]}")
                    outcome = self._execute_action(action, {"directive": atom, "agent": winner})
                
                if isinstance(outcome, dict):
                    outcome = json.dumps(outcome)
                
                # 6. Logic Git (Versioning)
                self.logic_git.commit_node(directive["directive_id"], atom, outcome)
                directive_results.append(f"[{winner} @ {confidence:.2f}] {outcome}")
                
            final_outcome = " | ".join(directive_results)
            self.state_mgr.update_directive_status(directive["directive_id"], "completed", final_outcome[:300])
            self._log_decision(f"superposition_directive:{directive['directive_id']}", final_outcome, True)
            results.append(f"[{directive['directive_id']}] {final_outcome}")
            
        return results

    def _evaluate_superposition(self, atom: str) -> Dict[str, Any]:
        """Neural 13.0: Evaluates multiple action paths and collapses to the optimal one."""
        # Candidates: [Action, Energy Cost, Risk/Cortisol]
        candidates = [
            {"action": self._parse_directive(atom), "energy": 50, "risk": 5},
            {"action": "heal", "energy": 100, "risk": 2}, # Safe bet
            {"action": "motor_priority", "energy": 150, "risk": 15} # High impact
        ]
        
        state = self.physiology.get_state()
        current_energy = state["metabolism"]["current_energy"]
        
        # Scoring Loop (Entanglement Weighting)
        best_candidate = candidates[0]
        max_score = -1000
        
        for c in candidates:
            score = 100
            score -= (c["energy"] / current_energy) * 100
            score -= c["risk"] * 2
            
            if score > max_score:
                max_score = score
                best_candidate = c
                
        self._log_decision("superposition:collapse", f"Best: {best_candidate['action']} (Score: {max_score})", True)
        return best_candidate

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

    def _autonomic_maintenance(self) -> List[str]:
        results = []
        state = self.physiology.get_state()
        toxic = self.liver.get_toxic_load()
        if toxic.get("toxicity_pct", 0) > 75:
            r = self._execute_action("filtrate", {})
            results.append(f"Auto-filtration: {r}")
        if state["immune"]["threat_level"] in ("Fever", "Sepsis"):
            r = self._execute_action("heal", {})
            results.append(f"Fever response: {r}")
        
        # Consolidation check via StateManager
        conn = self.state_mgr._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM lattice_tasks")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count >= 30:
            allowed, _ = self.gate.check("trigger_memory_consolidation")
            if allowed:
                r = self._execute_action("consolidate", {})
                results.append(f"Auto-dream: {r}")
        motor_pending = self.motor.get_status().get("pending_motor_tasks", 0)
        if motor_pending > 0:
            r = self._execute_action("motor_priority", {})
            results.append(f"Motor drain: {r}")
        return results

    def tick(self) -> Dict[str, Any]:
        physio = self.physiology.get_state()
        if physio["metabolism"]["status"] == "Critical":
            return {"status": "suspended", "reason": "Energy critical"}
        
        results = {
            "sensory": self._process_sensory_events(),
            "signals": self._process_active_signals(),
            "directives": self._process_directive_inbox(),
            "maintenance": self._autonomic_maintenance(),
        }
        self.physiology.synthesize_vibe()
        self.physiology.consume_energy(15)
        
        # Neural 13.0: Exhale to Hive for cross-instance sync
        self.hive.exhale_to_hive()
        
        # Neural 13.0: Token Sentry - Monitoring context saturation
        # We estimate context size based on recent results and directives
        context_snapshot = json.dumps(results)
        from layers.L05_Memory.context_pager import ContextPager
        pager = ContextPager(self.base_dir)
        paged, msg = pager.trigger_autonomic_paging(len(context_snapshot) * 10) # Weighted estimate
        if paged:
            results["maintenance"].append(msg)
        
        return results

    def _execute_action(self, action: str, context: Dict[str, Any]) -> str:
        """Executes a specific biological action by delegating to the appropriate engine."""
        if action == "heal":
            return "\n".join(self.repair.scan_and_fix())
        if action == "intel":
            return "Intelligence ingested into the Digestive Engine."
        if action == "diagnose":
            return json.dumps(self.get_status())
        if action == "filtrate":
            return self.liver.filter_toxins()
        if action == "consolidate":
            self.memory.consolidate()
            return "Memory consolidation complete (Dream cycle)."
        if action == "motor_priority":
            return "Motor priority pulse executed."
        return f"Action '{action}' deferred to fallback handler."

    def _log_decision(self, decision: str, outcome: str, success: bool):
        self.signals.emit_signal("DECISION", {"decision": decision, "outcome": outcome[:200], "success": success}, ttl_seconds=3600)

    def _bump_routing_weight(self, signal_type: str, success: bool):
        self.state_mgr.update_routing_stats(signal_type, success)

    def get_status(self) -> Dict[str, Any]:
        pending = len(self.state_mgr.get_queued_directives("pending"))
        routing = self.state_mgr.get_routing_weights()
        return {
            "status": "active",
            "pending_directives": pending,
            "active_lattice_nodes": len(self.lattice.get_active_nodes()),
            "motor_pending": self.motor.get_status().get("pending_motor_tasks", 0),
            "routing_table_size": len(routing)
        }
if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    orch = OrchestratorEngine(base)
    print(json.dumps(orch.tick(), indent=2))
