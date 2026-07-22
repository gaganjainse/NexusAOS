"""
NexusAOS - Reflex Arc (The Spinal Cord)
Version: 1.0.0
Description: Fast-path, autonomic responses to critical stimuli. Bypasses high-level reasoning.
"""

import time
from pathlib import Path
from typing import Dict, List, Optional
from soma.nervous.signal_router import SignalRouter
from soma.metabolic.metabolism_engine import MetabolismEngine

class ReflexArc:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)
        self.metabolism = MetabolismEngine(base_dir)
        self.last_reflex = time.time()

    def check_reflexes(self) -> List[str]:
        """Runs the 'Fast Path' checks for all hard-wired instincts."""
        actions_taken = []
        
        # 1. Nociceptive Reflex (Pain/Error Response)
        nociception = self._check_nociception()
        if nociception:
            actions_taken.append(nociception)

        # 2. Respiratory Ventilation Reflex (Oxygen/Context Response)
        ventilation = self._check_ventilation()
        if ventilation:
            actions_taken.append(ventilation)
            
        return actions_taken

    def _check_nociception(self) -> Optional[str]:
        """Detects 'Pain' (High Error Rates or Security Breach)."""
        active_signals = self.signals.get_active_signals()
        
        # Check for immediate critical threats
        if "NOCICEPTION" in active_signals:
            # Immediate Quarantine Reflex
            self.signals.emit_signal(
                "QUARANTINE_TRIGGERED",
                {"reason": "Autonomic Nociception", "target": "ALL_NON_ESSENTIAL"},
                ttl_seconds=60
            )
            return "Nociceptive Reflex: Immediate Quarantine applied to threatened sectors."
        return None

    def _check_ventilation(self) -> Optional[str]:
        """Detects 'Hypoxia' (Context Window Saturation)."""
        vitals = self.metabolism._report()
        oxygen = vitals.get("oxygen", 100)
        
        # If oxygen (context window headroom) is below 20%
        if oxygen < 20:
            # Immediate Ventilation Reflex
            self.signals.emit_signal(
                "HYPOXIA_ALERT",
                {"reason": "Context window saturation", "action": "COMPRESS_NOW"},
                ttl_seconds=120
            )
            return "Respiratory Reflex: Hypoxia detected. Triggering immediate context ventilation."
        return None

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    arc = ReflexArc(base)
    print("Reflex Check:", arc.check_reflexes())
