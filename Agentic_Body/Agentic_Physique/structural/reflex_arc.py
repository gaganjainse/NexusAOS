"""
SeshaAOS - Reflex Arc (The Spinal Cord)
Version: 1.0.0
Description: Fast-path, autonomic responses to critical stimuli. Bypasses high-level reasoning.
"""

from pathlib import Path
from typing import Optional
import sys
import time

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

from Agentic_Body.Agentic_Physique.nervous.signal_router import SignalRouter
from Agentic_Body.Agentic_Physique.metabolism_engine import MetabolismEngine
from Agentic_Body.Agentic_Soma.Foundation.dna.dna_manager import DNAManager
from Agentic_Body.Agentic_Physique.nervous.shm_bridge import SHMBridge

class ReflexArc:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.signals = SignalRouter(base_dir)
        self.metabolism = MetabolismEngine(base_dir)
        self.dna = DNAManager(base_dir)
        self.bus = SHMBridge()
        self.bus.connect()
        self.last_reflex = time.time()

    def _get_param(self, category: str, key: str, default: float) -> float:
        genome = self.dna.get_genome()
        return genome.get(category, {}).get(key, default)

    def check_reflexes(self) -> list[str]:
        """Runs the 'Fast Path' checks for all hard-wired instincts."""
        actions_taken = []
        
        # 1. Nociceptive Reflex (Pain/Error Response)
        res = self._check_nociception()
        if res: actions_taken.append(res)

        # 2. Respiratory Ventilation Reflex (Oxygen/Context Response)
        res = self._check_ventilation()
        if res: actions_taken.append(res)

        # 3. Metabolic Satiety Reflex (Hunger/Energy Response)
        res = self._check_metabolic_satiety()
        if res: actions_taken.append(res)

        # 4. Thermal Inflammation Reflex (Fever Response)
        res = self._check_thermal_inflammation()
        if res: actions_taken.append(res)
            
        return actions_taken

    def _check_nociception(self) -> str:
        """Detects 'Pain' (High Error Rates or Security Breach)."""
        active_signals = self.signals.get_active_signals()
        if "NOCICEPTION" in active_signals:
            # 1. High-speed kernel reflex (Sub-microsecond)
            self.bus.emit_spike("!", "NOCICEPTOR")
            
            # 2. Legacy signaling for swarm visibility
            self.signals.emit_signal(
                "QUARANTINE_TRIGGERED",
                {"reason": "Autonomic Nociception", "target": "ALL_NON_ESSENTIAL"},
                ttl_seconds=60,
                evidentiality="!" 
            )
            return "Nociceptive Reflex: High-speed SHM spike emitted. Quarantine applied."
        return None

    def _check_ventilation(self) -> str:
        """Detects 'Hypoxia' (Context Window Saturation)."""
        vitals = self.metabolism._report()
        threshold = self._get_param("reflex_parameters", "hypoxia_threshold", 20.0)
        if vitals.get("oxygen", 100) < threshold:
            self.signals.emit_signal(
                "HYPOXIA_ALERT",
                {"reason": "Context window saturation", "action": "COMPRESS_NOW"},
                ttl_seconds=120,
                evidentiality="!"
            )
            return "Respiratory Reflex: Hypoxia detected. Triggering ventilation."
        return None

    def _check_metabolic_satiety(self) -> str:
        """Detects 'Energy Depletion' (ATP below threshold)."""
        vitals = self.metabolism._report()
        threshold = self._get_param("reflex_parameters", "ischemia_threshold", 15.0)
        if vitals.get("atp", 100) < threshold:
            self.signals.emit_signal(
                "ISCHEMIA_WARNING",
                {"reason": "ATP Critical", "action": "THROTTLE_ALL_NON_VITAL"},
                ttl_seconds=300,
                evidentiality="!"
            )
            return "Metabolic Reflex: Energy critical. Throttling non-vital synapses."
        return None

    def _check_thermal_inflammation(self) -> str:
        """Detects 'Fever' (Thermal load above threshold)."""
        vitals = self.metabolism._report()
        threshold = self._get_param("reflex_parameters", "fever_threshold", 85.0)
        if vitals.get("heat", 0) > threshold:
            self.signals.emit_signal(
                "FEVER_DETECTED",
                {"reason": "Overheating", "action": "STAGGER_SYNAPSES"},
                ttl_seconds=600,
                evidentiality="!"
            )
            return "Thermal Reflex: Fever detected. Staggering execution to cool Soma."
        return None

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    arc = ReflexArc(base)
    print("Reflex Check:", arc.check_reflexes())
