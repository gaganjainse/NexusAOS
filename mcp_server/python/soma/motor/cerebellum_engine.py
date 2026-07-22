"""
NexusAOS - Cerebellum Engine (Motor Learning)
Version: 1.0.0
Description: Fine-tunes tool execution parameters based on repetition and performance.
Biological analog: Cerebellum (Procedural memory, timing, motor coordination).
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List

class CerebellumEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.procedural_path = base_dir / "active_core" / "monitoring_active" / "procedural_memory.json"
        self._ensure_memory()

    def _ensure_memory(self):
        if not self.procedural_path.exists():
            self.procedural_path.parent.mkdir(parents=True, exist_ok=True)
            self.procedural_path.write_text(json.dumps({"tool_sequences": {}}), encoding="utf-8")

    def record_action(self, tool_id: str, success: bool, duration: float):
        """Learns the performance profile of a tool."""
        with open(self.procedural_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            
            if tool_id not in data["tool_sequences"]:
                data["tool_sequences"][tool_id] = {"success_count": 0, "fail_count": 0, "avg_duration": duration}
                
            stats = data["tool_sequences"][tool_id]
            if success:
                stats["success_count"] += 1
            else:
                stats["fail_count"] += 1
                
            # Rolling average duration
            stats["avg_duration"] = (stats["avg_duration"] * 0.7) + (duration * 0.3)
            
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def get_efficiency_mod(self, tool_id: str) -> float:
        """Returns a latency multiplier based on tool reliability."""
        with open(self.procedural_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        stats = data["tool_sequences"].get(tool_id)
        if not stats: return 1.0
        
        reliability = stats["success_count"] / max(1, stats["success_count"] + stats["fail_count"])
        # High reliability = lower latency multiplier (faster execution)
        return max(0.5, 2.0 - reliability)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    cb = CerebellumEngine(base)
    cb.record_action("web_search", True, 1.2)
    print("Efficiency Mod:", cb.get_efficiency_mod("web_search"))
