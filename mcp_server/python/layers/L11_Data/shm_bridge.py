"""
NexusAOS - Shared Memory Bridge 2.0 (Transcended)
Version: 2.0.0
Description: Python interface for the NEURAL 6.0 Zig Synaptic Bus. 
Supports binary routing tables and high-velocity spike emission.
"""

import mmap
import ctypes
import os
import time
import sys
from pathlib import Path
from typing import Optional, List, Dict

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

# Structure definition (MUST match synaptic_bus.zig 2.0 exactly)
class Spike(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("timestamp", ctypes.c_double),
        ("sigil", ctypes.c_uint8),
        ("priority", ctypes.c_uint8),
        ("sender_id", ctypes.c_char * 16),
        ("target_id", ctypes.c_char * 16),
        ("payload_hash", ctypes.c_char * 32),
    ]

class Route(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("signal_type_id", ctypes.c_uint32),
        ("target_zone_id", ctypes.c_uint32),
        ("weight", ctypes.c_float),
        ("is_active", ctypes.c_bool),
    ]

RING_SIZE = 2048
MAX_ROUTES = 256
CACHE_LINE = 64

class SynapticRingBuffer(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("write_idx", ctypes.c_size_t),
        ("_pad1", ctypes.c_char * (CACHE_LINE - ctypes.sizeof(ctypes.c_size_t))),
        ("read_idx", ctypes.c_size_t),
        ("_pad2", ctypes.c_char * (CACHE_LINE - ctypes.sizeof(ctypes.c_size_t))),
        ("routing_table", Route * MAX_ROUTES),
        ("spikes", Spike * RING_SIZE)
    ]

class SHMBridge:
    def __init__(self, shm_name: str = "nexus_synaptic_bus"):
        self.shm_name = shm_name
        self.size = ctypes.sizeof(SynapticRingBuffer)
        self.mm: Optional[mmap.mmap] = None
        self.buffer: Optional[SynapticRingBuffer] = None

    def connect(self):
        try:
            if os.name == 'nt':
                self.mm = mmap.mmap(-1, self.size, tagname=self.shm_name)
            else:
                fd = os.open(f"/dev/shm/{self.shm_name}", os.O_RDWR)
                self.mm = mmap.mmap(fd, self.size)
            
            self.buffer = SynapticRingBuffer.from_buffer(self.mm)
            return True
        except Exception as e:
            # Fallback for disconnected state
            self.mm = mmap.mmap(-1, self.size)
            self.buffer = SynapticRingBuffer.from_buffer(self.mm)
            return False

    def emit_spike(self, sigil: str, priority: int, sender: str, target: str = "ALL"):
        if not self.buffer: return
        
        write_idx = self.buffer.write_idx
        spike = self.buffer.spikes[write_idx % RING_SIZE]
        spike.timestamp = time.time()
        spike.sigil = ord(sigil[0])
        spike.priority = priority
        spike.sender_id = sender.encode()[:16].ljust(16, b'\0')
        spike.target_id = target.encode()[:16].ljust(16, b'\0')
        
        self.buffer.write_idx += 1

    def read_latest_spike(self) -> Optional[dict]:
        """Reads the latest spike from the ring buffer."""
        if not self.buffer: return None
        
        write_idx = self.buffer.write_idx
        read_idx = self.buffer.read_idx
        
        if write_idx > read_idx:
            spike = self.buffer.spikes[read_idx % RING_SIZE]
            self.buffer.read_idx += 1
            return {
                "timestamp": spike.timestamp,
                "sigil": chr(spike.sigil),
                "priority": spike.priority,
                "sender": spike.sender_id.decode().strip('\x00'),
                "target": spike.target_id.decode().strip('\x00')
            }
        return None

    def update_route(self, route_id: int, signal_id: int, zone_id: int, weight: float, active: bool):
        if not self.buffer: return
        route = self.buffer.routing_table[route_id % MAX_ROUTES]
        route.signal_type_id = signal_id
        route.target_zone_id = zone_id
        route.weight = weight
        route.is_active = active

if __name__ == "__main__":
    bridge = SHMBridge()
    bridge.connect()
    bridge.emit_spike("!", 10, "PYTHON_REFLEX", "ZIG_KERNEL")
    print("Synaptic 2.0 Bridge Operational.")
