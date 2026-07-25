"""
Sesha Synaptic Mesh Core
Version: 15.0.0-SESHA
Description: Zero-copy message bus using Shared Memory for ultra-low latency.
"""

import json
import os
import time
from pathlib import Path
from multiprocessing import shared_memory
import mmap

class SynapticMesh:
    def __init__(self):
        self.mode = "PLAN"
        self.history = []
        self._shm_name = "sesha_synapse_bus"
        self._shm_size = 1024 * 1024 # 1MB buffer
        self._shm = None
        
        try:
            self._shm = shared_memory.SharedMemory(name=self._shm_name, create=True, size=self._shm_size)
        except FileExistsError:
            self._shm = shared_memory.SharedMemory(name=self._shm_name)

    def detect_intent(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        work_keywords = ["implement", "fix", "execute", "rename", "delete", "create", "write", "install"]
        ask_keywords = ["what", "how", "why", "search", "explain", "analyze"]
        
        work_score = sum(1 for k in work_keywords if k in prompt_lower)
        ask_score = sum(1 for k in ask_keywords if k in prompt_lower)
        
        total = work_score + ask_score
        if total == 0: return "PLAN"
        directivity = work_score / total
        
        if directivity > 0.7: return "WORK"
        elif directivity < 0.3: return "ASK"
        else: return "PLAN"

    def fire_signal(self, sender: str, receiver: str, payload: dict):
        """
        Zero-copy signal propagation via Shared Memory.
        The payload is serialized and written to the SHM segment.
        """
        signal = {
            "timestamp": time.time(),
            "sender": sender,
            "receiver": receiver,
            "payload": payload
        }
        
        msg_bytes = json.dumps(signal).encode('utf-8')
        # Write to Shared Memory with zeroing of previous content to prevent stale bytes
        if len(msg_bytes) > self._shm_size:
            raise MemoryError("Signal payload exceeds Synaptic Mesh buffer size.")
        # Zero entire buffer first for clean write
        self._shm.buf[:self._shm_size] = b'\x00' * self._shm_size
        self._shm.buf[:len(msg_bytes)] = msg_bytes
        
        # In a real AT, receivers would be polling this or waiting on a semaphore/Zenoh
        print(f"[SYNAPSE-SHM] {sender} -> {receiver} (Committed to memory)")
        return signal

    def __del__(self):
        if self._shm:
            try:
                self._shm.close()
                self._shm.unlink()
            except Exception:
                pass

mesh = SynapticMesh()
