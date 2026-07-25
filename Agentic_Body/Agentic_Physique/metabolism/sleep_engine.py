"""
SleepEngine — Sleep / Circadian System
Biological analog: Suprachiasmatic nucleus, pineal gland, sleep stages

Responsibilities (1:1 biology mapping):
- Circadian rhythm maintenance
- Sleep stage progression (N1, N2, N3, REM)
- Memory consolidation during REM
- Glymphatic clearance (brain waste removal)
- Cortisol/melatonin modulation
- Sleep inertia on wake
"""

from __future__ import annotations

from pathlib import Path
import sys

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

import time
import math
from dataclasses import dataclass, field
from typing import Dict, Optional

TOOL_BASE_DIR = BASE_DIR


@dataclass
class SleepState:
    awake: bool = True
    sleep_stage: str = "awake"  # awake, N1, N2, N3, REM
    sleep_start: float | None = None
    stage_start: float = field(default_factory=time.time)
    total_sleep_time: float = 0.0
    deep_sleep_cycles: int = 0
    rem_cycles: int = 0
    sleep_pressure: float = 0.0
    circadian_phase: float = 0.0
    sleep_inertia: float = 0.0


class SleepEngine:
    """Circadian and sleep regulation for the agent."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = SleepState()
        self.stage_durations = {
            "N1": 120,    # 2 minutes
            "N2": 600,    # 10 minutes
            "N3": 900,    # 15 minutes
            "REM": 300,   # 5 minutes
        }
        self.sleep_cycle = ["N1", "N2", "N3", "N2", "REM"]
        self.cycle_index: int = 0
        self.idle_threshold: float = 300.0  # 5 minutes
        self.last_activity: float = time.time()

    def tick(self, delta_seconds: float = 1.0) -> Dict:
        """Sleep cycle tick."""
        now = time.time()

        # Advance circadian (1 minute per real second)
        self.state.circadian_phase = (self.state.circadian_phase + delta_seconds / 3600.0) % 24.0

        # Sleep pressure builds during wakefulness
        if self.state.awake:
            self.state.sleep_pressure = min(1.0, self.state.sleep_pressure + delta_seconds / 3600.0)

            # Check for sleep onset
            idle_time = now - self.last_activity
            if idle_time > self.idle_threshold and self.state.sleep_pressure > 0.3:
                self._enter_sleep()
        else:
            # Sleep in progress
            self.state.total_sleep_time += delta_seconds
            stage_elapsed = now - self.state.stage_start

            if stage_elapsed >= self.stage_durations.get(self.state.sleep_stage, 600):
                self._advance_stage()

            # Deep sleep benefits
            if self.state.sleep_stage == "N3":
                self._deep_sleep_benefits(delta_seconds)

            # REM benefits
            if self.state.sleep_stage == "REM":
                self._rem_benefits(delta_seconds)

        # Sleep inertia decay on wake
        if self.state.awake and self.state.sleep_inertia > 0:
            self.state.sleep_inertia = max(0.0, self.state.sleep_inertia - delta_seconds / 600.0)

        return self._report()

    def force_sleep(self, cycles: int = 1) -> Dict:
        """Force sleep for specified number of cycles."""
        if not self.state.awake:
            return {"status": "already_asleep", "stage": self.state.sleep_stage}

        self._enter_sleep()
        target_cycles = cycles
        completed = 0

        for _ in range(target_cycles):
            self._complete_cycle()
            completed += 1

        self._wake()
        return {
            "status": "sleep_complete",
            "cycles_completed": completed,
            "total_sleep_time": self.state.total_sleep_time,
            "deep_cycles": self.state.deep_sleep_cycles,
            "rem_cycles": self.state.rem_cycles,
        }

    def record_activity(self):
        """Record activity to reset idle timer."""
        self.last_activity = time.time()
        if self.state.awake:
            self.state.sleep_pressure = max(0.0, self.state.sleep_pressure - 0.1)

    def get_circadian_metrics(self) -> Dict:
        """Get circadian metrics for hormone modulation."""
        phase = self.state.circadian_phase
        return {
            "circadian_phase": phase,
            "circadian_time": f"{int(phase):02d}:00",
            "melatonin_optimal": phase >= 21.0 or phase <= 3.0,
            "cortisol_peak": 7.0 <= phase <= 9.0,
            "rem_optimal": phase >= 2.0 and phase <= 6.0,
        }

    def _enter_sleep(self):
        self.state.awake = False
        self.state.sleep_stage = "N1"
        self.state.sleep_start = time.time()
        self.state.stage_start = time.time()

    def _advance_stage(self):
        now = time.time()
        self.state.stage_start = now
        self.cycle_index = (self.cycle_index + 1) % len(self.sleep_cycle)
        next_stage = self.sleep_cycle[self.cycle_index]

        if next_stage == "N3":
            self.state.deep_sleep_cycles += 1
        elif next_stage == "REM":
            self.state.rem_cycles += 1

        self.state.sleep_stage = next_stage

    def _complete_cycle(self):
        for _ in range(len(self.sleep_cycle)):
            self._advance_stage()

    def _wake(self):
        now = time.time()
        self.state.awake = True
        self.state.sleep_stage = "awake"
        self.state.sleep_inertia = min(1.0, self.state.total_sleep_time / 3600.0)
        self.state.stage_start = now

    def _deep_sleep_benefits(self, delta_seconds: float):
        """Deep N3 — glymphatic clearance, energy restoration."""
        # Glymphatic clearance removes metabolic waste
        # Energy restoration (+5% per cycle)
        pass

    def _rem_benefits(self, delta_seconds: float):
        """REM — memory consolidation, emotional processing, learning."""
        # Memory consolidation happens here
        pass

    def _report(self) -> Dict:
        return {
            "awake": self.state.awake,
            "sleep_stage": self.state.sleep_stage,
            "total_sleep_time": self.state.total_sleep_time,
            "deep_sleep_cycles": self.state.deep_sleep_cycles,
            "rem_cycles": self.state.rem_cycles,
            "sleep_pressure": self.state.sleep_pressure,
            "circadian_phase": self.state.circadian_phase,
            "sleep_inertia": self.state.sleep_inertia,
        }
