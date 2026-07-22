"""
NexusAOS - Thought Agent (The Explainer)
Version: 1.0.0
Description: Translates complex internal NEURAL pulses into readable thoughts for the Sovereign.
"""

from pathlib import Path
from typing import Dict, List

class ThoughtAgent:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def explain_pulse(self, neural_pulse: str) -> str:
        """
        Converts a high-density NEURAL pulse into a natural language explanation.
        Example: '::P fix file ::Z HIGH ::X auto_repair' -> 'I am prioritizing a critical file repair due to detected high-stress signals.'
        """
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

    def summarize_swarm(self, active_nodes: List[Dict]) -> str:
        """Provides a high-level summary of what the 200+ agents are doing."""
        return f"Swarm is currently coordinating {len(active_nodes)} simultaneous synaptic tasks across the 11 biological systems."
