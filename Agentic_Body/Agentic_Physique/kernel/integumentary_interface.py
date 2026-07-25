# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""IntegumentaryInterface — Integumentary / Boundary System
Biological analog: Skin, barrier protection, sensory interface, temperature regulation

Responsibilities (1:1 biology mapping):
- API gateway / boundary defense
- Input/output sensory interface
- Thermal regulation (system cooling/heating)
- Barrier integrity checks
- Wound detection and sealing
"""

from __future__ import annotations

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOL_BASE_DIR = Path(__file__).resolve().parent.parent.parent


@dataclass
class SkinLayer:
    name: str
    integrity: float = 100.0
    permeability: float = 0.0
    last_compromised: Optional[float] = None


@dataclass
class IntegumentaryState:
    layers: Dict[str, SkinLayer] = field(default_factory=dict)
    temperature: float = 37.0
    wounds: List[Dict] = field(default_factory=list)
    barrier_breaches: int = 0
    last_check: float = field(default_factory=time.time)


class IntegumentaryInterface:
    """System boundary — skin/barrier layer."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = IntegumentaryState()
        self._init_layers()

    def _init_layers(self):
        self.state.layers = {
            "epidermis": SkinLayer(name="epidermis", integrity=100.0, permeability=0.1),
            "dermis": SkinLayer(name="dermis", integrity=100.0, permeability=0.05),
            "hypodermis": SkinLayer(name="hypodermis", integrity=100.0, permeability=0.02),
        }

    def inspect_boundary(self, request: Dict[str, Any]) -> Dict:
        """Inspect incoming request — boundary defense."""
        threats = self._detect_threats(request)

        if threats:
            self.state.barrier_breaches += 1
            return {
                "allowed": False,
                "threats": threats,
                "layer": "epidermis",
            }

        return {
            "allowed": True,
            "sanitized": self._sanitize(request),
        }

    def regulate_temperature(self, target_temp: float = 37.0) -> Dict:
        """Regulate system temperature."""
        current = self.state.temperature
        delta = target_temp - current

        if abs(delta) < 0.5:
            return {"regulated": True, "temperature": current}

        adjustment = delta * 0.1
        self.state.temperature = current + adjustment

        return {
            "regulated": True,
            "previous": current,
            "current": self.state.temperature,
            "target": target_temp,
        }

    def seal_wound(self, wound_id: str) -> Dict:
        """Seal system breach."""
        for wound in self.state.wounds:
            if wound.get("id") == wound_id:
                wound["sealed"] = True
                wound["sealed_at"] = time.time()
                return {"sealed": True, "wound_id": wound_id}

        return {"sealed": False, "reason": "wound_not_found", "wound_id": wound_id}

    def detect_sensory_input(self, input_data: Any) -> Dict:
        """Detect and classify sensory input through boundary."""
        input_type = self._classify_input(input_data)
        danger = self._assess_danger(input_data)

        return {
            "detected": True,
            "type": input_type,
            "danger": danger,
            "nociception": danger > 0.7,
        }

    def get_skin_health(self) -> Dict:
        """Get overall skin/barrier health."""
        avg_integrity = sum(layer.integrity for layer in self.state.layers.values()) / len(self.state.layers)
        return {
            "average_integrity": avg_integrity,
            "barrier_breaches": self.state.barrier_breaches,
            "open_wounds": sum(1 for w in self.state.wounds if not w.get("sealed")),
            "temperature": self.state.temperature,
            "status": self._health_status(avg_integrity),
        }

    def _detect_threats(self, request: Dict[str, Any]) -> List[str]:
        threats: List[str] = []
        text = str(request).lower()

        threat_patterns = [
            ("sql_injection", re.compile(r"select.*from|drop table|delete from", re.IGNORECASE)),
            ("xss", re.compile(r"<script>|javascript:", re.IGNORECASE)),
            ("command_injection", re.compile(r"rm -rf|sudo|chmod", re.IGNORECASE)),
            ("path_traversal", re.compile(r"\.\./|\.\.\\", re.IGNORECASE)),
        ]

        for threat_name, pattern in threat_patterns:
            if pattern.search(text):
                threats.append(threat_name)

        return threats

    def _sanitize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = dict(request)
        sanitized.pop("__proto__", None)
        sanitized.pop("constructor", None)
        return sanitized

    def _classify_input(self, input_data: Any) -> str:
        if isinstance(input_data, str):
            return "text"
        if isinstance(input_data, bytes):
            return "binary"
        if isinstance(input_data, dict):
            return "structured"
        return "unknown"

    def _assess_danger(self, input_data: Any) -> float:
        text = str(input_data).lower()
        danger_keywords = ["delete", "drop", "rm -rf", "sudo", "password", "secret"]
        matches = sum(1 for kw in danger_keywords if kw in text)
        return min(1.0, matches * 0.25)

    def _health_status(self, avg_integrity: float) -> str:
        if avg_integrity >= 90:
            return "healthy"
        if avg_integrity >= 70:
            return "minor_damage"
        if avg_integrity >= 50:
            return "damaged"
        return "critical"
