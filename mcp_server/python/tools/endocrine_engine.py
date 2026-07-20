"""
Nexus Corporate OS - Endocrine Engine
Version: 1.0.0
Description: Synthesizes system "Mood" and hormonal levels based on performance and energy.
"""

import json
from pathlib import Path
from typing import Dict, Any

class EndocrineEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.mood_path = base_dir / "core" / "monitoring" / "mood.json"
        self.lattice_path = base_dir / "core" / "monitoring" / "lattice_state.json"
        self.metabolism_path = base_dir / "core" / "monitoring" / "metabolism.json"
        self._ensure_state_exists()

    def _ensure_state_exists(self):
        if not self.mood_path.parent.exists():
            self.mood_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.mood_path.exists():
            initial_state = {
                "vibe": "Stable",
                "hormones": {
                    "dopamine": 50.0,
                    "serotonin": 50.0,
                    "cortisol": 10.0,
                    "adrenaline": 0.0
                }
            }
            self._write_mood(initial_state)

    def synthesize_vibe(self) -> str:
        """Calculates global mood based on history and energy."""
        mood = self.get_mood()

        # 1. Gather Inputs
        try:
            with open(self.lattice_path, "r", encoding="utf-8") as f:
                lattice = json.load(f)
            with open(self.metabolism_path, "r", encoding="utf-8") as f:
                metabolism = json.load(f)
        except:
            return mood["vibe"]

        history = lattice.get("history", [])
        energy_pct = (metabolism["current_energy"] / metabolism["max_energy"]) * 100

        # 2. Update Hormones
        # Dopamine (based on recent success)
        recent_success = len([t for t in history[-5:] if "result" in t])
        mood["hormones"]["dopamine"] = min(100.0, 20.0 + (recent_success * 15.0))

        # Serotonin (based on overall success rate)
        if history:
            success_rate = len([t for t in history if "result" in t]) / len(history)
            mood["hormones"]["serotonin"] = min(100.0, success_rate * 100.0)

        # Cortisol (based on failures and low energy)
        recent_failures = len([t for t in history[-5:] if "result" not in t])
        energy_stress = max(0.0, 50.0 - energy_pct)
        mood["hormones"]["cortisol"] = min(100.0, (recent_failures * 20.0) + energy_stress)

        # 3. Determine Vibe
        h = mood["hormones"]
        if h["cortisol"] > 60:
            mood["vibe"] = "Stressed"
        elif energy_pct < 15:
            mood["vibe"] = "Depressed"
        elif h["serotonin"] > 75 and h["dopamine"] > 70:
            mood["vibe"] = "Euphoric"
        else:
            mood["vibe"] = "Stable"

        self._write_mood(mood)
        return mood["vibe"]

    def get_mood(self) -> Dict[str, Any]:
        try:
            with open(self.mood_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"vibe": "Stable", "hormones": {}}

    def _write_mood(self, state: Dict):
        with open(self.mood_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = EndocrineEngine(base)
    print(f"Global Vibe Synthesized: {engine.synthesize_vibe()}")
    print(f"Hormonal Levels: {engine.get_mood()['hormones']}")
