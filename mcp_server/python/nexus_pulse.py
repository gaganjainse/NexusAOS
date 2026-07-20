"""
Nexus Corporate OS - Pulse (The Heart)
Version: 1.0.0
Description: Continuous background service for proactive intelligence and signaling.
"""

import time
import subprocess
import sys
from pathlib import Path
from tools.signal_router import SignalRouter
from tools.memory_synth import MemorySynth
from tools.physiology_engine import PhysiologyEngine
from tools.reproduction_engine import ReproductionEngine
from tools.nexus_liver import NexusLiver
from tools.service_heartbeat import ServiceHeartbeat

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PHYSIOLOGY = PhysiologyEngine(BASE_DIR)
SIGNALS = SignalRouter(BASE_DIR)
MEMORY = MemorySynth(BASE_DIR)
REPRODUCTION = ReproductionEngine(BASE_DIR)
LIVER = NexusLiver(BASE_DIR)
HEARTBEAT = ServiceHeartbeat(BASE_DIR, "pulse")

def heartbeat_loop():
    print("--- Nexus Pulse LIVE (Circulatory System Active) ---")

    cycle_count = 0

    while True:
        state = PHYSIOLOGY.get_state()
        met_status = state["metabolism"]["status"]

        if met_status == "Critical":
            print("Pulse: Energy CRITICAL. Heartbeat suspended.")
            time.sleep(300) # Sleep long to save resources
            continue

        # Determine frequency
        wait_time = 60 if met_status == "Healthy" else 300

        print(f"Pulse: Cycle {cycle_count} | Mode: {met_status}")

        # 1. Proactive Intelligence (Oracle)
        # Run every 5 cycles in Healthy mode, every 1 in Conserving (to keep flow but slow)
        intel_freq = 5 if met_status == "Healthy" else 1
        if cycle_count % intel_freq == 0:
            print("Pulse: Triggering Proactive Intelligence Scrape...")
            try:
                scraper_path = BASE_DIR / "mcp_server" / "python" / "oracle_scraper.py"
                if scraper_path.exists():
                    subprocess.run([sys.executable, str(scraper_path)], capture_output=True)
                    SIGNALS.emit_signal("GROWTH", {"event": "Intelligence Consolidated"}, ttl_seconds=3600)
                    # Cost of scrape
                    PHYSIOLOGY.consume_energy(500)
            except Exception as e:
                print(f"Pulse: Scrape Error: {e}")

        # 2. Metabolic Maintenance
        # Small cost for the heartbeat itself
        PHYSIOLOGY.consume_energy(10)

        # 3. Signal Decay / Cleanup
        active = SIGNALS.get_active_signals()
        if "ADRENALINE" in active:
            print("Pulse: [URGENT SIGNAL DETECTED] High activity mode active.")

        # 4. Endocrine Synthesis (Mood)
        # Run every 5 cycles
        if cycle_count % 5 == 0:
            vibe = PHYSIOLOGY.synthesize_vibe()
            print(f"Pulse: System Vibe is {vibe}.")
            SIGNALS.emit_signal("VIBE", {"vibe": vibe}, ttl_seconds=600)

        # 5. Deep Sleep (Memory Consolidation)
        # Run every 50 cycles (Standard)
        if cycle_count > 0 and cycle_count % 50 == 0:
            print("Pulse: Initiating Deep Sleep (Memory Consolidation)...")
            report = MEMORY.consolidate()
            print(f"Pulse: {report}")
            # Metabolic cost of dreaming
            PHYSIOLOGY.consume_energy(200)

            # 5.1 Evolutionary Mutation Check
            # Only if energy is high enough (>40%)
            met_state = PHYSIOLOGY.get_state()["metabolism"]
            if met_state["current_energy"] / met_state["max_energy"] > 0.4:
                print("Pulse: Checking for Genetic Drift / Protocol Shifts...")
                # In a real AGOI, this would trigger an LLM to propose a mutation.
                # For now, we emit a signal that the system is "Plastic" (ready to change).
                SIGNALS.emit_signal("GENETIC_PLASTICITY", {"status": "High"}, ttl_seconds=3600)

        # 6. Replication Check (Spawn Conditions)
        # Check every 20 cycles
        if cycle_count > 0 and cycle_count % 20 == 0:
            state = PHYSIOLOGY.get_state()
            met_state = state["metabolism"]
            vibe = state["endocrine"]["vibe"]
            wisdom = MEMORY.get_wisdom_summary()

            energy_pct = (met_state["current_energy"] / met_state["max_energy"]) * 100

            if energy_pct > 80 and vibe in ["Euphoric", "Stable"] and wisdom["total_memories"] >= 3:
                print("Pulse: [SYSTEM MATURE] Replication conditions met. Emitting signal.")
                SIGNALS.emit_signal("REPRODUCTION_READY", {"status": "Mature"}, ttl_seconds=3600)

        # 7. Filtration Cycle (The Liver)
        # Run every 100 cycles
        if cycle_count > 0 and cycle_count % 100 == 0:
            print("Pulse: Initiating Filtration Cycle (Cleaning the blood)...")
            report = LIVER.filter_toxins()
            print(f"Pulse: {report}")
            # Metabolic cost of filtration
            PHYSIOLOGY.consume_energy(100)

        # 8. Motor Agency (The Hand) — delegated to Orchestrator when running
        # Pulse no longer processes motor queue; Orchestrator owns the closed loop.

        cycle_count += 1
        HEARTBEAT.beat("alive", {"cycle": cycle_count, "mode": met_status})
        time.sleep(wait_time)

if __name__ == "__main__":
    heartbeat_loop()
