"""
SeshaAOS - Salience Module
Version: 1.0.0
Description: Agent attention heuristic - cortisol elevates survival/priority signals.
"""
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent


class SalienceEngine:
    """Computes salience/priority for signals and tasks based on physiological state.
    
    High cortisol = survival priority elevation
    High adrenaline = immediate action priority
    Low energy = conserve/observe priority
    """
    
    def __init__(self, base_dir: Path, physiology_engine=None):
        self.base_dir = base_dir
        self.physiology = physiology_engine
        self.history: List[Dict] = []
        self.max_history = 200
    
    def _get_physiology(self):
        if self.physiology is None:
            from layers.L02_Agent.physiology_engine import PhysiologyEngine
            self.physiology = PhysiologyEngine(self.base_dir)
        return self.physiology
    
    def compute_signal_priority(self, signal_type: str, base_priority: int = 5, payload: Dict = None) -> Dict:
        """Compute effective priority for a signal based on current state."""
        state = self._get_physiology().get_state()
        hormones = state["endocrine"]["hormones"]
        cortisol = hormones.get("cortisol", 0.0)
        adrenaline = hormones.get("adrenaline", 0.0)
        serotonin = hormones.get("serotonin", 50.0)
        energy = state["metabolism"]["current_energy"]
        max_energy = state["metabolism"]["max_energy"]
        energy_pct = (energy / max_energy) * 100 if max_energy > 0 else 0
        threat = state["immune"]["threat_level"]
        
        # Base modifiers
        priority = base_priority
        modifiers = {}
        
        # Cortisol elevates NOCICEPTION/GROWTH/INFLAMMATION (survival signals)
        if signal_type in ("NOCICEPTION", "INFLAMMATION", "ADRENALINE") and cortisol >= 60.0:
            priority += 2
            modifiers["stress_boost"] = True
        elif cortisol >= 40.0:
            priority += 1
            modifiers["stress_boost"] = True
        
        # Adrenaline boosts motor/urgent actions
        if signal_type in ("ADRENALINE", "motor_priority", "motor_command") and adrenaline >= 20.0:
            priority += 3
            modifiers["adrenaline_boost"] = True
        
        # Low energy suppresses non-essential signals
        if energy_pct < 20:
            priority -= 2
            modifiers["energy_conservation"] = True
        elif energy_pct < 35:
            priority -= 1
            modifiers["energy_conservation"] = True
        
        # Fever/Sepsis elevates immune-related signals
        if threat in ("Fever", "Sepsis") and signal_type in ("NOCICEPTION", "heal", "filtrate"):
            priority += 2
            modifiers["immune_emergency"] = True
        
        # Clamp priority
        priority = max(1, min(10, priority))
        
        result = {
            "signal_type": signal_type,
            "base_priority": base_priority,
            "effective_priority": priority,
            "modifiers": modifiers,
            "context": {
                "cortisol": cortisol,
                "adrenaline": adrenaline,
                "energy_pct": energy_pct,
                "threat_level": threat
            },
            "timestamp": time.time()
        }
        
        self.history.append(result)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        return result
    
    def should_process_signal(self, signal_type: str, base_priority: int = 5) -> bool:
        """Decide whether a signal should be processed now based on salience."""
        computed = self.compute_signal_priority(signal_type, base_priority)
        return computed["effective_priority"] >= 3
    
    def get_top_signals(self, limit: int = 10) -> List[Dict]:
        """Get top priority signals from history."""
        return sorted(self.history, key=lambda x: -x["effective_priority"])[:limit]
    
    def explain_priority(self, signal_type: str, base_priority: int = 5) -> str:
        """Human-readable explanation of priority calculation."""
        computed = self.compute_signal_priority(signal_type, base_priority)
        parts = [f"{signal_type}: p{computed['base_priority']} -> p{computed['effective_priority']}"]
        ctx = computed["context"]
        parts.append(f"cortisol={ctx['cortisol']:.1f}, adrenaline={ctx['adrenaline']:.1f}")
        parts.append(f"energy={ctx['energy_pct']:.1f}%")
        if ctx["threat_level"] != "Negligible":
            parts.append(f"threat={ctx['threat_level']}")
        for mod, active in computed["modifiers"].items():
            if active:
                parts.append(f"+{mod}")
        return " | ".join(parts)

