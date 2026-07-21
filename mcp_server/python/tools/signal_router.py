"""
NexasAOS - Signal Router (Postman / Gut / Microbiome)
Version: 2.0.0
Description: Event routing with agent-to-agent messaging (Gut/Microbiome communication).
"""
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import threading

class SignalRouter:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals_path = base_dir / "core" / "monitoring" / "signals.json"
        self.history_path = base_dir / "core" / "monitoring" / "signal_history.json"
        self.lock = threading.Lock()
        self.agent_queues: Dict[str, List[Dict]] = {}
        self.agent_callbacks: Dict[str, List[callable]] = {}

    def _load(self) -> Dict[str, Dict]:
        if self.signals_path.exists():
            return json.loads(self.signals_path.read_text(encoding="utf-8"))
        return {}

    def _save(self, data: Dict[str, Dict]):
        self.signals_path.parent.mkdir(parents=True, exist_ok=True)
        self.signals_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _log_history(self, signal_type: str, payload: Dict, ttl_seconds: int):
        entry = {
            "signal_type": signal_type,
            "payload": payload,
            "timestamp": time.time(),
            "ttl_seconds": ttl_seconds,
        }
        hist = []
        if self.history_path.exists():
            try:
                hist = json.loads(self.history_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        hist.append(entry)
        if len(hist) > 500:
            hist = hist[-500:]
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        self.history_path.write_text(json.dumps(hist, indent=2), encoding="utf-8")

    def emit_signal(self, signal_type: str, payload: Dict, ttl_seconds: int = 300):
        with self.lock:
            data = self._load()
            data[signal_type] = {
                "payload": payload,
                "emitted_at": time.time(),
                "ttl_seconds": ttl_seconds,
                "active": True,
            }
            self._save(data)
            self._log_history(signal_type, payload, ttl_seconds)
            # Wake any waiting agent listeners
            self._deliver_to_agents(signal_type, payload)

    def get_active_signals(self) -> Dict[str, Dict]:
        with self.lock:
            data = self._load()
            now = time.time()
            active = {}
            for sig, info in list(data.items()):
                if not info.get("active", False):
                    continue
                age = now - info.get("emitted_at", 0)
                if age > info.get("ttl_seconds", 300):
                    info["active"] = False
                    self._save(data)
                    continue
                active[sig] = info
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