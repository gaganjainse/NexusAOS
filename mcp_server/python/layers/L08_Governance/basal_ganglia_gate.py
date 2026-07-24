"""
BasalGangliaGate — Basal ganglia gating layer
Biological analog: Basal ganglia action selection, habit formation, inhibition

Responsibilities (1:1 biology mapping):
- Action selection / response gating
- Habit/procedural routing
- Inhibitory control over competing actions
- Direct/indirect pathway simulation
"""

from __future__ import annotations

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

TOOL_BASE_DIR = Path(__file__).resolve().parent.parent.parent


@dataclass
class BasalState:
    direct_pathway_activity: float = 50.0
    indirect_pathway_activity: float = 50.0
    selected_action: Optional[str] = None
    inhibited_actions: List[str] = field(default_factory=list)
    last_update: float = field(default_factory=time.time)


class BasalGangliaGate:
    """Action selection gate — basal ganglia."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = BasalState()
        self.action_history: List[Dict] = []
        self.inhibition_threshold: float = 60.0

    def check(self, tool_name: str, salience: float, competing_actions: Optional[List[str]] = None) -> Dict:
        """Basal ganglia gating — action selection."""
        competing_actions = competing_actions or []

        # Direct pathway favors selected action
        self.state.direct_pathway_activity = min(100.0, self.state.direct_pathway_activity + salience * 0.2)

        # Indirect pathway inhibits competing actions
        inhibition_power = 0.0
        for competing in competing_actions:
            if competing != tool_name:
                inhibition_power += 10.0
                self.state.inhibited_actions.append(competing)

        self.state.indirect_pathway_activity = min(100.0, self.state.indirect_pathway_activity + inhibition_power * 0.1)

        selected = self.state.direct_pathway_activity >= self.state.indirect_pathway_activity
        self.state.selected_action = tool_name if selected else None

        if not selected:
            return {
                "allowed": False,
                "reason": "basal_ganglia_inhibited",
                "tool": tool_name,
                "selected": self.state.selected_action,
            }

        if inhibiting := any(competing in self.state.inhibited_actions for competing in competing_actions):
            return {
                "allowed": False,
                "reason": "basal_ganglia_action_inhibited",
                "tool": tool_name,
            }

        return {
            "allowed": True,
            "gate": "basal_ganglia",
            "selected_action": self.state.selected_action,
        }
