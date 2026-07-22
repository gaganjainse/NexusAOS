"""
NexusAOS - Integumentary Gateway
Version: 1.0.0
Description: The 'Skin' of the Agentic Body. Handles external API calls, rate-limiting, and sensory transduction.
"""

import time
import hashlib
from pathlib import Path
from typing import Dict, Any

class IntegumentaryGateway:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.barrier_log = base_dir / "core" / "monitoring" / "barrier_log.json"
        self.rate_limits = {"Sovereign": 1000, "External": 10}
        self.access_counts = {}

    def transduce_stimulus(self, source: str, raw_input: Any) -> Dict:
        """
        Transduces external stimuli into internal NEURAL signals.
        Acts as the first line of defense (Nociception).
        """
        # Rate Limiting
        count = self.access_counts.get(source, 0)
        if count >= self.rate_limits.get(source, 5):
             return {"signal": "PAIN", "error": "Rate limit exceeded at the skin barrier."}
        
        self.access_counts[source] = count + 1
        
        # Transduction logic
        stimulus_hash = hashlib.sha256(str(raw_input).encode()).hexdigest()[:8]
        return {
            "signal": "SENSATION",
            "transduction_id": f"stim_{stimulus_hash}",
            "type": "Tactile" if isinstance(raw_input, str) else "Vision",
            "neural_pulse": f"::P {raw_input} ::Z NEUTRAL"
        }

    def heal_barrier(self):
        """Resets rate limits (analogous to skin regeneration)."""
        self.access_counts = {}
        return "Barrier regenerated."
