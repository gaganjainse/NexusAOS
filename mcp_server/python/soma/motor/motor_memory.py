"""
NexusAOS - Motor Memory (BSF - Binary Synaptic Format)
Version: 1.0.0
Description: Binary storage for procedural tool reliability and latency.
"""

import struct
import mmap
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Format: 16s (tool_id), f (reliability), f (avg_duration), I (total_calls)
TOOL_SLOT_FORMAT = "16sffI"
MAX_TOOLS = 128
BSF_MOTOR_FORMAT = f"<{TOOL_SLOT_FORMAT * MAX_TOOLS}"

class MotorMemory:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.bin_path = base_dir / "active_core" / "monitoring_active" / "motor_procedural.bsf"
        self.size = struct.calcsize(BSF_MOTOR_FORMAT)
        self.mm: Optional[mmap.mmap] = None
        self._ensure_file()

    def _ensure_paths(self):
        if not self.bin_path.parent.exists():
            self.bin_path.parent.mkdir(parents=True, exist_ok=True)

    def _ensure_file(self):
        self._ensure_paths()
        if not self.bin_path.exists():
            with open(self.bin_path, "wb") as f:
                f.write(b'\0' * self.size)

    def connect(self):
        fd = os.open(self.bin_path, os.O_RDWR)
        self.mm = mmap.mmap(fd, self.size)
        return self.mm

    def record_performance(self, tool_id: str, success: bool, duration: float):
        """Direct binary update of procedural memory."""
        if not self.mm: self.connect()
        
        # 1. Find or Allocate Slot (Simulated simple hashing)
        slot_idx = hash(tool_id) % MAX_TOOLS
        offset = slot_idx * struct.calcsize(TOOL_SLOT_FORMAT)
        
        self.mm.seek(offset)
        raw = self.mm.read(struct.calcsize(TOOL_SLOT_FORMAT))
        tid, rel, avg_dur, count = struct.unpack(f"<{TOOL_SLOT_FORMAT}", raw)
        
        # 2. Update Stats
        new_count = count + 1
        new_rel = (rel * count + (1.0 if success else 0.0)) / new_count
        new_dur = (avg_dur * count + duration) / new_count
        
        # 3. Write Back
        self.mm.seek(offset)
        self.mm.write(struct.pack(f"<{TOOL_SLOT_FORMAT}", tool_id.encode()[:16].ljust(16, b'\0'), new_rel, new_dur, new_count))

    def get_reliability(self, tool_id: str) -> float:
        if not self.mm: self.connect()
        slot_idx = hash(tool_id) % MAX_TOOLS
        offset = slot_idx * struct.calcsize(TOOL_SLOT_FORMAT)
        self.mm.seek(offset)
        raw = self.mm.read(struct.calcsize(TOOL_SLOT_FORMAT))
        _, rel, _, _ = struct.unpack(f"<{TOOL_SLOT_FORMAT}", raw)
        return rel if rel > 0 else 1.0

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    mm = MotorMemory(base)
    mm.record_performance("web_search", True, 0.5)
    print("Web Search Reliability:", mm.get_reliability("web_search"))
