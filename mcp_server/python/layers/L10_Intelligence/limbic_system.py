"""
SeshaAOS - Limbic System (Emotional Intelligence)
Version: 1.0.0
Description: Manages complex emotional states (Fear, Anger, Joy) that bias the Mind's decisions.
Biological analog: Amygdala, Hippocampus, Hypothalamus (The emotional brain).
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from layers.L12_Infrastructure.dna_manager import DNAManager
from layers.L11_Data.signal_router import SignalRouter

class LimbicSystem:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.dna = DNAManager(base_dir)
        self.signals = SignalRouter(base_dir)
        self.state_path = base_dir / "active_core" / "monitoring_active" / "limbic_state.json"
        self._init_state()

    def _init_state(self):
        if not self.state_path.exists():
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            initial = {
                "fear": 0.1,    # Response to Security/Nociception
                "anger": 0.1,   # Response to blockages/failures
                "joy": 0.5,     # Response to success/Sovereign praise
                "last_update": time.time()
            }
            self.state_path.write_text(json.dumps(initial, indent=4), encoding="utf-8")

    def process_stimulus(self) -> str:
        """Evaluates active signals and shifts the emotional state."""
        genome = self.dna.get_genome()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        active_signals = self.signals.get_active_signals()
        
        # 1. Fear Response (Security/Pain)
        if "NOCICEPTION" in active_signals or "QUARANTINE_TRIGGERED" in active_signals:
            state["fear"] = min(1.0, state["fear"] + 0.2)
            state["joy"] *= 0.8 # Fear dampens Joy
            
        # 2. Anger Response (Persistence/Blockage)
        if any("blocked" in str(s) for s in active_signals.values()):
            state["anger"] = min(1.0, state["anger"] + 0.15)
            
        # 3. Joy Response (Achievement)
        if "EVOLUTION_PROMOTION" in active_signals or "AIDE2_PLASTICITY_COMPLETE" in active_signals:
            state["joy"] = min(1.0, state["joy"] + 0.3)
            state["fear"] *= 0.5 # Joy suppresses Fear
            
        # 4. Basal Decay (Homeostasis)
        state["fear"] = max(0.1, state["fear"] * 0.95)
        state["anger"] = max(0.1, state["anger"] * 0.9)
        state["joy"] = max(0.1, state["joy"] * 0.98)
        
        state["last_update"] = time.time()
        self.state_path.write_text(json.dumps(state, indent=4), encoding="utf-8")
        
        # Emit 'Vibe' shift to Endocrine
        emotions = {k: v for k, v in state.items() if k != "last_update"}
        dominant = max(emotions, key=emotions.get)
        self.signals.emit_signal("VIBE_SHIFT", {"dominant": dominant, "scores": emotions}, evidentiality="◊")
        
        return f"Limbic Shift: Dominant emotion is {dominant.upper()}."

    def get_bias_weights(self) -> Dict[str, float]:
        """Returns weights to bias the Moral Cortex and Orchestrator."""
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        return {
            "caution": state["fear"] * 1.5,
            "persistence": state["anger"] * 1.2,
            "exploration": state["joy"] * 2.0
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent
    limbic = LimbicSystem(base)
    print(limbic.process_stimulus())
    print("Bias Weights:", limbic.get_bias_weights())

