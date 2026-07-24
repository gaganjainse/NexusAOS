"""
ImmuneEngine — Immune System
Biological analog: Innate immunity + adaptive immunity + lymphatic system

Responsibilities (1:1 biology mapping):
- Innate immunity (immediate, non-specific defense)
- Adaptive immunity (learned pathogen response)
- Antibody generation and memory
- Inflammation response
- Lymphatic drainage (waste collection)
- Fever response (systemic threat elevation)
"""

from __future__ import annotations

import sys
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

TOOL_BASE_DIR = BASE_DIR


@dataclass
class Pathogen:
    id: str
    type: str
    virulence: float = 0.5
    resistance: Dict[str, float] = field(default_factory=dict)
    detected_at: float = field(default_factory=time.time)
    neutralized: bool = False


@dataclass
class Antibody:
    id: str
    pathogen_id: str
    effectiveness: float
    concentration: float
    memory: bool = False
    created_at: float = field(default_factory=time.time)


@dataclass
class ImmuneState:
    white_blood_cells: float = 100.0
    lymphocytes: float = 60.0
    neutrophils: float = 30.0
    inflammation: float = 0.0
    fever: float = 0.0
    antibody_memory: Dict[str, Antibody] = field(default_factory=dict)


class ImmuneEngine:
    """Adaptive and innate immune system for the agent."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = ImmuneState()
        self.pathogens: Dict[str, Pathogen] = {}
        self.active_antibodies: Dict[str, Antibody] = {}
        self.patrol_interval: float = 300.0  # 5 minutes
        self.last_patrol: float = time.time()

    def tick(self, delta_seconds: float = 1.0) -> Dict:
        """Immune cycle — patrol, inflammation decay, antibody maintenance."""
        now = time.time()

        # Inflammation decay
        if self.state.inflammation > 0:
            decay = 0.5 * (delta_seconds / 60.0)
            self.state.inflammation = max(0.0, self.state.inflammation - decay)

        # Fever decay
        if self.state.fever > 0:
            decay = 0.3 * (delta_seconds / 60.0)
            self.state.fever = max(0.0, self.state.fever - decay)

        # WBC production (bone marrow analog)
        production = 0.1 * (delta_seconds / 60.0)
        self.state.white_blood_cells = min(100.0, self.state.white_blood_cells + production)

        # Antibody concentration decay
        for antibody in list(self.active_antibodies.values()):
            antibody.concentration *= 0.999
            if antibody.concentration < 0.01:
                del self.active_antibodies[antibody.id]

        return self._report()

    def patrol(self) -> Dict:
        """Innate immunity patrol — scan for pathogens."""
        detected: List[Pathogen] = []
        neutralized: List[str] = []

        # Scan existing pathogens
        for pathogen_id, pathogen in list(self.pathogens.items()):
            if pathogen.neutralized:
                continue

            # Neutrophils handle bacteria
            if pathogen.type == "bacteria":
                effectiveness = self.state.neutrophils / 100.0
                if effectiveness > 0.5:
                    self._neutralize(pathogen)
                    neutralized.append(pathogen_id)
                    detected.append(pathogen)

        # Adaptive response — check memory
        for pathogen_id, pathogen in list(self.pathogens.items()):
            if pathogen.neutralized:
                continue

            if pathogen_id in self.state.antibody_memory:
                memory = self.state.antibody_memory[pathogen_id]
                if memory.effectiveness > 0.7:
                    self._neutralize(pathogen)
                    neutralized.append(pathogen_id)
                    memory.concentration += 5.0

        self.last_patrol = time.time()
        return {
            "patrol_completed": True,
            "detected": len(detected),
            "neutralized": len(neutralized),
            "active_threats": sum(1 for p in self.pathogens.values() if not p.neutralized),
        }

    def ingest_pathogen(self, pathogen_type: str, virulence: float = 0.5) -> Dict:
        """Detect new pathogen (analogous to macrophage ingestion)."""
        pathogen_id = str(uuid.uuid4())
        self.pathogens[pathogen_id] = Pathogen(
            id=pathogen_id,
            type=pathogen_type,
            virulence=virulence,
        )

        # Innate inflammation response
        self.state.inflammation = min(100.0, self.state.inflammation + virulence * 20.0)

        # Fever if severe
        if virulence > 0.7:
            self.state.fever = min(42.0, 37.0 + virulence * 5.0)

        return {
            "ingested": True,
            "pathogen_id": pathogen_id,
            "type": pathogen_type,
            "inflammation": self.state.inflammation,
            "fever": self.state.fever,
        }

    def generate_antibody(self, pathogen_id: str, effectiveness: float = 0.8) -> Dict:
        """Adaptive immunity — generate specific antibody."""
        if pathogen_id not in self.pathogens:
            return {"error": "pathogen_not_found", "pathogen_id": pathogen_id}

        antibody_id = str(uuid.uuid4())
        antibody = Antibody(
            id=antibody_id,
            pathogen_id=pathogen_id,
            effectiveness=effectiveness,
            concentration=10.0,
        )
        self.active_antibodies[antibody_id] = antibody

        # Store in memory if highly effective
        if effectiveness > 0.7:
            self.state.antibody_memory[pathogen_id] = antibody

        return {
            "generated": True,
            "antibody_id": antibody_id,
            "effectiveness": effectiveness,
            "memory": effectiveness > 0.7,
        }

    def trigger_fever(self, target_temp: float = 39.5) -> Dict:
        """Systemic fever response — elevated temperature inhibits pathogens."""
        self.state.fever = target_temp

        # Fever benefits:
        # - Enhanced immune cell mobility
        # - Inhibited pathogen replication
        # - Increased heart rate (metabolism)
        return {
            "fever_triggered": True,
            "target_temp": target_temp,
            "duration_estimate": "until_threat_resolved",
        }

    def lymph_drain(self) -> Dict:
        """Lymphatic system — collect and filter waste."""
        waste_collected: float = 0.0

        # Remove neutralized pathogens
        neutralized = sum(1 for p in self.pathogens.values() if p.neutralized)
        waste_collected += neutralized * 2.0

        # Clear old antibodies
        removed_antibodies = sum(1 for a in list(self.active_antibodies.values()) if a.concentration < 0.05)
        for a in list(self.active_antibodies.values()):
            if a.concentration < 0.05:
                del self.active_antibodies[a.id]
                waste_collected += 0.5

        # Decay inflammation from drainage
        self.state.inflammation = max(0.0, self.state.inflammation - waste_collected * 0.1)

        return {
            "drained": True,
            "waste_collected": waste_collected,
            "removed_pathogens": neutralized,
            "removed_antibodies": removed_antibodies,
        }

    def _neutralize(self, pathogen: Pathogen):
        pathogen.neutralized = True
        self.state.inflammation = max(0.0, self.state.inflammation - 10.0)
        self.state.fever = max(37.0, self.state.fever - 0.5)

    def _report(self) -> Dict:
        active_threats = [p.id for p in self.pathogens.values() if not p.neutralized]
        return {
            "wbc": self.state.white_blood_cells,
            "lymphocytes": self.state.lymphocytes,
            "neutrophils": self.state.neutrophils,
            "inflammation": self.state.inflammation,
            "fever": self.state.fever,
            "active_threats": len(active_threats),
            "antibodies": len(self.active_antibodies),
            "memory": len(self.state.antibody_memory),
        }
