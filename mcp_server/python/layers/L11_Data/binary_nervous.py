"""
NexusAOS - Binary Nervous System (BSF - Binary Synaptic Format)
Version: 1.0.0
Description: Zero-copy access to biological state using Python's buffer protocol.
Replaces legacy JSON state for high-frequency organs.
"""

import struct
import mmap
import os
import time
import sys
from pathlib import Path
from typing import Dict, Any, Optional

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

# BSF Genome Schema
# f: float32, I: uint32, d: double, Q: uint64, q: int64
BSF_GENOME_FORMAT = "<fffffIId" # 36 bytes

# NXP-B (Nexus Pulse Binary) Format
# Sigil (32 + 64 + 8) + topic_hash (8) + payload_len (8) = 120 bytes header
NXPB_HEADER_FORMAT = "<32s64sqQQ" 

class BinaryNervous:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.bin_dna_path = base_dir / "active_core" / "monitoring_active" / "evolution" / "dna.bsf"
        self.pulse_mesh_path = base_dir / "core" / "monitoring" / "pulse_mesh.nxpb"
        self.size = struct.calcsize(BSF_GENOME_FORMAT)
        self.mm: Optional[mmap.mmap] = None
        self._ensure_dna()
        self._ensure_mesh()

    def _ensure_dna(self):
        if not self.bin_dna_path.parent.exists():
            self.bin_dna_path.parent.mkdir(parents=True, exist_ok=True)
            
        if not self.bin_dna_path.exists():
            with open(self.bin_dna_path, "wb") as f:
                # Default DNA values
                data = struct.pack(BSF_GENOME_FORMAT, 
                                   0.8, 20.0, 15.0, 85.0, 0.5, 1, 0, float(time.time()))
                f.write(data)

    def _ensure_mesh(self):
        self.pulse_mesh_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.pulse_mesh_path.exists():
            with open(self.pulse_mesh_path, "wb") as f:
                f.write(b"\x00" * 1024 * 1024) # 1MB pre-allocated mesh buffer

    def transmit_binary_pulse(self, topic_hash: int, sigil_data: Dict, payload: bytes):
        """Neural 6.0: Transmits an NXP-B pulse via zero-copy mesh."""
        header = struct.pack(NXPB_HEADER_FORMAT,
            sigil_data["hw"].encode()[:32],
            sigil_data["sig"].encode()[:64],
            sigil_data["ts"],
            topic_hash,
            len(payload)
        )
        
        fd = os.open(self.pulse_mesh_path, os.O_RDWR)
        with mmap.mmap(fd, 0) as mm:
            # Atomic write to mesh (simulated)
            mm.write(header)
            mm.write(payload)
        os.close(fd)

    def connect(self):
        fd = os.open(self.bin_dna_path, os.O_RDWR)
        self.mm = mmap.mmap(fd, self.size)
        return self.mm

    def get_vitals(self) -> Dict[str, Any]:
        """Reads DNA vitals with direct slice."""
        if not self.mm: self.connect()
        
        self.mm.seek(0)
        unpacked = struct.unpack(BSF_GENOME_FORMAT, self.mm.read(self.size))
        return {
            "nociception_sensitivity": unpacked[0],
            "hypoxia_threshold": unpacked[1],
            "ischemia_threshold": unpacked[2],
            "fever_threshold": unpacked[3],
            "free_energy_threshold": unpacked[4],
            "generation": unpacked[5],
            "last_mutation": unpacked[7]
        }

    def mutate(self, index: int, new_val: float):
        """Mutates a specific genetic constant directly in the binary file."""
        if not self.mm: self.connect()
        
        self.mm.seek(0)
        vals = list(struct.unpack(BSF_GENOME_FORMAT, self.mm.read(self.size)))
        vals[index] = float(new_val)
        vals[5] += 1 # Generation++
        vals[7] = float(time.time())
        
        self.mm.seek(0)
        self.mm.write(struct.pack(BSF_GENOME_FORMAT, *vals))

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[3]
    bn = BinaryNervous(base)
    print("Initial Binary Vitals:", bn.get_vitals())
    bn.mutate(0, 0.9)
    print("Mutated Binary Vitals:", bn.get_vitals())
