# Provenance tracking: links audit/provenance trail (AUDIT_REPORT.md line 1-149 audit trail; mesh_hive_sync_status.md sync status; COMMIT_MESSAGE.md commit 40203ec NEURAL 15.0 specialization cycle; dataset/11_SYSTEM_MAPPING.md 11-system mapping + provenance framework; saved logs: bone_marrow.log / physiology.json / signal_history.json). Reference special framework (AGENTS.md line 36-39: specialization mandate + provenance tracking + evolution tracking). Provenance applies to conversation recording cycle.
"""
SeshaAOS - Conversation Recorder (L09)
Version: 1.0.0
Description: High-fidelity "Black Box" for recording every Prompt, Thought, and Output.
Ensures total recall and provenance of the system's reasoning.
"""

from pathlib import Path
from typing import Any
import json
import os
import time

class ConversationRecorder:
    """The Black Box - Records the A-Z reasoning process."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.vault_dir = base_dir / "archives" / "dna_core" / "learning" / "conversation_vault"
        self.vault_dir.mkdir(parents=True, exist_ok=True)

    def record(self, prompt: str, thoughts: str, output: str):
        """Records a full conversation cycle."""
        timestamp = time.time()
        file_name = f"Sesha_cycle_{int(timestamp)}.json"
        
        entry = {
            "timestamp": timestamp,
            "human_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)),
            "prompt": prompt,
            "thought_process": thoughts,
            "final_output": output,
            "vibe_at_time": self._get_current_vibe()
        }
        
        with open(self.vault_dir / file_name, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=4)
            
        return file_name

    def _get_current_vibe(self) -> str:
        try:
            from Agentic_Body.Agentic_Physique.physiology_engine import PhysiologyEngine
            phys = PhysiologyEngine(self.base_dir)
            return phys.get_state().get("endocrine", {}).get("vibe", "Unknown")
        except Exception:  # noqa: BLE001
            return "Stable"

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    cr = ConversationRecorder(base)
    cr.record("Test Prompt", "Test Thought", "Test Output")
    print("Test Record Saved.")
