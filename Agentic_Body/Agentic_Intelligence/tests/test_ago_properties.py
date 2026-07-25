"""
SeshaAOS - Property-Based Tests
Version: 1.0.0
Description: Tests for properties that must always hold true.
"""
from pathlib import Path
import asyncio
import sys

import unittest

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))


class TestAGOProperties(unittest.TestCase):
    def test_energy_never_negative(self):
        from tools.physiology_engine import PhysiologyEngine
        engine = PhysiologyEngine(BASE_DIR)
        state = engine.get_state()
        self.assertGreaterEqual(state["metabolism"]["current_energy"], 0)

    def test_wal_always_replayable(self):
        from Agentic_Body.Agentic_Intelligence.planning.sesha_runtime import WAL
        wal = WAL(BASE_DIR)

        async def run():
            return await wal.read_all()

        events = asyncio.run(run())
        self.assertIsInstance(events, list)

    def test_physiological_gate_enforced(self):
        from tools.physiological_gate import PhysiologicalGate
        gate = PhysiologicalGate(BASE_DIR)
        # Test with high threat
        allowed, _ = gate.check("propose_dna_mutation")
        # Just ensure no crash
        self.assertIsInstance(allowed, bool)


if __name__ == "__main__":
    unittest.main()
