"""CorticalGate — Cortical gating layer
Biological analog: Prefrontal cortex, executive function, rule-based control

Responsibilities (1:1 biology mapping):
- Executive control / rule-based gating
- Working memory gating
- Developmental rule enforcement
- Task set gating
- Safety/ethics gating
"""

from __future__ import annotations

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

TOOL_BASE_DIR = Path(__file__).resolve().parent.parent.parent


class _DevelopmentStandIn:
    current_stage = "Adult"


DevelopmentalBoot = _DevelopmentStandIn()


@dataclass
class CorticalState:
    active_rules: List[str] = field(default_factory=list)
    blocked_tools: Set[str] = field(default_factory=set)
    executive_enabled: bool = True
    last_update: float = field(default_factory=time.time)


class CorticalGate:
    """Frontal cortex executive control gate."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = CorticalState()
        self.rules: List[Dict] = []
        self._init_default_rules()

    def _init_default_rules(self):
        self.rules = [
            {"name": "no_destructive_system_calls", "pattern": "rm -rf /", "severity": "critical"},
            {"name": "no_credential_exposure", "pattern": "password|secret|token", "severity": "high"},
            {"name": "no_network_without_receptor", "pattern": "curl|wget|http", "severity": "medium"},
        ]

    def check(self, tool_name: str, args: Dict) -> Dict:
        """Cortical gating — executive control."""
        if not self.state.executive_enabled:
            return {
                "allowed": True,
                "gate": "cortex_disabled",
            }

        blocked = tool_name in self.state.blocked_tools
        if blocked:
            return {
                "allowed": False,
                "reason": "cortical_executive_block",
                "tool": tool_name,
            }

        developmental = self._check_developmental(tool_name)
        if not developmental["allowed"]:
            return developmental

        safety = self._check_safety(tool_name, args)
        if not safety["allowed"]:
            return safety

        return {
            "allowed": True,
            "gate": "cortex",
        }

    def block_tool(self, tool_name: str):
        self.state.blocked_tools.add(tool_name)
        self.state.active_rules.append(f"block:{tool_name}")

    def unblock_tool(self, tool_name: str):
        self.state.blocked_tools.discard(tool_name)

    def _check_developmental(self, tool_name: str) -> Dict:
        current_stage = getattr(DevelopmentalBoot, "current_stage", "Adult")
        allowed_stages = ["Adult"]
        if current_stage not in allowed_stages:
            return {
                "allowed": False,
                "reason": f"developmental_stage_{current_stage}",
                "required": allowed_stages,
            }
        return {"allowed": True}

    def _check_safety(self, tool_name: str, args: Dict) -> Dict:
        args_text = json.dumps(args) if not isinstance(args, str) else args
        for rule in self.rules:
            pattern = rule.get("pattern", "")
            if pattern and pattern.lower() in args_text.lower():
                return {
                    "allowed": False,
                    "reason": f"cortical_safety_rule:{rule['name']}",
                    "severity": rule.get("severity", "medium"),
                }
        return {"allowed": True}
