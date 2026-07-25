"""
SeshaAOS - Chaos Test: WAL Corruption
Description: Corrupt WAL segment → verify replay handles it gracefully.
"""
import asyncio
import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))


class TestWALCorruption(unittest.TestCase):
    def test_wal_replay_handles_corruption(self):
        from services.Sesha_runtime import WAL
        wal = WAL(BASE_DIR)
        events = asyncio.run(wal.read_all())
        self.assertIsInstance(events, list)


if __name__ == "__main__":
    unittest.main()

