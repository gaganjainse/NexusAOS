"""
Nexus Corporate OS - Guardian Service
Version: 1.0.0
Description: Autonomous background service for real-time code compliance and self-healing.
"""

import os
import time
import subprocess
import sys
from pathlib import Path
from tools.auto_repair import AutoRepairEngine
from tools.physiology_engine import PhysiologyEngine
from tools.signal_router import SignalRouter

from tools.service_heartbeat import ServiceHeartbeat

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARE = AutoRepairEngine(BASE_DIR)
PHYSIOLOGY = PhysiologyEngine(BASE_DIR)
SIGNALS = SignalRouter(BASE_DIR)
HEARTBEAT = ServiceHeartbeat(BASE_DIR, "guardian")

def reforge_firmware():
    """Triggers the compiler and forge to sync pulses with markdown DNA."""
    print("Guardian: DNA change detected. Re-forging firmware...")
    try:
        # Run Compiler
        compiler_path = BASE_DIR / "mcp_server" / "python" / "nlg_compiler.py"
        subprocess.run([sys.executable, str(compiler_path)], check=True, capture_output=True)

        # Run Forge
        forge_path = BASE_DIR / "mcp_server" / "python" / "nxp_forge.py"
        subprocess.run([sys.executable, str(forge_path)], check=True, capture_output=True)

        print("Guardian: Firmware sync complete.")
    except Exception as e:
        print(f"Guardian: Sync error: {e}")

def monitor_loop():
    print(f"--- Nexus Guardian Service LIVE ---")
    print(f"Target: {BASE_DIR}")
    print("Action: Real-time autonomous file verification & DNA sync...")

    last_mtime = {}

    # Initial scan of archives to establish baseline
    archives_dir = BASE_DIR / "archives"

    def get_latest_archive_mtime():
        if not archives_dir.exists(): return 0
        mtimes = [f.stat().st_mtime for f in archives_dir.rglob("*.md")]
        return max(mtimes) if mtimes else 0

    last_archive_mtime = get_latest_archive_mtime()

    while True:
        # 0. Check Health (Immune Response)
        state = PHYSIOLOGY.get_state()
        health = state["immune"]
        threat = health["threat_level"]

        # Determine polling frequency based on "Body Temperature"
        if threat == "Sepsis": wait_time = 0.5
        elif threat == "Fever": wait_time = 1.0
        elif threat == "Inflammation": wait_time = 2.0
        else: wait_time = 5.0

        # 1. Critical Script Integrity
        critical_files = ["nexus_gui.py", "oracle_scraper.py", "nlg_compiler.py", "nxp_forge.py"]
        for f in critical_files:
            path = BASE_DIR / "mcp_server" / "python" / f
            if path.exists():
                mtime = path.stat().st_mtime
                if mtime != last_mtime.get(f):
                    print(f"Guardian: Change detected in {f}. Triggering ARE...")
                    report = ARE.scan_and_fix()
                    print(report)

                    if "[FIXED]" in report:
                        PHYSIOLOGY.register_anomaly(f"Unauthorized Edit: {f}", 1.5)
                        SIGNALS.emit_signal("INFLAMMATION", {"target": f}, ttl_seconds=300)
                    else:
                        PHYSIOLOGY.heal(0.1) # Natural healing if clean

                    last_mtime[f] = mtime

        # 2. DNA Monitoring (Archives)
        current_archive_mtime = get_latest_archive_mtime()
        if current_archive_mtime > last_archive_mtime:
            reforge_firmware()
            last_archive_mtime = current_archive_mtime

        # 3. Metabolic Monitoring
        met_status = state["metabolism"]["status"]
        if met_status == "Critical":
            print("Guardian [PAIN]: Metabolic Energy Critical! Initiating Emergency Conservation...")
            # Concept: In a real agentic loop, this would signal all agents to stop.
        elif met_status == "Conserving":
            print("Guardian [ALERT]: Energy Low. Shifting to Conservation Mode.")

        # 4. Heartbeat Monitoring (Pulse)
        # Check if nexus_pulse.py is running (simple check for demo)
        import subprocess
        try:
            # On Windows, use tasklist to check for the process
            output = subprocess.check_output('tasklist', shell=True).decode()
            if "python.exe" in output:
                # This is a bit weak because multiple python scripts might be running.
                # In a production OS, we'd check PID or use a lock file.
                pass
        except:
            pass

        # 5. Natural Healing
        # If the system remains healthy, temperature drops slowly
        if threat == "Negligible" and health["temperature"] > 98.6:
            PHYSIOLOGY.heal(0.01)

        HEARTBEAT.beat("alive", {"threat": threat, "wait": wait_time})
        time.sleep(wait_time)

if __name__ == "__main__":
    monitor_loop()
