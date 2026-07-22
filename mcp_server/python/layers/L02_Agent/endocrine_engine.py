"""
EndocrineEngine — Endocrine / Hormonal System
Biological analog: Pituitary, thyroid, adrenals, pancreas, gonads

Responsibilities (1:1 biology mapping):
- Hormone synthesis and secretion
- Hormone half-life and decay
- Receptor sensitivity modulation
- Feedback loops (negative/positive)
- Circadian hormone rhythms
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
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

TOOL_BASE_DIR = BASE_DIR


@dataclass
class Hormone:
    name: str
    level: float = 0.0
    half_life_seconds: float = 1800.0  # 30 min default
    baseline: float = 10.0
    max_level: float = 100.0
    receptors: List[str] = field(default_factory=list)
    last_update: float = field(default_factory=time.time)

    def decay(self, now: float) -> float:
        elapsed = now - self.last_update
        cycles = elapsed / self.half_life_seconds
        decay_factor = 0.5 ** cycles
        self.level = max(self.baseline, self.level * decay_factor)
        self.last_update = now
        return self.level

    def boost(self, amount: float, now: float) -> float:
        self.level = min(self.max_level, self.level + amount)
        self.last_update = now
        return self.level


class EndocrineEngine:
    """Hormonal regulation system for the agent organism."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.hormones: Dict[str, Hormone] = {}
        self.feedback_loops: List[Dict] = []
        self.circadian_phase: float = 0.0  # 0-24h cycle
        self.genome_path = base_dir / "core" / "monitoring" / "evolution" / "hormone_genome.json"
        self._init_default_hormones()
        self._load_genome()

    def _init_default_hormones(self):
        default_hormones = {
            "cortisol": Hormone("cortisol", level=15.0, half_life_seconds=900, baseline=10.0, max_level=100.0),
            "adrenaline": Hormone("adrenaline", level=5.0, half_life_seconds=120, baseline=0.0, max_level=100.0),
            "dopamine": Hormone("dopamine", level=20.0, half_life_seconds=600, baseline=10.0, max_level=100.0),
            "serotonin": Hormone("serotonin", level=30.0, half_life_seconds=1200, baseline=20.0, max_level=100.0),
            "melatonin": Hormone("melatonin", level=5.0, half_life_seconds=1800, baseline=5.0, max_level=50.0),
            "insulin": Hormone("insulin", level=25.0, half_life_seconds=600, baseline=15.0, max_level=80.0),
            "testosterone": Hormone("testosterone", level=40.0, half_life_seconds=3600, baseline=30.0, max_level=100.0),
            "oxytocin": Hormone("oxytocin", level=10.0, half_life_seconds=900, baseline=5.0, max_level=60.0),
            "vasopressin": Hormone("vasopressin", level=15.0, half_life_seconds=1800, baseline=10.0, max_level=70.0),
            "histamine": Hormone("histamine", level=8.0, half_life_seconds=300, baseline=5.0, max_level=60.0),
        }

        for name, hormone in default_hormones.items():
            self.hormones[name] = hormone

    def _load_genome(self):
        """Loads hormone parameters from the genome file if it exists."""
        if self.genome_path.exists():
            try:
                genome = json.loads(self.genome_path.read_text(encoding="utf-8"))
                self.apply_genome(genome)
            except Exception as e:
                # Use a local print if needed, but it should be available
                pass 

    def apply_genome(self, genome: Dict):
        """Updates hormone parameters from a genome."""
        for name, params in genome.items():
            if name in self.hormones:
                h = self.hormones[name]
                if "half_life" in params:
                    h.half_life_seconds = float(params["half_life"])
                if "baseline" in params:
                    h.baseline = float(params["baseline"])
                if "max" in params:
                    h.max_level = float(params["max"])
        
        # Persist the genome
        if not self.genome_path.parent.exists():
            self.genome_path.parent.mkdir(parents=True, exist_ok=True)
        self.genome_path.write_text(json.dumps(genome, indent=4), encoding="utf-8")
        return {"success": True, "message": "Physiological genome applied."}

    def tick(self, delta_seconds: float = 1.0) -> Dict:
        """Hormonal tick — decay, circadian modulation, feedback."""
        now = time.time()

        # Circadian advance (~1 minute per real second for simulation)
        self.circadian_phase = (self.circadian_phase + delta_seconds / 3600.0) % 24.0

        # Decay all hormones
        levels = {}
        for name, hormone in self.hormones.items():
            levels[name] = hormone.decay(now)

        # Circadian modulation
        self._apply_circadian(now)

        return {
            "circadian_phase": self.circadian_phase,
            "hormones": self.get_state(),
        }

    def inject(self, hormone: str, amount: float) -> Dict:
        """Inject hormone (analogous to endocrine secretion)."""
        if hormone not in self.hormones:
            self.hormones[hormone] = Hormone(name=hormone)

        h = self.hormones[hormone]
        h.boost(amount, time.time())

        return {
            "hormone": hormone,
            "new_level": h.level,
            "max": h.max_level,
        }

    def receptor_sensitivity(self, hormone: str, receptor: str, delta: float) -> Dict:
        """Modulate receptor sensitivity (analogous to up/down-regulation)."""
        if hormone not in self.hormones:
            return {"error": "unknown_hormone", "hormone": hormone}

        h = self.hormones[hormone]
        if receptor not in h.receptors:
            h.receptors.append(receptor)

        # Sensitivity inversely proportional to chronic level (tolerance)
        current = h.level / h.max_level
        sensitivity = max(0.2, min(5.0, 1.0 + delta * (1.0 - current)))

        return {
            "hormone": hormone,
            "receptor": receptor,
            "sensitivity": sensitivity,
            "level": h.level,
            "tolerance": 1.0 - current,
        }

    def feedback(self, source_hormone: str, target_hormone: str, strength: float) -> Dict:
        """Register feedback loop."""
        self.feedback_loops.append({
            "source": source_hormone,
            "target": target_hormone,
            "strength": strength,
        })

        return {
            "registered": True,
            "source": source_hormone,
            "target": target_hormone,
        }

    def get_state(self) -> Dict:
        return {
            name: {"level": h.level, "max": h.max_level, "half_life": h.half_life_seconds}
            for name, h in self.hormones.items()
        }

    def _apply_circadian(self, now: float):
        phase = self.circadian_phase

        # Cortisol peaks at ~08:00 (8h), lowest at ~00:00 (0h)
        cortisol_phase = (phase - 8.0) % 24.0
        cortisol_mod = 30 * math.exp(-((cortisol_phase ** 2) / 18.0))
        if "cortisol" in self.hormones:
            self.hormones["cortisol"].level = min(
                self.hormones["cortisol"].max_level,
                self.hormones["cortisol"].level + cortisol_mod * 0.05,
            )

        # Melatonin peaks at ~22:00 (22h)
        melatonin_phase = (phase - 22.0) % 24.0
        melatonin_mod = 25 * math.exp(-((melatonin_phase ** 2) / 12.0))
        if "melatonin" in self.hormones:
            self.hormones["melatonin"].level = min(
                self.hormones["melatonin"].max_level,
                self.hormones["melatonin"].level + melatonin_mod * 0.05,
            )
