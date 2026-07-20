"""
Nexus Corporate OS - Orchestrator Service (The CPU Loop)
Version: 1.0.0
Description: Always-on autonomous decision loop. Closes senses -> motor -> memory.
"""

import time
from pathlib import Path

from tools.orchestrator_engine import OrchestratorEngine
from tools.physiology_engine import PhysiologyEngine
from tools.service_heartbeat import ServiceHeartbeat

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ORCHESTRATOR = OrchestratorEngine(BASE_DIR)
PHYSIOLOGY = PhysiologyEngine(BASE_DIR)
HEARTBEAT = ServiceHeartbeat(BASE_DIR, "orchestrator")


def orchestrator_loop():
    print("--- Nexus Orchestrator LIVE (CPU Loop Active) ---")
    print("Closed loop: Senses -> Decision -> Lattice -> Motor -> Memory")

    while True:
        state = PHYSIOLOGY.get_state()
        met_status = state["metabolism"]["status"]

        if met_status == "Critical":
            HEARTBEAT.beat("suspended", {"reason": "energy_critical"})
            print("Orchestrator: Energy CRITICAL. CPU loop suspended.")
            time.sleep(30)
            continue

        wait_time = 3 if met_status == "Healthy" else 10

        try:
            results = ORCHESTRATOR.tick()
            actions = (
                len(results.get("sensory", []))
                + len(results.get("signals", []))
                + len(results.get("directives", []))
                + len(results.get("maintenance", []))
            )
            if actions > 0:
                print(f"Orchestrator: Tick {results['tick']} | {actions} action(s)")
                for category in ("directives", "sensory", "signals", "maintenance"):
                    for item in results.get(category, []):
                        print(f"  [{category}] {item[:120]}")
            HEARTBEAT.beat("alive", {"tick": results.get("tick", 0), "actions": actions})
        except Exception as e:
            print(f"Orchestrator: Tick error: {e}")
            HEARTBEAT.beat("error", {"error": str(e)})

        time.sleep(wait_time)


if __name__ == "__main__":
    orchestrator_loop()
