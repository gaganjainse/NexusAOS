"""
OxidationModel — Fission and Fusion with reactive oxidative behavior
Biological analog: Fission (mitosis-like branching), Fusion (lineage merging),
oxidative damage (entropy/aging), antioxidation (repair/maturation)

Responsibilities (1:1 biology mapping):
- Fission: create child units with branching lineage and oxidative cost
- Fusion: merge units/lineage with compatibility and oxidative risk
- Oxidation accumulate state per lineage instance
- Antioxidant repair: reduce cumulative oxidative burden
- Operational limits: block or throttle when oxidative stress is high
"""

from __future__ import annotations

import sys
from pathlib import Path
_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

import math
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

TOOL_BASE_DIR = BASE_DIR


@dataclass
class LineageInstance:
    instance_id: str
    parent_id: Optional[str]
    created_at: float = field(default_factory=time.time)
    oxidative_load: float = 0.0
    generations: int = 1
    fission_count: int = 0
    fusion_count: int = 0
    last_event: str = "born"


@dataclass
class OxidationState:
    instances: Dict[str, LineageInstance] = field(default_factory=dict)
    global_oxidative_pressure: float = 0.0
    antioxidant_capacity: float = 100.0


class OxidationModel:
    """Track oxidative stress and govern fission/fusion operations."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = OxidationState()
        self.fission_oxidation_cost: float = 12.0
        self.fusion_oxidation_cost: float = 18.0
        self.antioxidant_repair_rate: float = 8.0
        self.max_safe_oxidative_load: float = 75.0

    def create_instance(self, parent_id: Optional[str] = None) -> LineageInstance:
        instance_id = str(uuid.uuid4())
        instance = LineageInstance(
            instance_id=instance_id,
            parent_id=parent_id,
            oxidative_load=5.0,
        )
        self.state.instances[instance_id] = instance
        self._update_global_pressure()
        return instance

    def fission(self, parent_id: str) -> Dict:
        if parent_id not in self.state.instances:
            return {"allowed": False, "reason": "parent_not_found", "parent_id": parent_id}

        parent = self.state.instances[parent_id]
        parent.oxidative_load += self.fission_oxidation_cost
        parent.fission_count += 1
        parent.last_event = "fission"

        child = self.create_instance(parent_id=parent_id)
        child.generations = parent.generations + 1
        child.last_event = "born_after_fission"

        self._update_global_pressure()
        return {
            "allowed": True,
            "event": "fission",
            "parent_id": parent_id,
            "child_id": child.instance_id,
            "oxidative_load": parent.oxidative_load,
            "global_pressure": self.state.global_oxidative_pressure,
        }

    def fuse(self, instance_a: str, instance_b: str) -> Dict:
        if instance_a not in self.state.instances or instance_b not in self.state.instances:
            return {"allowed": False, "reason": "instance_not_found"}

        a = self.state.instances[instance_a]
        b = self.state.instances[instance_b]

        merged_load = (a.oxidative_load + b.oxidative_load) / 2 + self.fusion_oxidation_cost
        if merged_load > self.max_safe_oxidative_load:
            return {
                "allowed": False,
                "reason": "oxidative_limit_exceeded",
                "merged_load": merged_load,
                "limit": self.max_safe_oxidative_load,
            }

        merged_id = str(uuid.uuid4())
        merged = LineageInstance(
            instance_id=merged_id,
            parent_id=None,
            oxidative_load=merged_load,
            generations=max(a.generations, b.generations),
            fission_count=a.fission_count + b.fission_count,
            fusion_count=a.fusion_count + b.fusion_count + 1,
        )
        merged.last_event = "fusion"
        self.state.instances[merged_id] = merged

        a.oxidative_load = merged_load * 0.25
        b.oxidative_load = merged_load * 0.25
        a.last_event = "fused"
        b.last_event = "fused"

        self._update_global_pressure()
        return {
            "allowed": True,
            "event": "fusion",
            "instance_a": instance_a,
            "instance_b": instance_b,
            "merged_id": merged_id,
            "oxidaton": merged.oxidative_load,
            "global_pressure": self.state.global_oxidative_pressure,
        }

    def antioxidant_repair(self, instance_id: str) -> Dict:
        if instance_id not in self.state.instances:
            return {"repaired": False, "reason": "instance_not_found"}

        instance = self.state.instances[instance_id]
        before = instance.oxidative_load
        instance.oxidative_load = max(0.0, instance.oxidative_load - self.antioxidant_repair_rate)
        self._update_global_pressure()
        return {
            "repaired": True,
            "instance_id": instance_id,
            "before": before,
            "after": instance.oxidative_load,
        }

    def should_throttle(self) -> Dict:
        if self.state.global_oxidative_pressure >= self.max_safe_oxidative_load:
            return {
                "throttled": True,
                "reason": "high_oxidative_pressure",
                "pressure": self.state.global_oxidative_pressure,
            }
        return {
            "throttled": False,
            "pressure": self.state.global_oxidative_pressure,
        }

    def get_instance_status(self, instance_id: str) -> Dict:
        if instance_id not in self.state.instances:
            return {"found": False, "instance_id": instance_id}
        instance = self.state.instances[instance_id]
        return {
            "found": True,
            "instance_id": instance_id,
            "parent_id": instance.parent_id,
            "generations": instance.generations,
            "fission_count": instance.fission_count,
            "fusion_count": instance.fusion_count,
            "oxidative_load": instance.oxidative_load,
            "last_event": instance.last_event,
        }

    def _update_global_pressure(self):
        count = len(self.state.instances)
        if count == 0:
            self.state.global_oxidative_pressure = 0.0
            return
        total = sum(instance.oxidative_load for instance in self.state.instances.values())
        self.state.global_oxidative_pressure = total / count
