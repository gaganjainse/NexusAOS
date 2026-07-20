"""
Nexus Corporate OS - Metabolism Engine
Version: 1.0.0
Description: Tracks and manages system energy (tokens and resource budget).
"""

import json
import os
from pathlib import Path
from datetime import datetime

class MetabolismEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.state_path = base_dir / "core" / "monitoring" / "metabolism.json"
        self.default_budget = 1000000  # Default 1M tokens/units
        self._ensure_state_exists()

    def _ensure_state_exists(self):
        if not self.state_path.parent.exists():
            self.state_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.state_path.exists():
            self.reset_budget()

    def reset_budget(self):
        """Resets the energy budget to default."""
        initial_state = {
            "max_energy": self.default_budget,
            "current_energy": self.default_budget,
            "last_reset": datetime.now().isoformat(),
            "status": "Healthy"
        }
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(initial_state, f, indent=4)

    def consume_energy(self, amount: int):
        """Deducts energy from the current budget."""
        state = self.get_full_state()
        state["current_energy"] = max(0, state["current_energy"] - amount)
        state["status"] = self._calculate_status(state["current_energy"], state["max_energy"])

        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        return state["status"]

    def _calculate_status(self, current, max_val):
        percentage = (current / max_val) * 100
        if percentage < 10:
            return "Critical"
        elif percentage < 30:
            return "Conserving"
        return "Healthy"

    def get_status(self):
        """Returns the current energy status string."""
        return self.get_full_state().get("status", "Unknown")

    def get_full_state(self):
        """Returns the full metabolic state dictionary."""
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.reset_budget()
            return self.get_full_state()

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    engine = MetabolismEngine(base)
    print(f"Metabolic Status: {engine.get_status()}")
    print(f"Energy Remaining: {engine.get_full_state()['current_energy']}")
