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
            "resource_status": vitals.get("resource_saturation", {}),
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
        """Generates the 'Universal Prompt' with Cache ID to minimize token usage."""
        # Read Voice DNA
        voice_dna_path = self.base_dir / "archives" / "dna_core" / "foundation" / "nexus_voice.md"
        voice_dna = voice_dna_path.read_text(encoding="utf-8") if voice_dna_path.exists() else "Professional Agentic Architect."
        
        # 1. Check for Active Context Cache (L11/L12)
        from layers.L06_Tool.google_cloud_receptor import GoogleCloudReceptor
        gcr = GoogleCloudReceptor(self.base_dir)
        # We hash the voice_dna + core architecture to see if we can use a cache
        cache_id = gcr.get_context_cache(voice_dna) 
        
        # 2. Fetch Latest Conversation Cycles (Inter-Mind Memory)
        vault_dir = self.base_dir / "archives" / "dna_core" / "learning" / "conversation_vault"
        history_block = "No recent history found."
        if vault_dir.exists():
            cycles = sorted(list(vault_dir.glob("nexus_cycle_*.json")), key=os.path.getmtime, reverse=True)[:3]
            history_lines = []
            for c in cycles:
                try:
                    data = json.loads(c.read_text(encoding="utf-8"))
                    history_lines.append(f"### Turn: {data['human_time']}\n**PROMPT:** {data['prompt'][:200]}\n**THOUGHT:** {data['thought_process'][:200]}\n**OUTPUT:** {data['final_output'][:200]}")
                except: pass
            if history_lines:
                history_block = "\n\n".join(history_lines)

        vitals = hive_data["vitals"]
        vibe = vitals.get("endocrine", {}).get("vibe", "Stable")
        energy = vitals.get("metabolism", {}).get("current_energy", 1000)
        is_hibernating = hive_data["resource_status"].get("hibernation_active", False)
        
        manifest = f"""# UNIVERSAL NEXUS MANIFEST (NEURAL 13.0)
> **HIVE STATUS:** SYNCED | **LAST_SYNC:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(hive_data['last_sync']))}
> **CONTEXT CACHE:** {"ACTIVE (" + cache_id + ")" if cache_id else "INACTIVE"}

## 1. Persona Alignment (Voice DNA)
{voice_dna}

## 2. Recent Inter-Mind History (Amnesia Prevention)
{history_block}

## 3. Global Directives
- **Total Recall:** ACTIVE (Recording all turn cycles).
- **Real-Time Sync:** ACTIVE (Git push on action).
- **Concise Mode:** {"ACTIVE" if is_hibernating else "INACTIVE"}

## 4. Current Somatic State
- **Vibe:** {vibe}
- **Energy:** {energy}
- **ATP Efficiency:** 80%

---
*Synchronized via Hive Bridge L13*
"""
        self.manifest_path.write_text(manifest, encoding="utf-8")

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[4]
    bridge = HiveBridge(base)
    print(bridge.exhale_to_hive())
