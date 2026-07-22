"""
NexusAOS - Shared Memory Bridge
Version: 1.0.0
Description: Python interface for the Zig Synaptic Bus. 
Uses mmap and ctypes for sub-microsecond state access.
"""

import mmap
import ctypes
import os
import time
from pathlib import Path
from typing import Optional

# Structure definition (MUST match synaptic_bus.zig exactly)
class Spike(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("timestamp", ctypes.c_double),
        ("sigil", ctypes.c_uint8),
        ("sender_id", ctypes.c_char * 16),
        ("payload_hash", ctypes.c_char * 32),
    ]

RING_SIZE = 1024
CACHE_LINE = 64

class SynapticRingBuffer(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("write_idx", ctypes.c_size_t), # Atomic simulated via volatile-like access
        ("_pad1", ctypes.c_char * (CACHE_LINE - ctypes.sizeof(ctypes.c_size_t))),
        ("read_idx", ctypes.c_size_t),
        ("_pad2", ctypes.c_char * (CACHE_LINE - ctypes.sizeof(ctypes.c_size_t))),
        ("spikes", Spike * RING_SIZE)
    ]

class SHMBridge:
    def __init__(self, shm_name: str = "nexus_synaptic_bus"):
        self.shm_name = shm_name
        self.size = ctypes.sizeof(SynapticRingBuffer)
        self.mm: Optional[mmap.mmap] = None
        self.buffer: Optional[SynapticRingBuffer] = None

    def connect(self):
        """Connects to the Zig-managed shared memory."""
        try:
            if os.name == 'nt':
                # Windows Named Shared Memory
                self.mm = mmap.mmap(-1, self.size, tagname=self.shm_name)
            else:
                # Linux POSIX Shared Memory (/dev/shm)
                fd = os.open(f"/dev/shm/{self.shm_name}", os.O_RDWR)
                self.mm = mmap.mmap(fd, self.size)
            
            self.buffer = SynapticRingBuffer.from_buffer(self.mm)
            return True
        except Exception as e:
            print(f"SHM Bridge Connection Failed: {e}")
            # Fallback to local memory for simulation if Zig bus not running
            self.mm = mmap.mmap(-1, self.size)
            self.buffer = SynapticRingBuffer.from_buffer(self.mm)
            return False

    def read_latest_spike(self) -> Optional[dict]:
        if not self.buffer: return None
        
        write_idx = self.buffer.write_idx
        read_idx = self.buffer.read_idx
        
        if write_idx > read_idx:
            spike = self.buffer.spikes[read_idx % RING_SIZE]
            # Atomically increment read pointer (Python simulation)
            self.buffer.read_idx += 1
            return {
                "timestamp": spike.timestamp,
                "sigil": chr(spike.sigil),
                "sender": spike.sender_id.decode().strip('\x00')
            }
        return None

    def emit_spike(self, sigil: str, sender: str):
        """Emits a spike into the SHM bus."""
        if not self.buffer: return
        
        write_idx = self.buffer.write_idx
        spike = self.buffer.spikes[write_idx % RING_SIZE]
        spike.timestamp = time.time()
        spike.sigil = ord(sigil[0])
        spike.sender_id = sender.encode()[:16]
        
        self.buffer.write_idx += 1

if __name__ == "__main__":
    bridge = SHMBridge()
    bridge.connect()
    bridge.emit_spike("!", "PYTHON_REFLEX")
    print("Read Spike:", bridge.read_latest_spike())
