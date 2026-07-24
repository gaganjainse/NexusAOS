"""
NexasAOS - Signal Router (Postman / Gut / Microbiome)
Version: 2.0.0
Description: Event routing with agent-to-agent messaging (Gut/Microbiome communication).
"""
import json
import sys
import threading
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from layers.L05_Memory.state_manager import StateManager
from layers.L11_Data.soma_transcended import TranscendedSubstrate
from layers.L08_Governance.sigil_x import SigilX
from layers.L11_Data.binary_nervous import BinaryNervous

class SignalRouter:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_mgr = StateManager(base_dir)
        self.substrate = TranscendedSubstrate(base_dir)
        self.sigil_x = SigilX()
        self.bin_nervous = BinaryNervous(base_dir)
        self.lock = threading.Lock()
        self.agent_queues: Dict[str, List[Dict]] = {}
        self.agent_callbacks: Dict[str, List[callable]] = {}

    def emit_signal(self, signal_type: str, payload: Dict, ttl_seconds: int = 300, evidentiality: str = "◊"):
        """
        Emits a signal into the synaptic mesh with an Evidentiality Marker.
        ::! Known, ::? Uncertain, ::◊ Predicted, ::~ Reported, ::Φ Philosophical, ::Ω Terminal
        """
        with self.lock:
            # 1. Sigil-X Hardware Signing (L08)
            signed_pulse = self.sigil_x.sign_pulse(signal_type, payload)
            
            # 2. Singularity Kernel Verification (L03/L12) - NEURAL 6.0
            # Simulated kernel-gate check
            if not signed_pulse.get("sigil", {}).get("hw"):
                return # Drop pulse if identity missing
            
            # 3. NXP-B Binary Transmission (L11 Fast-Path)
            topic_hash = hash(signal_type) & 0xFFFFFFFFFFFFFFFF
            self.bin_nervous.connect()
            self.bin_nervous.transmit_binary_pulse(topic_hash, signed_pulse["sigil"], json.dumps(payload).encode())

            # 4. P2P Mesh Publication (Transcended)
            self.substrate.publish(f"signal/{signal_type}", {
                "payload": payload,
                "evidentiality": evidentiality,
                "ts": time.time(),
                "sigil": signed_pulse["sigil"]
            })
            
            # 4. DB-Native Reflex Trigger (Neural 6.0)
            reflex = self.state_mgr.detect_native_reflex(f"{signal_type}:{json.dumps(payload)}")
            if reflex:
                self.substrate.publish("reflex/autonomic", {"action": reflex})

            # 5. Hot-State & Persistence
            self.substrate.set_vital(f"sig:{signal_type}", payload, ttl=ttl_seconds)
            self.state_mgr.upsert_signal(signal_type, payload, ttl_seconds, evidentiality)
            self.state_mgr.log_signal_history(signal_type, payload, ttl_seconds, evidentiality)
            
            # Legacy agent delivery
            self._deliver_to_agents(signal_type, payload)

    def get_active_signals(self) -> Dict[str, Dict]:
        # Favor hot-state if available, fallback to SQLite
        active = self.state_mgr.get_active_signals()
        for sig in active:
            hot = self.substrate.get_vital(f"sig:{sig}")
            if hot:
                active[sig]["payload"] = hot
        return active

    def aggregate_observe_stream(self, limit: int = 25) -> List[Dict]:
        active = self.get_active_signals()
        agg = []
        for sig, info in active.items():
            agg.append({"signal": sig, "payload": info.get("payload", {}), "age_sec": round(time.time() - info.get("emitted_at", 0), 2)})
        agg.sort(key=lambda x: -x["age_sec"])
        return agg[:limit]

    def route_pulse(self) -> str:
        active = self.get_active_signals()
        if not active:
            return "No active signals"
        actions = []
        threats = [s for s in active if s in ("NOCICEPTION", "INFLAMMATION", "Sepsis")]
        repair_signals = [s for s in active if s in ("heal", "diagnose", "auto_repair")]
        if threats and repair_signals:
            actions.append("AUTO_HEALING_TRIGGERED")
        growth = [s for s in active if s in ("GROWTH", "INTELLIGENCE", "learning")]
        if growth:
            actions.append("GROWTH_SIGNAL_DETECTED")
        return "PULSE_ROUTING -> " + (", ".join(actions) if actions else "OBSERVE")

    def wake_ncc(self):
        active = self.get_active_signals()
        return {"active_signal_count": len(active), "signals": list(active.keys())}

    def inject_vibe_feedback(self, vibe: str):
        self.emit_signal("VIBE_FEEDBACK", {"vibe": vibe, "source": "NCC"}, ttl_seconds=600)

    # --- Agent-to-Agent Communication (Gut / Microbiome) ---
    def register_agent(self, agent_id: str, callback=None):
        if agent_id not in self.agent_queues:
            self.agent_queues[agent_id] = []
            self.agent_callbacks[agent_id] = []
        if callback:
            self.agent_callbacks[agent_id].append(callback)

    def unregister_agent(self, agent_id: str):
        self.agent_queues.pop(agent_id, None)
        self.agent_callbacks.pop(agent_id, None)

    def agent_send(self, from_agent: str, to_agent: str, message_type: str, payload: Dict, ttl_seconds: int = 300) -> Dict:
        message = {
            "id": f"{from_agent}:{to_agent}:{int(time.time()*1000)}",
            "from": from_agent,
            "to": to_agent,
            "type": message_type,
            "payload": payload,
            "created_at": time.time(),
            "ttl_seconds": ttl_seconds,
            "delivered": False,
        }
        if to_agent in self.agent_queues:
            self.agent_queues[to_agent].append(message)
        # Also publish as a signal for routing visibility
        self.emit_signal("AGENT_MSG", message, ttl_seconds=ttl_seconds)
        return {"queued": True, "message_id": message["id"]}

    def agent_poll(self, agent_id: str, limit: int = 10) -> List[Dict]:
        if agent_id not in self.agent_queues:
            self.agent_queues[agent_id] = []
        queue = self.agent_queues[agent_id]
        messages = queue[:limit]
        self.agent_queues[agent_id] = queue[len(messages):]
        for msg in messages:
            self._deliver_to_callbacks(agent_id, msg)
        return messages

    def broadcast_to_role(self, from_agent: str, role: str, message_type: str, payload: Dict, ttl_seconds: int = 300) -> Dict:
        delivered = 0
        for agent_id in list(self.agent_queues.keys()):
            if role in agent_id:
                self.agent_send(from_agent, agent_id, message_type, payload, ttl_seconds=ttl_seconds)
                delivered += 1
        return {"role": role, "delivered_to": delivered}

    def _deliver_to_agents(self, signal_type: str, payload: Dict):
        for agent_id, queue in self.agent_queues.items():
            if signal_type == "AGENT_MSG" and payload.get("to") == agent_id:
                queue.append(payload)

    def _deliver_to_callbacks(self, agent_id: str, message: Dict):
        for fn in self.agent_callbacks.get(agent_id, []):
            try:
                fn(message)
            except Exception:
                pass

    def _clean_agent_queues(self):
        now = time.time()
        for agent_id, queue in list(self.agent_queues.items()):
            kept = []
            for msg in queue:
                age = now - msg.get("created_at", 0)
                if age <= msg.get("ttl_seconds", 300):
                    kept.append(msg)
            self.agent_queues[agent_id] = kept