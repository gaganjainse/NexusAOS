"""
Nexus Corporate OS - Supervisor (Autonomic Process Manager)
Version: 1.0.0
Description: Boots, monitors, and restarts all autonomic background services.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from tools.service_heartbeat import ServiceHeartbeat

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PYTHON_DIR = BASE_DIR / "mcp_server" / "python"

SERVICES = [
    {"name": "pulse", "script": "nexus_pulse.py", "stale_after": 360},
    {"name": "guardian", "script": "nexus_guardian.py", "stale_after": 30},
    {"name": "senses", "script": "nexus_senses.py", "stale_after": 25},
    {"name": "orchestrator", "script": "nexus_orchestrator.py", "stale_after": 20},
]

SUPERVISOR_STATE = BASE_DIR / "core" / "monitoring" / "supervisor_state.json"


def _load_state() -> dict:
    if SUPERVISOR_STATE.exists():
        try:
            with open(SUPERVISOR_STATE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"processes": {}, "restarts": {}}


def _save_state(state: dict):
    SUPERVISOR_STATE.parent.mkdir(parents=True, exist_ok=True)
    with open(SUPERVISOR_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)


def _start_service(script: str) -> int:
    script_path = PYTHON_DIR / script
    if not script_path.exists():
        return -1
    proc = subprocess.Popen(
        [sys.executable, str(script_path)],
        cwd=str(PYTHON_DIR),
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )
    return proc.pid


def boot_all() -> str:
    """Starts all autonomic services."""
    state = _load_state()
    report = ["--- Nexus Supervisor Boot ---"]

    for svc in SERVICES:
        pid = _start_service(svc["script"])
        state["processes"][svc["name"]] = {"pid": pid, "started_at": time.time(), "script": svc["script"]}
        status = f"PID {pid}" if pid > 0 else "FAILED"
        report.append(f"[BOOT] {svc['name']}: {status}")

    state["booted_at"] = time.time()
    _save_state(state)
    return "\n".join(report)


def supervisor_loop():
    print("--- Nexus Supervisor LIVE ---")
    print(boot_all())

    HEARTBEAT = ServiceHeartbeat(BASE_DIR, "supervisor")

    while True:
        state = _load_state()
        restarts = state.get("restarts", {})

        for svc in SERVICES:
            hb = ServiceHeartbeat(BASE_DIR, svc["name"])
            if hb.is_stale(svc["stale_after"]):
                print(f"Supervisor: {svc['name']} stale/missing. Restarting...")
                pid = _start_service(svc["script"])
                state["processes"][svc["name"]] = {"pid": pid, "started_at": time.time(), "script": svc["script"]}
                restarts[svc["name"]] = restarts.get(svc["name"], 0) + 1
                print(f"Supervisor: {svc['name']} restarted (PID {pid})")

        state["restarts"] = restarts
        state["last_check"] = time.time()
        _save_state(state)
        HEARTBEAT.beat("alive", {"services": len(SERVICES), "restarts": restarts})
        time.sleep(15)


if __name__ == "__main__":
    supervisor_loop()
