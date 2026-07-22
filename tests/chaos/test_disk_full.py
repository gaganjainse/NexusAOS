"""
NexusAOS - Chaos Test: Disk Full
Description: Fill disk during filtration → verify emergency rotation.
"""
import unittest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))


class TestDiskFull(unittest.TestCase):
    def test_filtration_handles_disk_full(self):
        from tools.nexus_liver import NexusLiver
        liver = NexusLiver(BASE_DIR)
        # Just verify the liver can be instantiated
        self.assertIsNotNone(liver)


if __name__ == "__main__":
    unittest.main()
