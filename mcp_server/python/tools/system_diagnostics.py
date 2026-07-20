"""
Nexus Corporate OS - System Diagnostics Tool
Version: 1.0.0
Description: Core logic for deep-dive environment analysis.
"""

import os
import json
import time
from pathlib import Path

def run_diagnostics(base_dir: Path) -> str:
    """Performs deep-dive logic verification."""
    results = ["--- Nexus OS Diagnostic Report ---"]

    # Check Data Integrity
    roles_dir = base_dir / "core" / "ui" / "nexus_dashboard" / "src" / "data" / "roles"
    results.append(f"Data Path: {roles_dir}")

    if not roles_dir.exists():
        results.append("[CRITICAL] Roles data directory is MISSING.")
        return "\n".join(results)

    index_path = roles_dir / "index.json"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            roles = json.load(f)
            results.append(f"[OK] index.json found with {len(roles)} roles.")

            # Check for orphaned roles or missing files
            missing_files = []
            for role in roles:
                role_id = role.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
                if not (roles_dir / f"{role_id}.json").exists():
                    missing_files.append(role)

            if missing_files:
                results.append(f"[WARNING] {len(missing_files)} roles in index lack matching JSON files.")
            else:
                results.append("[OK] All indexed roles have valid JSON targets.")
    else:
        results.append("[CRITICAL] index.json is MISSING.")

    # Check Scraper Data
    intel_path = base_dir / "archives" / "core" / "monitoring" / "scraped_data.json"
    if intel_path.exists():
        results.append(f"[OK] Intel data found ({intel_path.stat().st_size} bytes).")
    else:
        results.append("[WARNING] Scraped intelligence data not found.")

    # Check Lattice Proprioception
    lattice_path = base_dir / "core" / "monitoring" / "lattice_state.json"
    if lattice_path.exists():
        try:
            with open(lattice_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            active_count = len(state.get("active_tasks", {}))
            results.append(f"[OK] Lattice aware: {active_count} active firing nodes.")
        except:
            results.append("[ERROR] Lattice state file is corrupted.")
    else:
        results.append("[WARNING] Lattice state not initialized.")

    # Check Learning Depth (Wisdom)
    learning_dir = base_dir / "archives" / "core" / "learning"
    if learning_dir.exists():
        memories = list(learning_dir.glob("consolidation_*.md"))
        results.append(f"[OK] Learning Depth: {len(memories)} consolidated patterns.")
    else:
        results.append("[WARNING] Learning engine not initialized.")

    # Check Endocrine System (Mood)
    mood_path = base_dir / "core" / "monitoring" / "mood.json"
    if mood_path.exists():
        try:
            with open(mood_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            results.append(f"[OK] System Vibe: {data['vibe']} (Hormones: {list(data['hormones'].keys())})")
        except:
            results.append("[ERROR] Mood state file is corrupted.")
    else:
        results.append("[WARNING] Endocrine system not initialized.")

    # Check Immune System (Proactive Health)
    health_path = base_dir / "core" / "monitoring" / "health.json"
    if health_path.exists():
        try:
            with open(health_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            results.append(f"[OK] System Temp: {data['temperature']}°F (Threat: {data['threat_level']})")
            if data['threat_level'] != "Negligible":
                results.append(f"[ALERT] Active Inflammation: {len(data['anomalies'])} anomalies registered.")
        except:
            results.append("[ERROR] Health state file is corrupted.")
    else:
        results.append("[WARNING] Immune system not initialized.")

    # Check Filtration (The Liver)
    try:
        from tools.nexus_liver import NexusLiver
        liver = NexusLiver(base_dir)
        load = liver.get_toxic_load()
        results.append(f"[OK] Toxic Load: {load['toxicity_pct']:.1f}% ({load['stale_artifact_count']} stale artifacts)")
    except:
        results.append("[WARNING] Filtration engine not accessible.")

    # Check Sensory System (Streaming Nerves)
    try:
        from tools.nexus_senses import NexusSenses
        senses = NexusSenses(base_dir)
        status = senses.get_status()
        deprived = "DEPRIVED" if status.get("deprived") else "ACTIVE"
        results.append(f"[OK] Sensory Feed: {status['total_events']} events | Status: {deprived}")
        if status.get("deprived"):
            results.append("[WARNING] Sensory system stale — start nexus_senses.py background service.")
    except:
        results.append("[WARNING] Sensory engine not accessible.")

    # Check Physiological Dampening (Biological Compulsion)
    try:
        from tools.physiological_gate import PhysiologicalGate
        gate = PhysiologicalGate(base_dir)
        report = gate.get_dampening_report()
        blocked = [t for t, v in report["tools"].items() if not v["allowed"]]
        if blocked:
            results.append(f"[ALERT] Dampening active: {len(blocked)} tool(s) blocked ({', '.join(blocked)})")
        else:
            results.append("[OK] Physiological dampening: All gated tools cleared.")
    except:
        results.append("[WARNING] Physiological gate not accessible.")

    # Check Orchestrator (CPU Loop)
    try:
        from tools.orchestrator_engine import OrchestratorEngine
        from tools.service_heartbeat import ServiceHeartbeat
        orch = OrchestratorEngine(base_dir)
        status = orch.get_status()
        hb = ServiceHeartbeat(base_dir, "orchestrator")
        stale = hb.is_stale(20)
        hb_label = "STALE" if stale else "LIVE"
        results.append(f"[{'WARNING' if stale else 'OK'}] Orchestrator: {status['status']} | Ticks: {status['tick_count']} | Heartbeat: {hb_label}")
        if status.get("pending_directives", 0) > 0:
            results.append(f"[INFO] Pending sovereign directives: {status['pending_directives']}")
    except:
        results.append("[WARNING] Orchestrator engine not accessible.")

    # Check Supervisor / Service Heartbeats
    try:
        from tools.service_heartbeat import ServiceHeartbeat
        services = ServiceHeartbeat.all_services(base_dir)
        if services:
            alive = [s["service"] for s in services if (time.time() - s.get("timestamp", 0)) < 60]
            results.append(f"[OK] Autonomic services reporting: {', '.join(alive) or 'none'}")
        else:
            results.append("[WARNING] No service heartbeats. Run boot_nexus_os().")
    except:
        results.append("[WARNING] Service heartbeat check failed.")

    return "\n".join(results)
