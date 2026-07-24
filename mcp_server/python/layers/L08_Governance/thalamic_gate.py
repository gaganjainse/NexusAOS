"""
ThalamicGate — Thalamic gating layer
Biological analog: Thalamus as sensory relay and consciousness filter

Responsibilities (1:1 biology mapping):
- Sensory relay gating
- Consciousness/awareness filter
- Attention routing pre-filter
- Cortical broadcast gating
"""

from __future__ import annotations

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

TOOL_BASE_DIR = Path(__file__).resolve().parent.parent.parent


@dataclass
class ThalamicState:
    gated_signals: int = 0
    passed_signals: int = 0
    last_update: float = field(default_factory=time.time)


class ThalamicGate:
    """Thalamic gating — consciousness/awareness filter."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = ThalamicState()
        self.allowed_signal_types: Set[str] = {"SENSE", "DIRECTIVE", "INTERNAL"}
        self.blocked_signal_types: Set[str] = set()

    def check(self, tool_name: str) -> Dict:
        """Thalamic gating — consciousness filter."""
        blocked = tool_name in self.blocked_signal_types
        if blocked:
            self.state.gated_signals += 1
            return {
                "allowed": False,
                "reason": "thalamic_gate_blocked",
                "tool": tool_name,
            }

        self.state.passed_signals += 1
        return {
            "allowed": True,
            "gate": "thalamus",
        }

    def relay_sense(self, signal_type: str, payload: Dict) -> Dict:
        """Relay sensory signal to cortex."""
        if signal_type not in self.allowed_signal_types:
            return {
                "relayed": False,
                "reason": "signal_type_not_permitted",
                "allowed_types": list(self.allowed_signal_types),
            }

        return {
            "relayed": True,
            "signal_type": signal_type,
            "payload": payload,
        }
