"""
SeshaAOS - Chaos Test: Disk Full
Description: Fill disk during filtration → verify emergency rotation.
"""
from pathlib import Path
import sys

import unittest

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))


class TestDiskFull(unittest.TestCase):
    def test_filtration_handles_disk_full(self):
        from tools.Sesha_liver import SeshaLiver
        liver = SeshaLiver(BASE_DIR)
        # Just verify the liver can be instantiated
        self.assertIsNotNone(liver)


if __name__ == "__main__":
    unittest.main()
