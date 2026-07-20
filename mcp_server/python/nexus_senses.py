"""
Nexus Corporate OS - Sensory Service (Streaming Nerves)
Version: 1.0.0
Description: Continuous background perception loop for real-time filesystem events.
"""

import time
from pathlib import Path

from tools.nexus_senses import NexusSenses
from tools.physiology_engine import PhysiologyEngine
from tools.signal_router import SignalRouter
from tools.service_heartbeat import ServiceHeartbeat

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SENSES = NexusSenses(BASE_DIR)
PHYSIOLOGY = PhysiologyEngine(BASE_DIR)
SIGNALS = SignalRouter(BASE_DIR)
HEARTBEAT = ServiceHeartbeat(BASE_DIR, "senses")


def sensory_loop():
    print("--- Nexus Senses LIVE (Streaming Nerves Active) ---")
    print(f"Watching: {SENSES.get_status()['watch_paths']}")

    while True:
        state = PHYSIOLOGY.get_state()
        met_status = state["metabolism"]["status"]

        if met_status == "Critical":
            print("Senses: Energy CRITICAL. Perception suspended.")
            time.sleep(60)
            continue

        wait_time = 2 if met_status == "Healthy" else 10

        events = SENSES.poll()
        if events:
            critical = [e for e in events if e["salience"] == "critical"]
            high = [e for e in events if e["salience"] == "high"]
            print(f"Senses: {len(events)} event(s) detected ({len(critical)} critical, {len(high)} high).")
            for e in events:
                print(f"  [{e['event_type']}] {e['path']} -> {e['signal_emitted'] or 'log only'}")
            PHYSIOLOGY.consume_energy(5 * len(events))

            if critical:
                SIGNALS.emit_signal("ADRENALINE", {"event": "Nociception triggered"}, ttl_seconds=300)

        HEARTBEAT.beat("alive", {"events": len(events), "mode": met_status})
        time.sleep(wait_time)


if __name__ == "__main__":
    sensory_loop()
