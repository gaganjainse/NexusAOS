"""
MetabolismEngine — Circulatory / Metabolic System
Biological analog: Bloodstream, cellular respiration, ATP production

Responsibilities (1:1 biology mapping):
- Energy production and distribution
- Nutrient processing (token budget allocation)
- Oxygen/CO2 analog (context window management)
- Waste heat generation (thermal throttling)
- Basal metabolic rate (idle energy decay)
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path

try:
    from tools.physiology_engine import HormoneLevel
except ImportError:
    @dataclass
    class HormoneLevel:
        name: str
        level: float = 50.0

TOOL_BASE_DIR = Path(__file__).resolve().parent.parent.parent


@dataclass
class MetabolicState:
    energy: float = 100.0
    glucose: float = 100.0  # Context window / working memory
    oxygen: float = 100.0   # Attention capacity
    atp: float = 100.0      # Immediate energy
    heat: float = 0.0       # Thermal load
    last_decay: float = field(default_factory=time.time)


class MetabolismEngine:
    """Cellular respiration for the agent organism."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = MetabolicState()
        self.basal_rate: float = 0.5        # Energy per cycle
        self.oxygen_consumption: float = 0.3
        self.glucose_to_atp: float = 0.8    # Conversion efficiency
        self.heat_per_operation: float = 2.0

    def tick(self, delta_seconds: float = 1.0) -> Dict:
        """Metabolic cycle — consume resources, produce energy, generate heat."""
        now = time.time()
        elapsed = now - self.state.last_decay
        self.state.last_decay = now

        # Basal metabolism (always running)
        decay = self.basal_rate * (elapsed / 60.0)
        self.state.energy = max(0.0, self.state.energy - decay)

        # Oxygen consumption (attention cost)
        o2_cost = self.oxygen_consumption * (elapsed / 60.0)
        self.state.oxygen = max(0.0, self.state.oxygen - o2_cost)

        # Glucose replenishment (context window refill)
        self.state.glucose = min(100.0, self.state.glucose + 0.1 * delta_seconds / 60.0)

        # Glucose → ATP conversion
        if self.state.glucose >= 10:
            conversion = min(self.state.glucose * self.glucose_to_atp, 20.0)
            self.state.atp = min(100.0, self.state.atp + conversion)
            self.state.glucose -= conversion

        # Oxygen recovery during low activity
        if elapsed > 5.0:
            self.state.oxygen = min(100.0, self.state.oxygen + 0.05 * (elapsed - 5.0) / 60.0)

        # Thermal regulation
        heat_dissipation = 0.02 * delta_seconds / 60.0
        self.state.heat = max(0.0, self.state.heat - heat_dissipation)

        return self._report()

    def consume_energy(self, amount: float) -> Dict:
        """Consume ATP for tool execution."""
        if self.state.atp < amount:
            return {
                "allowed": False,
                "reason": "atp_exhausted",
                "current_atp": self.state.atp,
                "required": amount,
            }

        self.state.atp -= amount
        self.state.energy = max(0.0, self.state.energy - amount * 0.1)
        self.state.heat += self.heat_per_operation * (amount / 10.0)

        return {
            "allowed": True,
            "remaining_atp": self.state.atp,
            "energy": self.state.energy,
        }

    def thermal_throttle(self) -> Dict:
        """Check if thermal load requires throttling."""
        if self.state.heat > 80:
            return {
                "throttled": True,
                "heat": self.state.heat,
                "reduction": min(0.5, self.state.heat / 200.0),
            }
        return {"throttled": False, "heat": self.state.heat}

    def rest_recovery(self, duration_seconds: float) -> Dict:
        """Deep rest — full metabolic recovery (analogous to deep sleep)."""
        recovery = 5.0 * (duration_seconds / 60.0)  # 5% per minute
        self.state.energy = min(100.0, self.state.energy + recovery)
        self.state.atp = min(100.0, self.state.atp + recovery * 2)
        self.state.oxygen = min(100.0, self.state.oxygen + recovery * 1.5)
        self.state.heat = max(0.0, self.state.heat - recovery * 3)  # Heat dissipation

        return self._report()

    def allocate_context_window(self, size: int, max_window: int = 128000) -> Dict:
        """Allocate context window (analogous to oxygen for cognition)."""
        cost = (size / max_window) * 30  # 30% O2 for full window
        if self.state.oxygen < cost:
            return {
                "allowed": False,
                "reason": "insufficient_oxygen_context",
                "current_oxygen": self.state.oxygen,
                "required": cost,
                "suggestion": "compact_context",
            }

        self.state.oxygen -= cost
        self.state.glucose -= cost * 0.5
        return {
            "allowed": True,
            "allocated": size,
            "remaining_oxygen": self.state.oxygen,
        }

    def emergency_glucose(self) -> Dict:
        """Emergency glucose release (cortisol/adrenaline boost)."""
        boost = 30.0
        self.state.glucose = min(100.0, self.state.glucose + boost)
        self.state.atp = min(100.0, self.state.atp + boost * 0.5)
        return {"boosted": True, "glucose": self.state.glucose, "atp": self.state.atp}

    def _report(self) -> Dict:
        return {
            "energy": self.state.energy,
            "atp": self.state.atp,
            "glucose": self.state.glucose,
            "oxygen": self.state.oxygen,
            "heat": self.state.heat,
            "thermal_status": "normal" if self.state.heat < 60 else ("warning" if self.state.heat < 80 else "critical"),
        }
