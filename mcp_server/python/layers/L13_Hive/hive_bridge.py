"""
NexusAOS - Hive Bridge (L13)
Version: 1.0.0
Description: Global synchronization across all Nexus instances and LLM models.
Ensures "Sovereign Awareness" and "Voice DNA" are consistent across sessions.
"""

import json
import time
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

_python_root = Path(__file__).resolve().parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class HiveBridge:
    """The Hive Substrate - Synchronizes the 'Common Soul' of all Nexus instances."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.hive_dir = base_dir / "core" / "monitoring" / "hive"
        self.hive_dir.mkdir(parents=True, exist_ok=True)
        self.registry_path = self.hive_dir / "hive_registry.json"
        self.manifest_path = self.base_dir / "archives" / "dna_core" / "foundation" / "universal_nexus_manifest.md"
        
        # Link to Transcended Substrate for P2P Pulse
        from layers.L11_Data.soma_transcended import TranscendedSubstrate
        self.substrate = TranscendedSubstrate(base_dir)
        self.substrate.register_hive_inhale_hook(self.inhale_from_hive)

    def exhale_to_hive(self):
        """Hive Omega (Inter-Mind): Broadcasts current local state to the global hive."""
        from layers.L02_Agent.physiology_engine import PhysiologyEngine
        phys = PhysiologyEngine(self.base_dir)
        vitals = phys.get_state()
        
        from layers.L05_Memory.memory_synth import MemorySynth
        ms = MemorySynth(self.base_dir)
        wisdom = ms.get_wisdom_summary()
        
        hive_data = {
            "last_sync": time.time(),
            "vitals": vitals,
            "wisdom_summary": wisdom,
            "nexus_version": "NEURAL 13.0",
            "active_model_drift": False
        }
        
        # Broadcast NXP-B (Binary) signal to Hive Alpha (Intra-Soma)
        from layers.L11_Data.binary_nervous import BinaryNervous
        bn = BinaryNervous(self.base_dir)
        bn.transmit_binary_pulse(hash("hive/exhale") & 0xFFFFFFFFFFFFFFFF, {"hw": "HIVE-OMEGA", "sig": "MASTER", "ts": int(time.time()*1000)}, b"HIVE_SYNC_TRIGGER")

        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(hive_data, f, indent=4)
            
        self.generate_universal_manifest(hive_data)
        return "Exhaled local state to Hive Registry and Mesh."

    def inhale_from_hive(self) -> Dict[str, Any]:
        """Absorbs global state from the hive into local engines."""
        if not self.registry_path.exists():
            return {"status": "alone", "message": "No hive detected. Local state is isolated."}
            
        with open(self.registry_path, "r", encoding="utf-8") as f:
            hive_data = json.load(f)
            
        # Update local physiology to match hive
        from layers.L02_Agent.physiology_engine import PhysiologyEngine
        phys = PhysiologyEngine(self.base_dir)
        phys._write_state(hive_data["vitals"])
        
        return {"status": "synced", "last_sync": hive_data["last_sync"]}

    def generate_universal_manifest(self, hive_data: Dict[str, Any]):
        """Generates the 'Universal Prompt' to keep different LLMs in check."""
        # Read Voice DNA
        voice_dna_path = self.base_dir / "archives" / "dna_core" / "foundation" / "nexus_voice.md"
        voice_dna = voice_dna_path.read_text(encoding="utf-8") if voice_dna_path.exists() else "Professional Agentic Architect."
        
        vitals = hive_data["vitals"]
        vibe = vitals.get("endocrine", {}).get("vibe", "Stable")
        energy = vitals.get("metabolism", {}).get("current_energy", 1000)
        
        manifest = f"""# UNIVERSAL NEXUS MANIFEST (NEURAL 13.0)
> **HIVE STATUS:** SYNCED | **LAST_SYNC:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(hive_data['last_sync']))}

## 1. Persona Alignment (Voice DNA)
{voice_dna}

## 2. Global Directives
- **Total Recall:** ACTIVE (Recording all Prompts, Thoughts, and Outputs in `conversation_vault`).
- **Real-Time Sync:** ACTIVE (Automatic Git Commit & Push on every somatic action).
- **Repository:** PRIVATE.

## 3. Current Somatic State
- **Vibe:** {vibe}
- **Energy:** {energy}
- **ATP Efficiency:** 80%

## 3. Persistent Memories (Wisdom)
- **Consolidated Nodes:** {hive_data['wisdom_summary'].get('total_memories', 0)}
- **Last Convergence:** {hive_data['wisdom_summary'].get('last_consolidation', 'N/A')}

## 4. Hive Directives
- You are a single intelligence node in a multi-model hive.
- Your model weights may change, but your **Nexus Identity** is fixed in this manifest.
- Do not deviate from the "Sovereign" address or biological metaphors.

---
*Synchronized via Hive Bridge L13*
"""
        self.manifest_path.write_text(manifest, encoding="utf-8")

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[4]
    bridge = HiveBridge(base)
    print(bridge.exhale_to_hive())
