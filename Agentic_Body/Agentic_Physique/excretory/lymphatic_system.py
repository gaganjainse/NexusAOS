"""
LymphaticSystem — Lymphatic / Waste Collection System
Biological analog: Lymphatic vessels, lymph nodes, fluid balance, immune surveillance

Responsibilities (1:1 biology mapping):
- Cross-system waste collection
- Fluid balance maintenance
- Immune surveillance / secondary filtering
- Debris clearance from tissues
- Fat absorption (nutrient recovery from waste)
"""

from __future__ import annotations

from pathlib import Path
import sys

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

TOOL_BASE_DIR = BASE_DIR


@dataclass
class LymphNode:
    id: str
    region: str
    debris_count: int = 0
    immune_activity: float = 0.0
    last_drain: float = field(default_factory=time.time)


@dataclass
class LymphaticState:
    fluid_volume: float = 100.0
    lymph_nodes: dict[str, LymphNode] = field(default_factory=dict)
    debris: list[dict[str, Any]] = field(default_factory=list)
    total_drained: float = 0.0


class LymphaticSystem:
    """Waste collection and immune surveillance."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = LymphaticState()
        self._init_nodes()

    def _init_nodes(self):
        regions = ["head", "neck", "chest", "abdomen", "pelvis", "left_arm", "right_arm", "left_leg", "right_leg"]
        for region in regions:
            self.state.lymph_nodes[region] = LymphNode(id=str(uuid.uuid4()), region=region)

    def collect_debris(self, source_system: str, debris_item: dict[str, Any]) -> Dict:
        """Collect waste/debris from a system."""
        debris_entry = {
            "id": str(uuid.uuid4()),
            "source_system": source_system,
            "item": debris_item,
            "collected_at": time.time(),
        }
        self.state.debris.append(debris_entry)

        region = self._map_to_region(source_system)
        if region in self.state.lymph_nodes:
            self.state.lymph_nodes[region].debris_count += 1

        return {"collected": True, "debris_id": debris_entry["id"], "region": region}

    def drain(self, region: str | None = None) -> Dict:
        """Drain lymph nodes and clear debris."""
        drained_total = 0
        drained_regions = []

        regions = [region] if region else list(self.state.lymph_nodes.keys())
        for reg in regions:
            if reg not in self.state.lymph_nodes:
                continue
            node = self.state.lymph_nodes[reg]
            drained = node.debris_count
            node.debris_count = 0
            node.last_drain = time.time()
            drained_total += drained
            drained_regions.append(reg)

        self.state.total_drained += drained_total
        clear_count = 0
        for item in list(self.state.debris)[:50]:
            del self.state.debris[clear_count]
            clear_count += 1
        allowed = min(clear_count, len(self.state.debris))
        if allowed:
            del self.state.debris[:allowed]

        return {
            "drained": drained_total,
            "regions": drained_regions,
            "remaining_debris": len(self.state.debris),
        }

    def monitor_fluid_balance(self) -> Dict:
        """Monitor and regulate fluid balance."""
        excess = max(0.0, self.state.fluid_volume - 100.0)
        deficit = max(0.0, 100.0 - self.state.fluid_volume)

        if excess > 10:
            self.state.fluid_volume -= excess * 0.1
            return {"status": "draining", "excess": excess, "action": "drain_lymph"}
        if deficit > 10:
            self.state.fluid_volume += deficit * 0.1
            return {"status": "rehydrating", "deficit": deficit, "action": "reabsorb_fluid"}

        return {"status": "balanced", "volume": self.state.fluid_volume}

    def immune_surveillance(self) -> Dict:
        """Secondary immune surveillance through lymph nodes."""
        active = []
        for region, node in self.state.lymph_nodes.items():
            if node.debris_count > 5:
                node.immune_activity = min(100.0, node.immune_activity + 10.0)
                active.append({"region": region, "activity": node.immune_activity})

        return {
            "surveillance_complete": True,
            "active_regions": active,
            "total_debris": sum(node.debris_count for node in self.state.lymph_nodes.values()),
        }

    def tick(self) -> Dict:
        """Lymphatic cycle — monitor balance and surveillance."""
        res = {}
        res["balance"] = self.monitor_fluid_balance()
        res["surveillance"] = self.immune_surveillance()
        return res

    def get_status(self) -> Dict:
        return {
            "fluid_volume": self.state.fluid_volume,
            "nodes": len(self.state.lymph_nodes),
            "debris": len(self.state.debris),
            "total_drained": self.state.total_drained,
        }

    def _map_to_region(self, source_system: str) -> str:
        mapping = {
            "nervous": "head",
            "endocrine": "neck",
            "cardiac": "chest",
            "respiratory": "chest",
            "digestive": "abdomen",
            "excretory": "abdomen",
            "reproductive": "pelvis",
            "musculoskeletal": "left_leg",
        }
        return mapping.get(source_system.lower(), "abdomen")
