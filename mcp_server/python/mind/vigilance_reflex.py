"""
NexusAOS - Vigilance Reflex (Hybrid Attentional Gating)
Version: 1.0.0
Description: Automatically manages the "Noise" level of the swarm based on Sovereign activity.
"""

import time
import asyncio
from pathlib import Path
from typing import List, Dict
from soma.nervous.signal_router import SignalRouter

class VigilanceReflex:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)
        self.last_sovereign_pulse = time.time()
        self.is_vigilant = False
        
        # Attentional Tiers
        self.CRITICAL_SYSTEMS = ["immune", "nervous", "integumentary", "omni-lead", "signal_router"]
        self.HIGH_COST_SYSTEMS = ["researcher", "evolution", "motor", "reproductive", "digestive"]

    def trigger_pulse(self):
        """Called whenever the Sovereign interacts with the Mind."""
        self.last_sovereign_pulse = time.time()
        if not self.is_vigilant:
            self.is_vigilant = True
            self.signals.emit_signal(
                "VIGILANCE_HIGH", 
                {"reason": "Sovereign Interaction", "action": "HIBERNATE_NON_CRITICAL"},
                ttl_seconds=60
            )
            return "Vigilance High: Hibernating high-cost background synapses."
        return "Vigilance Maintained."

    def check_idle(self, idle_threshold: int = 300):
        """Checks if the Sovereign has been idle long enough to resume background growth."""
        if self.is_vigilant and (time.time() - self.last_sovereign_pulse > idle_threshold):
            self.is_vigilant = False
            self.signals.emit_signal(
                "VIGILANCE_LOW", 
                {"reason": "Sovereign Idle", "action": "WAKE_ALL"},
                ttl_seconds=300
            )
            return "Vigilance Low: Resuming full background swarm operations."
        return None

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    vr = VigilanceReflex(base)
    print(vr.trigger_pulse())
    print(vr.check_idle(0)) # Force wake
