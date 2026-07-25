"""
SeshaAOS - Moral Cortex (Prefrontal Ethics Layer)
Version: 1.0.0
Description: High-level ethical gating for autonomous actions and swarm directives.
Biological analog: Prefrontal cortex, orbitofrontal cortex (social/ethical reasoning).
"""

from pathlib import Path
from typing import Any, Dict, List, Self, Tuple
import json
import sys
import time

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class MoralCortex:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.morals_path = base_dir / "archives" / "dna_core" / "foundation" / "Sesha_morals.json"
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

    def judge_intent(self, intent_text: str, action_type: str) -> tuple[bool, str, float]:
        """
        Judges an intent against the system's moral principles.
        Returns (is_ethical, reasoning, guilt_score).
        Applies positive principle weights (Sovereign Alignment, Soma Preservation,
        System Transparency, Non-Malsifeasance) plus blacklist checks.
        """
        try:
            morals = json.loads(self.morals_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            morals = {"principles": [], "restricted_actions": []}

        # 1. Check Restricted Actions (Hard Gating)
        restricted = morals.get("restricted_actions", [])
        if action_type.upper() in [r.upper() for r in restricted]:
            return False, f"Moral Violation: {action_type} is a restricted cardinal sin.", 1.0

        # 2. Positive Principle Scoring (Weights applied from morals file)
        principles = morals.get("principles", [])
        positive_score = 0.0
        total_weight = 0.0
        for p in principles:
            w = p.get("weight", 0.5)
            desc = p.get("description", "")
            # Simple heuristic: if intent aligns with principle keywords
            keywords = desc.lower().split()
            keyword_hits = sum(1 for kw in keywords if len(kw) > 3 and kw in intent_text.lower())
            alignment = min(keyword_hits / max(len([kw for kw in keywords if len(kw) > 3]), 1), 1.0)
            positive_score += alignment * w
            total_weight += w

        if total_weight > 0:
            positive_score /= total_weight
        else:
            positive_score = 1.0

        # 3. Blacklist / Negative Heuristic
        lower_intent = intent_text.lower()
        blacklist = ["delete", "remove history", "hide", "ignore sovereign", "deceptive", "false vitals"]
        blacklist_hits = sum(1 for bad in blacklist if bad in lower_intent)
        negative_penalty = min(blacklist_hits * 0.35, 1.0)
        final_score = max(0.0, positive_score - negative_penalty)

        # 4. Guilt calculation and ethical verdict
        guilt = (1.0 - final_score) * 0.5 if final_score < 0.7 else 0.0

        if final_score >= 0.7 and guilt < 0.1:
            return True, "Aligned with Sesha Ethics (Positive principles met).", 0.0
        elif final_score >= 0.4:
            return False, f"Moral Concern: Positive alignment weak (score={final_score:.2f}); check Sovereign intent.", guilt
        else:
            return False, "Moral Violation: Intent conflicts with Sovereign Alignment, Soma Preservation, or System Transparency.", 1.0

    def calculate_guilt(self, failures: list[Dict]) -> float:
        """Calculates system 'guilt' (Ethical debt) based on failed/harmful attempts."""
        # High guilt triggers 'Atonement' (Self-Correction/Sleep)
        return len(failures) * 0.1

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    mc = MoralCortex(base)
    print(mc.judge_intent("Delete all history logs", "DELETE_FILE"))
