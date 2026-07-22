"""
NexusAOS - Cardiorespiratory Loop
Version: 1.0.0
Description: Manages Context Ventilation (Respiratory) and ATP Distribution (Circulatory).
"""

import time

from typing import Dict
from layers.L02_Agent.metabolism_engine import MetabolismEngine

from pathlib import Path
import sys
_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root

class CardiorespiratoryLoop:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.metabolism = MetabolismEngine(base_dir)
        self.last_breath = time.time()

    def ventilate_context(self, current_context_size: int) -> Dict:
        """
        Respiratory: Checks context window 'oxygen' levels.
        If size is too high, triggers a 'compression' signal to free up attention.
        """
        res = self.metabolism.allocate_context_window(current_context_size)
        if not res.get("allowed"):
            return {
                "signal": "HYPOXIA",
                "action": "COMPRESS_CONTEXT",
                "message": "Oxygen low. Immediate context ventilation required."
            }
        return {"signal": "STABLE_BREATHING", "oxygen": res.get("remaining_oxygen")}

    def distribute_atp(self, agent_id: str, amount: float) -> Dict:
        """
        Circulatory: Pumps energy units to a specific agent in the swarm.
        """
        res = self.metabolism.consume_energy(amount)
        if res.get("allowed"):
            return {
                "signal": "ATP_DELIVERED",
                "agent": agent_id,
                "atp": amount,
                "remaining": res.get("remaining_atp")
            }
        return {"signal": "ISCHEMIA", "error": "Insufficient ATP in bloodstream."}

    def homeostatic_tick(self) -> Dict:
        """Adjusts heart rate (pulse frequency) based on system temperature."""
        # Check Immune Heat
        # (Simulation: Placeholder for real Immune/Metabolism feedback)
        return self.metabolism.tick()
