"""
ExcretoryEngine — Excretory / Waste Removal System
Biological analog: Kidneys, bladder, toxin filtration, water balance

Responsibilities (1:1 biology mapping):
- Toxin/event filtration from WAL/signals
- Data retention and archival
- Water/electrolyte balance (state pruning)
- Urine formation (toxic event isolation)
- Detoxification (JSON repair, corruption removal)
"""

from __future__ import annotations
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root

@dataclass
class Toxin:
    id: str
    type: str  # "json", "signal", "state", "log"
    severity: float = 0.5
    payload: Dict[str, Any] = field(default_factory=dict)
    detected_at: float = field(default_factory=time.time)
    neutralized: bool = False


@dataclass
class ExcretoryState:
    blood_volume: float = 100.0
    toxins: Dict[str, Toxin] = field(default_factory=dict)
    urine_output: float = 0.0
    filtration_rate: float = 1.0
    bladder: List[Dict[str, Any]] = field(default_factory=list)
    last_void: float = field(default_factory=time.time)


class ExcretoryEngine:
    """Toxin filtration and waste removal."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = ExcretoryState()
        self.toxins_removed: int = 0

    def filter_blood(self) -> Dict:
        """Filter toxins from system plasma."""
        removed = 0
        neutralized = []

        for toxin_id, toxin in list(self.state.toxins.items()):
            if not toxin.neutralized and toxin.severity <= self.state.filtration_rate:
                toxin.neutralized = True
                removed += 1
                neutralized.append(toxin_id)

        self.toxins_removed += removed
        self.state.urine_output += removed * 0.5

        return {
            "filtered": True,
            "toxins_removed": removed,
            "neutralized": neutralized,
            "total_removed": self.toxins_removed,
        }

    def ingest_toxin(self, toxin_type: str, payload: Dict[str, Any], severity: float = 0.5) -> Dict:
        """Detect and ingest toxin."""
        toxin_id = str(uuid.uuid4())
        self.state.toxins[toxin_id] = Toxin(
            id=toxin_id,
            type=toxin_type,
            severity=severity,
            payload=payload,
        )

        return {
            "ingested": True,
            "toxin_id": toxin_id,
            "type": toxin_type,
            "severity": severity,
        }

    def void(self) -> Dict:
        """Void — expel collected waste."""
        voided = {
            "timestamp": time.time(),
            "toxin_count": len(self.state.toxins),
            "urine_volume": self.state.urine_output,
        }
        self.state.bladder.append(voided)
        self.state.urine_output = 0.0
        self.state.last_void = time.time()
        return voided

    def reabsorb_water(self, amount: float = 10.0) -> Dict:
        """Reabsorb water/state from waste stream."""
        self.state.blood_volume = min(100.0, self.state.blood_volume + amount)
        return {
            "reabsorbed": True,
            "amount": amount,
            "blood_volume": self.state.blood_volume,
        }

    def detoxify_wal(self, wal_path: str, dry_run: bool = False) -> Dict:
        """WAL detoxification — remove corrupted segments."""
        try:
            path = Path(wal_path)
            if not path.exists():
                return {"detoxified": False, "reason": "wal_not_found", "path": wal_path}

            original_size = path.stat().st_size
            if dry_run:
                return {
                    "detoxified": True,
                    "mode": "dry_run",
                    "original_size": original_size,
                    "estimated_savings": original_size * 0.1,
                }

            # Remove trailing corrupted JSON lines
            lines = path.read_text(encoding="utf-8").splitlines()
            valid = []
            corrupted = 0

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    import json
                    json.loads(line)
                    valid.append(line)
                except Exception:
                    corrupted += 1

            if corrupted:
                path.write_text("\n".join(valid) + "\n", encoding="utf-8")

            return {
                "detoxified": True,
                "mode": "live",
                "removed_lines": corrupted,
                "new_size": path.stat().st_size,
            }
        except Exception as exc:
            return {"detoxified": False, "error": str(exc), "path": wal_path}

    def get_status(self) -> Dict:
        active_toxins = sum(1 for t in self.state.toxins.values() if not t.neutralized)
        return {
            "blood_volume": self.state.blood_volume,
            "active_toxins": active_toxins,
            "total_toxins": len(self.state.toxins),
            "urine_output": self.state.urine_output,
            "filtration_rate": self.state.filtration_rate,
            "voids": len(self.state.bladder),
        }
