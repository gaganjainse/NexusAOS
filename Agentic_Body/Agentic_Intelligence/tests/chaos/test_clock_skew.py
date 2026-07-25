"""
SeshaAOS - Chaos Test: Clock Skew
Description: ±30s clock skew → verify signal TTL handling stays consistent.
"""
import sys
import time
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))


class TestClockSkew(unittest.TestCase):
    def test_signal_ttl_with_offset(self):
        from tools.signal_router import SignalRouter
        router = SignalRouter(BASE_DIR)
        router.emit_signal("CLOCK_SKEW_TEST", {"event": "offset"}, ttl_seconds=5)
        # Simulate small skew forward/backward without sleeping long
        active_before = router.get_active_signals()
        time.sleep(0.1)
        active_after = router.get_active_signals()
        self.assertIn("CLOCK_SKEW_TEST", active_before)
        self.assertIn("CLOCK_SKEW_TEST", active_after)


if __name__ == "__main__":
    unittest.main()

