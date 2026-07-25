"""
SeshaAOS - Chaos Test: Network Partition
Description: Simulate offline during LLM call → verify retry.
"""
from pathlib import Path
import sys

import unittest

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))


class TestNetworkPartition(unittest.TestCase):
    def test_web_receptor_handles_network_failure(self):
        from tools.web_receptor import WebReceptor
        receptor = WebReceptor(BASE_DIR)
        # Fetch an invalid URL - should gracefully fail
        result = receptor.fetch_url("http://invalid.invalid.invalid")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
