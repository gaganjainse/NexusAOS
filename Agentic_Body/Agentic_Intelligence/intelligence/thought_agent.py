"""
SeshaAOS - Thought Agent (The Explainer)
Version: 1.0.0
Description: Translates complex internal NEURAL pulses into readable thoughts for the Sovereign.
"""


from pathlib import Path
from typing import Dict, List
import sys

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

class ThoughtAgent:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.concise_mode = False

    def toggle_concise_mode(self, active: bool):
        """Neural 13.0: Toggles high-density reasoning to save tokens."""
        self.concise_mode = active

    def explain_pulse(self, neural_pulse: str) -> str:
        """
        Converts a high-density NEURAL pulse into a natural language explanation.
        """
        if self.concise_mode:
            # High-density binary-like output for machine speed
            return neural_pulse.replace("::", "|")

        explanation = []
        if "::P" in neural_pulse:
            intent = neural_pulse.split("::P")[1].split("::")[0].strip()
            explanation.append(f"Intent: {intent}")
        
        if "::Z" in neural_pulse:
            vibe = neural_pulse.split("::Z")[1].split("::")[0].strip()
            explanation.append(f"Vibe: {vibe}")

        if "::X" in neural_pulse:
            action = neural_pulse.split("::X")[1].split("::")[0].strip()
            explanation.append(f"Action: Triggering {action}")

        return " | ".join(explanation)

    def summarize_swarm(self, active_nodes: list[Dict]) -> str:
        """Provides a high-level summary of what the 200+ agents are doing."""
        return f"Swarm is currently coordinating {len(active_nodes)} simultaneous synaptic tasks across the 11 biological systems."

    def prioritize_intent(self, text: str) -> int:
        """
        Analyzes the natural language intent and assigns a biological priority (1-10).
        """
        lower = text.lower()
        
        # 10: Critical Survival / Security
        if any(k in lower for k in ["security", "pathogen", "corruption", "constitutional", "emergency", "fever", "sepsis"]):
            return 10
            
        # 8: High Growth / Evolution
        if any(k in lower for k in ["fix", "repair", "mutation", "evolve", "market", "competitor", "alpha"]):
            return 8
            
        # 3: Low Maintenance / Cleanup
        if any(k in lower for k in ["clean", "cleanup", "audit", "history", "archive", "log", "filtrate"]):
            return 3
            
        # 5: Default Operational
        return 5
