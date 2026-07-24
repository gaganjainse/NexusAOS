"""
AOS Hook Bridge — connects Cursor lifecycle hooks to the biological runtime.
"""
import json
import sys
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent


def main():
    hook_name = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    payload = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}

    from layers.L08_Governance.physiological_gate import PhysiologicalGate
    from layers.L01_Planning.orchestrator_engine import OrchestratorEngine
    from layers.L07_Integration.Sesha_senses import SeshaSenses

    result = {"hook": hook_name, "action": "continue"}

    if hook_name == "beforeSubmitPrompt":
        gate = PhysiologicalGate(BASE)
        report = gate.get_dampening_report()
        if report["threat_level"] == "Sepsis":
            result["action"] = "block"
            result["reason"] = "AOS in Sepsis state — physiological emergency."

    elif hook_name == "afterFileEdit":
        senses = SeshaSenses(BASE)
        senses.poll()

    elif hook_name == "stop":
        orch = OrchestratorEngine(BASE)
        orch.submit_directive("consolidate memory if history >= 10 tasks", priority=3)

    print(json.dumps(result))


if __name__ == "__main__":
    main()

