"""
SeshaAOS - Instinct Engine (Autonomic Motivations)
Version: 1.0.0
Description: Defines long-term biological drives that guide background behavior.
"""

from pathlib import Path
from typing import Optional
import sys
import time

from Agentic_Body.Agentic_Intelligence.intelligence.thought_agent import ThoughtAgent
from Agentic_Body.Agentic_Physique.metabolism_engine import MetabolismEngine
from Agentic_Body.Agentic_Physique.nervous.signal_router import SignalRouter
from Agentic_Body.Agentic_Soma.Foundation.dna.dna_manager import DNAManager

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root

class InstinctEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)
        self.metabolism = MetabolismEngine(base_dir)
        self.thought = ThoughtAgent(base_dir)
        self.dna = DNAManager(base_dir)
        self.last_ingestion = time.time()
        self.last_consolidation = time.time()

    def _get_param(self, category: str, key: str, default: float) -> float:
        genome = self.dna.get_genome()
        return genome.get(category, {}).get(key, default)

    def evaluate_drives(self) -> list[str]:
        """Evaluates long-term biological needs and emits motivational signals."""
        vitals = self.metabolism._report()
        energy = vitals.get("energy", 100)
        atp = vitals.get("atp", 100)
        
        actions = []

        # 1. Curiosity Instinct (Nutrient Ingestion)
        threshold = self._get_param("instinct_drives", "curiosity_threshold", 80.0)
        freq = self._get_param("instinct_drives", "curiosity_frequency", 3600)
        if energy > threshold and (time.time() - self.last_ingestion > freq):
            actions.append(self._trigger_curiosity())

        # 2. Consolidation Instinct (Sleep/Memory)
        threshold = self._get_param("instinct_drives", "consolidation_threshold", 40.0)
        freq = self._get_param("instinct_drives", "consolidation_frequency", 7200)
        if energy < threshold and (time.time() - self.last_consolidation > freq):
            actions.append(self._trigger_consolidation())

        # 3. Evolutionary Instinct (Growth)
        threshold = self._get_param("instinct_drives", "evolution_threshold", 90.0)
        if atp > threshold:
            actions.append(self._trigger_growth())

        return [a for a in actions if a]

    def _trigger_curiosity(self) -> str:
        self.last_ingestion = time.time()
        self.signals.emit_signal(
            "INSTINCT_CURIOSITY",
            {"action": "INGEST_NUTRIENTS", "target": "DIGESTIVE_ENGINE"},
            ttl_seconds=3600,
            evidentiality="!"
        )
        return "Curiosity Drive: Seeking new environmental nutrients."

    def _trigger_consolidation(self) -> str:
        self.last_consolidation = time.time()
        self.signals.emit_signal(
            "INSTINCT_CONSOLIDATION",
            {"action": "SLEEP_CONSOLIDATE", "target": "STATE_MANAGER"},
            ttl_seconds=1800,
            evidentiality="!"
        )
        return "Consolidation Drive: System requires sleep to harden memory."

    def _trigger_growth(self) -> str:
        self.signals.emit_signal(
            "INSTINCT_GROWTH",
            {"action": "EVOLVE_POLICIES", "target": "EVOLUTION_ENGINE"},
            ttl_seconds=600,
            evidentiality="!"
        )
        return "Growth Drive: ATP abundant. Triggering evolutionary mutation."

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    instinct = InstinctEngine(base)
    print("Drives:", instinct.evaluate_drives())
