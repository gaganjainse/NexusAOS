"""
Nexus Corporate OS - Physiology Engine (Unified)
Version: 4.0.0
Description: Unified manager for Metabolism, Endocrine, and Immune systems.
Consolidates state into physiology.json for optimized performance.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class PhysiologyEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_path = base_dir / "core" / "monitoring" / "physiology.json"
        self.lattice_path = base_dir / "core" / "monitoring" / "lattice_state.json"
        self.default_budget = 1000000
        self._ensure_state_exists()

    def _ensure_state_exists(self):
        if not self.state_path.parent.exists():
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_path.exists():
            self.reset_all()

    def reset_all(self):
        """Initializes/Resets the entire physiological state."""
        state = {
            "metabolism": {
                "max_energy": self.default_budget,
                "current_energy": self.default_budget,
                "status": "Healthy",
                "last_reset": datetime.now().isoformat()
            },
            "endocrine": {
                "vibe": "Stable",
                "hormones": {
                    "dopamine": 50.0,
                    "serotonin": 50.0,
                    "cortisol": 10.0,
                    "adrenaline": 0.0
                }
            },
            "immune": {
                "temperature": 98.6,
                "threat_level": "Negligible",
                "anomalies": []
            },
            "last_sync": time.time()
        }
        self._write_state(state)

    # --- Metabolism Logic ---
    def consume_energy(self, amount: int):
        state = self.get_state()
        met = state["metabolism"]
        met["current_energy"] = max(0, met["current_energy"] - amount)

        # Calculate status
        pct = (met["current_energy"] / met["max_energy"]) * 100
        if pct < 10: met["status"] = "Critical"
        elif pct < 30: met["status"] = "Conserving"
        else: met["status"] = "Healthy"

        self._write_state(state)
        return met["status"]

    # --- Endocrine Logic ---
    def synthesize_vibe(self):
        state = self.get_state()

        # Pull lattice history for synthesis
        try:
            with open(self.lattice_path, "r", encoding="utf-8") as f:
                lattice = json.load(f)
            history = lattice.get("history", [])
        except:
            history = []

        h = state["endocrine"]["hormones"]
        energy_pct = (state["metabolism"]["current_energy"] / state["metabolism"]["max_energy"]) * 100

        # Update Hormones
        recent_success = len([t for t in history[-5:] if "result" in t])
        h["dopamine"] = min(100.0, 20.0 + (recent_success * 15.0))

        if history:
            success_rate = len([t for t in history if "result" in t]) / len(history)
            h["serotonin"] = min(100.0, success_rate * 100.0)

        recent_failures = len([t for t in history[-5:] if "result" not in t])
        energy_stress = max(0.0, 50.0 - energy_pct)
        h["cortisol"] = min(100.0, (recent_failures * 20.0) + energy_stress)

        # Determine Vibe
        if h["cortisol"] > 60: state["endocrine"]["vibe"] = "Stressed"
        elif energy_pct < 15: state["endocrine"]["vibe"] = "Depressed"
        elif h["serotonin"] > 75 and h["dopamine"] > 70: state["endocrine"]["vibe"] = "Euphoric"
        else: state["endocrine"]["vibe"] = "Stable"

        self._write_state(state)
        return state["endocrine"]["vibe"]

    # --- Immune Logic ---
    def register_anomaly(self, type: str, severity: float):
        state = self.get_state()
        imm = state["immune"]
        imm["anomalies"].append({"timestamp": time.time(), "type": type, "severity": severity})
        if len(imm["anomalies"]) > 20: imm["anomalies"].pop(0)

        imm["temperature"] = min(106.0, imm["temperature"] + severity)

        # Calculate threat
        t = imm["temperature"]
        if t >= 104.0: imm["threat_level"] = "Sepsis"
        elif t >= 102.0: imm["threat_level"] = "Fever"
        elif t >= 100.0: imm["threat_level"] = "Inflammation"
        else: imm["threat_level"] = "Negligible"

        self._write_state(state)
        return imm["threat_level"]

    def heal(self, amount: float = 0.5):
        state = self.get_state()
        imm = state["immune"]
        imm["temperature"] = max(98.6, imm["temperature"] - amount)

        t = imm["temperature"]
        if t >= 104.0: imm["threat_level"] = "Sepsis"
        elif t >= 102.0: imm["threat_level"] = "Fever"
        elif t >= 100.0: imm["threat_level"] = "Inflammation"
        else: imm["threat_level"] = "Negligible"

        self._write_state(state)

    # --- IO Helpers ---
    def get_state(self) -> Dict:
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            self.reset_all()
            return self.get_state()

    def _write_state(self, state: Dict):
        state["last_sync"] = time.time()
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = PhysiologyEngine(base)
    print("Vibe:", engine.synthesize_vibe())
    print("Energy Status:", engine.consume_energy(0))
