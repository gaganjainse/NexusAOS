"""
AOS Integration Test Suite
Run: python tests/test_aos_integration.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT / "mcp_server" / "python"
sys.path.insert(0, str(PYTHON_DIR))

PASSED = 0
FAILED = 0


def test(name: str, fn):
    global PASSED, FAILED
    try:
        fn()
        print(f"  PASS  {name}")
        PASSED += 1
    except Exception as e:
        print(f"  FAIL  {name}: {e}")
        FAILED += 1


def main():
    print("=== AOS Integration Tests ===\n")

    def t_physiology():
        from tools.physiology_engine import PhysiologyEngine
        e = PhysiologyEngine(ROOT)
        s = e.get_state()
        assert "metabolism" in s and "endocrine" in s and "immune" in s

    def t_gate():
        from tools.physiological_gate import PhysiologicalGate
        g = PhysiologicalGate(ROOT)
        allowed, _ = g.check("propose_dna_mutation")
        assert isinstance(allowed, bool)

    def t_senses():
        from tools.nexus_senses import NexusSenses
        s = NexusSenses(ROOT)
        s.poll()
        assert "watch_paths" in s.get_status()

    def t_motor():
        from tools.motor_engine import MotorEngine
        from tools.nexus_lattice import LatticeEngine
        lat = LatticeEngine(ROOT)
        motor = MotorEngine(ROOT)
        lat.fire_synapse("Test", "Motor", "MOTOR:write:core/monitoring/test_motor.tmp:test")
        results = motor.process_lattice_queue()
        assert len(results) >= 1
        (ROOT / "core/monitoring/test_motor.tmp").unlink(missing_ok=True)

    def t_orchestrator():
        from tools.orchestrator_engine import OrchestratorEngine
        o = OrchestratorEngine(ROOT)
        o.submit_directive("diagnose system", priority=5)
        tick = o.tick()
        assert "tick" in tick

    def t_antibody():
        from tools.antibody_engine import AntibodyEngine
        a = AntibodyEngine(ROOT)
        a.patrol()
        status = a.get_immune_cells_status()
        assert "wbc_count" in status

    def t_cellular():
        from tools.cellular_engine import CellularEngine
        r = CellularEngine(ROOT).full_cell_report()
        assert r["total_components"] >= 10

    def t_fission_fusion():
        from tools.fission_fusion_engine import FissionFusionEngine
        ff = FissionFusionEngine(ROOT)
        result = ff.fusion("hq", "core", "test_fusion_tmp")
        assert "FUSION OK" in result
        (ROOT / "core/pulses/test_fusion_tmp.nxp").unlink(missing_ok=True)

    def t_vision():
        from tools.vision_engine import VisionEngine
        v = VisionEngine(ROOT)
        r = v.analyze_image("core/monitoring/physiology.json")
        assert "error" in r or "size_bytes" in r

    def t_plugin_registry():
        sys.path.insert(0, str(ROOT / "plugins"))
        from plugin_registry import PluginRegistry
        status = PluginRegistry(ROOT).get_status()
        assert status["cursor_bridge"] is True

    def t_cursor_files():
        assert (ROOT / ".cursor/mcp.json").exists()
        assert (ROOT / ".cursor/hooks.json").exists()
        assert (ROOT / ".cursor/rules/aos-constitution.mdc").exists()

    def t_heartbeats():
        from tools.service_heartbeat import ServiceHeartbeat
        services = ServiceHeartbeat.all_services(ROOT)
        assert isinstance(services, list)

    tests = [
        ("Physiology Engine", t_physiology),
        ("Physiological Gate", t_gate),
        ("Sensory Engine", t_senses),
        ("Motor Engine", t_motor),
        ("Orchestrator Engine", t_orchestrator),
        ("Antibody Engine", t_antibody),
        ("Cellular Engine", t_cellular),
        ("Fission/Fusion Engine", t_fission_fusion),
        ("Vision Engine", t_vision),
        ("Plugin Registry", t_plugin_registry),
        ("Cursor Bridge Files", t_cursor_files),
        ("Service Heartbeats", t_heartbeats),
    ]

    for name, fn in tests:
        test(name, fn)

    print(f"\n=== Results: {PASSED} passed, {FAILED} failed ===")
    return FAILED == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
