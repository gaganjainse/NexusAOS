"""
SeshaAOS - Pet Emergent Consciousness Engine (L7 Integration)
Version: 13.1.0
Description: Reads ALL biological system monitoring data and computes
emergent mood, energy, voice parameters, and behavioral directives.
"""

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


@dataclass
class EmergentState:
    mood: str = "calm"
    energy_pct: float = 100.0
    vibe: float = 0.0
    cortisol: float = 0.0
    dopamine: float = 0.0
    serotonin: float = 0.0
    adrenaline: float = 0.0
    immune_temp: float = 37.0
    threat_level: str = "Negligible"
    sleep_state: str = "awake"
    sleep_cycles: int = 0
    repair_success_rate: float = 1.0
    performance_trend: float = 0.0
    synaptic_pressure: float = 1.0
    sensory_active: bool = False
    pending_directives: int = 0
    active_lattice_nodes: int = 0
    description: str = ""
    voice_pitch: str = "0%"
    voice_rate: str = "0%"
    voice_volume: str = "100"
    voice_style: str = "gentle"
    voice_name: str = "en-US-AvaMultilingualNeural"


MOOD_VOICE_MAP = {
    "calm":     {"pitch": "0%",   "rate": "0%",   "volume": "100", "style": "gentle",     "voice": "en-US-AvaMultilingualNeural"},
    "happy":    {"pitch": "+15%", "rate": "+10%",  "volume": "110", "style": "cheerful",   "voice": "en-US-JennyMultilingualNeural"},
    "focused":  {"pitch": "-5%",  "rate": "0%",    "volume": "100", "style": "determined", "voice": "en-US-GuyNeural"},
    "concerned":{"pitch": "-10%", "rate": "-5%",   "volume": "90",  "style": "sad",        "voice": "en-US-AriaNeural"},
    "anomaly":  {"pitch": "-20%", "rate": "-10%",  "volume": "85",  "style": "whispering", "voice": "en-US-AriaNeural"},
    "asleep":   {"pitch": "0%",   "rate": "-20%",  "volume": "60",  "style": "gentle",     "voice": "en-US-JennyMultilingualNeural"},
    "thinking": {"pitch": "-5%",  "rate": "-5%",   "volume": "90",  "style": "chat",       "voice": "en-US-GuyNeural"},
}


class ConsciousnessEngine:
    def __init__(self, monitoring_dir: Path):
        self.monitoring_dir = monitoring_dir
        self._last_state: Optional[EmergentState] = None
        self._history: list = []

    def tick(self) -> EmergentState:
        raw = self._read_all()
        state = self._compute(raw)
        self._last_state = state
        self._history.append({"timestamp": time.time(), "mood": state.mood, "energy": state.energy_pct})
        if len(self._history) > 500:
            self._history = self._history[-500:]
        return state

    def _read_all(self) -> Dict[str, Any]:
        raw = {}
        try:
            pf = self.monitoring_dir / "physiology.json"
            if pf.exists():
                raw["physiology"] = json.loads(pf.read_text())
        except Exception:
            raw["physiology"] = {}

        try:
            sf = self.monitoring_dir / "sensory_feed.json"
            if sf.exists():
                raw["sensory"] = json.loads(sf.read_text())
        except Exception:
            raw["sensory"] = {}

        try:
            rf = self.monitoring_dir / "repair_log.json"
            if rf.exists():
                raw["repair"] = json.loads(rf.read_text())
        except Exception:
            raw["repair"] = []

        try:
            pl = self.monitoring_dir / "performance_ledger.json"
            if pl.exists():
                raw["performance"] = json.loads(pl.read_text())
        except Exception:
            raw["performance"] = []

        try:
            pb = self.monitoring_dir / "performance_baseline.json"
            if pb.exists():
                raw["baseline"] = json.loads(pb.read_text())
        except Exception:
            raw["baseline"] = {}

        try:
            bs = self.monitoring_dir / "body_schema.json"
            if bs.exists():
                raw["body_schema"] = json.loads(bs.read_text())
        except Exception:
            raw["body_schema"] = {}

        return raw

    def _compute(self, raw: Dict[str, Any]) -> EmergentState:
        state = EmergentState()
        phys = raw.get("physiology", {})

        met = phys.get("metabolism", {})
        max_energy = met.get("max_energy", 1000)
        current_energy = met.get("current_energy", 500)
        state.energy_pct = round((current_energy / max_energy) * 100, 1)

        endo = phys.get("endocrine", {})
        hormones = endo.get("hormones", {})
        state.dopamine = hormones.get("dopamine", 50.0)
        state.serotonin = hormones.get("serotonin", 50.0)
        state.cortisol = hormones.get("cortisol", 5.0)
        state.adrenaline = hormones.get("adrenaline", 0.0)

        immune = phys.get("immune", {})
        state.immune_temp = immune.get("temperature", 37.0)
        state.threat_level = immune.get("threat_level", "Negligible")

        sleep = phys.get("sleep", {})
        state.sleep_state = sleep.get("state", "awake")
        state.sleep_cycles = sleep.get("sleep_cycles", 0)

        body_schema = raw.get("body_schema", {})
        state.synaptic_pressure = body_schema.get("synaptic_pressure", 1.0)

        sensory = raw.get("sensory", {})
        state.sensory_active = sensory.get("active", False)

        repair_log = raw.get("repair", [])
        if repair_log:
            recent = repair_log[-10:]
            successes = sum(1 for r in recent if r.get("success"))
            state.repair_success_rate = successes / len(recent)

        perf = raw.get("performance", [])
        if perf:
            last = perf[-1]
            state.performance_trend = last.get("improvement_pct", 0.0)

        state.mood = self._compute_mood(state)
        vp = MOOD_VOICE_MAP.get(state.mood, MOOD_VOICE_MAP["calm"])
        state.voice_pitch = vp["pitch"]
        state.voice_rate = vp["rate"]
        state.voice_volume = vp["volume"]
        state.voice_style = vp["style"]
        state.voice_name = vp["voice"]
        state.description = self._describe(state)
        return state

    def _compute_mood(self, s: EmergentState) -> str:
        if s.sleep_state == "asleep":
            return "asleep"

        if s.energy_pct < 15:
            return "asleep"

        if s.threat_level.lower() in ("critical", "high") or s.immune_temp > 39.0:
            return "anomaly"

        if s.cortisol > 15 or s.adrenaline > 5:
            return "anomaly"

        if s.energy_pct < 30:
            return "concerned"

        if s.cortisol > 8:
            return "concerned"

        if s.threat_level.lower() == "elevated":
            return "focused"

        if s.performance_trend < -20 and s.energy_pct > 40:
            return "focused"

        if s.dopamine > 60 and s.serotonin > 50:
            return "happy"

        if s.energy_pct > 70 and s.dopamine > 50:
            return "happy"

        if s.synaptic_pressure > 2.0:
            return "focused"

        return "calm"

    def _describe(self, s: EmergentState) -> str:
        parts = []
        parts.append(f"Energy at {s.energy_pct:.0f}%")
        parts.append(f"Vibe: dopamine {s.dopamine:.1f}/serotonin {s.serotonin:.1f}/cortisol {s.cortisol:.1f}")
        if s.immune_temp != 37.0:
            parts.append(f"Temp: {s.immune_temp:.1f}°C")
        if s.threat_level.lower() != "negligible":
            parts.append(f"Threat: {s.threat_level}")
        if s.repair_success_rate < 0.8:
            parts.append(f"Repair rate: {s.repair_success_rate:.0%}")
        if s.synaptic_pressure > 1.5:
            parts.append(f"Synaptic pressure: {s.synaptic_pressure:.1f}")
        return " | ".join(parts)

    def get_last_state(self) -> Optional[EmergentState]:
        return self._last_state

    def get_history(self) -> list:
        return self._history

