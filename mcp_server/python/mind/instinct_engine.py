"""
NexusAOS - Instinct Engine (Autonomic Motivations)
Version: 1.0.0
Description: Defines long-term biological drives that guide background behavior.
"""

import time
from pathlib import Path
from typing import Dict, List, Optional
from soma.nervous.signal_router import SignalRouter
from soma.metabolic.metabolism_engine import MetabolismEngine
from mind.thought_agent import ThoughtAgent

class InstinctEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)
        self.metabolism = MetabolismEngine(base_dir)
        self.thought = ThoughtAgent(base_dir)
        self.last_ingestion = time.time()
        self.last_consolidation = time.time()

    def evaluate_drives(self) -> List[str]:
        """Evaluates long-term biological needs and emits motivational signals."""
        vitals = self.metabolism._report()
        energy = vitals.get("energy", 100)
        atp = vitals.get("atp", 100)
        
        actions = []

        # 1. Curiosity Instinct (Nutrient Ingestion)
        # Drive: Search for information when energy is high (>80%) and we haven't 'eaten' in 1 hour.
        if energy > 80 and (time.time() - self.last_ingestion > 3600):
            actions.append(self._trigger_curiosity())

        # 2. Consolidation Instinct (Sleep/Memory)
        # Drive: Move short-term canvas data to long-term archives when energy is low (<40%).
        if energy < 40 and (time.time() - self.last_consolidation > 7200):
            actions.append(self._trigger_consolidation())

        # 3. Evolutionary Instinct (Growth)
        # Drive: Trigger a mutation cycle when ATP is abundant (>90%).
        if atp > 90:
            actions.append(self._trigger_growth())

        return [a for a in actions if a]

    def _trigger_curiosity(self) -> str:
        self.last_ingestion = time.time()
        self.signals.emit_signal(
            "INSTINCT_CURIOSITY",
            {"action": "INGEST_NUTRIENTS", "target": "DIGESTIVE_ENGINE"},
            ttl_seconds=3600
        )
        return "Curiosity Drive: Seeking new environmental nutrients."

    def _trigger_consolidation(self) -> str:
        self.last_consolidation = time.time()
        self.signals.emit_signal(
            "INSTINCT_CONSOLIDATION",
            {"action": "SLEEP_CONSOLIDATE", "target": "STATE_MANAGER"},
            ttl_seconds=1800
        )
        return "Consolidation Drive: System requires sleep to harden memory."

    def _trigger_growth(self) -> str:
        self.signals.emit_signal(
            "INSTINCT_GROWTH",
            {"action": "EVOLVE_POLICIES", "target": "EVOLUTION_ENGINE"},
            ttl_seconds=600
        )
        return "Growth Drive: ATP abundant. Triggering evolutionary mutation."

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    instinct = InstinctEngine(base)
    print("Drives:", instinct.evaluate_drives())
