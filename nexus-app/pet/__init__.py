"""
SeshaAOS - Pet Package
Version: 13.1.0
Description: 3D realistic human avatar serving as the visual representation of Sesha.
Integrates with AOS via PySide6 QWebEngineView + QWebChannel bridge.
Includes emergent consciousness engine and mood-aware voice synthesis.
"""

from .pet_bridge import PetBridge, PetJSSide
from .pet_engine import ConsciousnessEngine, EmergentState
from .pet_voice import PetVoiceEngine, VOICE_PARAMS

__all__ = [
    "PetBridge",
    "PetJSSide",
    "ConsciousnessEngine",
    "EmergentState",
    "PetVoiceEngine",
    "VOICE_PARAMS",
]

