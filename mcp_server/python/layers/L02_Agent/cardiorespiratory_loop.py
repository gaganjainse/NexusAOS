"""
SeshaAOS - Cardiorespiratory Loop
Version: 15.0.0
Description: Manages Context Ventilation (Respiratory) and ATP Distribution (Circulatory) with Metabolism feedback.
"""

import sys
import time
from pathlib import Path
from typing import Dict

try:
    from layers.L02_Agent.metabolism_engine import MetabolismEngine
except ImportError:
    # Fallback for testing/standalone
    class MetabolismEngine:
        def __init__(self, bd): pass
        def allocate_context_window(self, s): return {"allowed": True, "remaining_oxygen": 95}
        def consume_energy(self, a): return {"allowed": True, "remaining_atp": 80}
        def tick(self): return {"vitals": "stable"}

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class CardiorespiratoryLoop:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.metabolism = MetabolismEngine(base_dir)
        self.last_breath = time.time()

    def ventilate_context(self, current_context_size: int) -> Dict:
        """Checks context window 'oxygen' levels and triggers compression if needed."""
        res = self.metabolism.allocate_context_window(current_context_size)
        if not res.get("allowed"):
            return {
                "signal": "HYPOXIA",
                "action": "COMPRESS_CONTEXT",
                "message": "Oxygen low. Immediate context ventilation required."
            }
        return {"signal": "STABLE_BREATHING", "oxygen": res.get("remaining_oxygen")}

    def distribute_atp(self, agent_id: str, amount: float) -> Dict:
        """Pumps energy units to a specific agent in the swarm."""
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
        """Adjusts pulse frequency based on metabolic feedback and external heat."""
        vitals = self.metabolism.tick()
        # Hebbian feedback: if energy is low, increase heart rate to pump more, 
        # but if heat is high, slow down (Vasodilation/Cooling).
        if vitals.get("atp_level", 100) < 20:
             vitals["pulse_adjustment"] = "ACCELERATE"
        elif vitals.get("heat_index", 40) > 60:
             vitals["pulse_adjustment"] = "DECELERATE"
        else:
             vitals["pulse_adjustment"] = "STABLE"
             
        return vitals
