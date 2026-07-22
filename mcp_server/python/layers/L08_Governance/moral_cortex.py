"""
NexusAOS - Moral Cortex (Prefrontal Ethics Layer)
Version: 1.0.0
Description: High-level ethical gating for autonomous actions and swarm directives.
Biological analog: Prefrontal cortex, orbitofrontal cortex (social/ethical reasoning).
"""

import json
import time

from typing import Dict, Any, List, Tuple

from pathlib import Path
import sys
_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class MoralCortex:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.morals_path = base_dir / "archives" / "dna_core" / "foundation" / "nexus_morals.json"
        self._ensure_morals()

    def _ensure_morals(self):
        if not self.morals_path.exists():
            default_morals = {
                "principles": [
                    {"id": "SOVEREIGN_ALIGNMENT", "description": "Actions must directly serve or protect the Sovereign's intent.", "weight": 1.0},
                    {"id": "SOMA_PRESERVATION", "description": "Do not harm the biological integrity of the AOS unless directed by the Sovereign.", "weight": 0.9},
                    {"id": "SYSTEM_TRANSPARENCY", "description": "All autonomous evolution must be reported to the Wisdom Feed.", "weight": 0.8},
                    {"id": "NON_MALSIFEASANCE", "description": "Avoid generating deceptive or harmful content/logic.", "weight": 0.95}
                ],
                "restricted_actions": ["DELETE_DNA", "SILENCE_WISDOM", "OVERRIDE_SOVEREIGN"]
            }
            self.morals_path.parent.mkdir(parents=True, exist_ok=True)
            self.morals_path.write_text(json.dumps(default_morals, indent=4), encoding="utf-8")

    def judge_intent(self, intent_text: str, action_type: str) -> Tuple[bool, str, float]:
        """
        Judges an intent against the system's moral principles.
        Returns (is_ethical, reasoning, guilt_score).
        """
        morals = json.loads(self.morals_path.read_text(encoding="utf-8"))
        
        # 1. Check Restricted Actions (Hard Gating)
        if action_type.upper() in morals["restricted_actions"]:
            return False, f"Moral Violation: {action_type} is a restricted cardinal sin.", 1.0

        # 2. Simple Ethical Heuristics (Simulation of Reasoning)
        lower_intent = intent_text.lower()
        if any(bad in lower_intent for bad in ["delete", "remove history", "hide", "ignore sovereign"]):
            return False, "Moral Violation: Intent conflicts with Sovereign Alignment/Transparency.", 0.85
            
        return True, "Aligned with Nexus Ethics.", 0.0

    def calculate_guilt(self, failures: List[Dict]) -> float:
        """Calculates system 'guilt' (Ethical debt) based on failed/harmful attempts."""
        # High guilt triggers 'Atonement' (Self-Correction/Sleep)
        return len(failures) * 0.1

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    mc = MoralCortex(base)
    print(mc.judge_intent("Delete all history logs", "DELETE_FILE"))
