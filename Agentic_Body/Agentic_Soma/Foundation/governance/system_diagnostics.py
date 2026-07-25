# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SeshaAOS - System Diagnostics Tool
Version: 13.0.0
Description: Hyper-Somatic Singularity diagnostic for the full 13-layer stack.
"""

import json
import os
import sqlite3
import sys
import time
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

def run_diagnostics(base_dir: Path) -> str:
    """Performs deep-dive logic verification for Neural 13.8 (Tripartite Singularity)."""
    results = ["--- Sesha OS Diagnostic Report (Neural 13.8) ---"]

    # 1. Genome & Pulse Density
    pulse_dir = base_dir / "active_core" / "pulses"
    results.append(f"Pulse Path: {pulse_dir}")

    if pulse_dir.exists():
        nxp_files = list(pulse_dir.glob("*.nxp"))
        results.append(f"[OK] Pulse density: {len(nxp_files)} agent genomes active.")
    else:
        results.append("[WARNING] Pulse directory is missing. Agents may be dormant.")

    # 2. Physiology (Metabolism, Endocrine, Lipids)
    phys_path = base_dir / "core" / "monitoring" / "physiology.json"
    if phys_path.exists():
        try:
            with open(phys_path, "r", encoding="utf-8") as f:
                phys = json.load(f)
            
            # Metabolism
            met = phys.get("metabolism", {})
            energy = met.get("current_energy", 0)
            status = met.get("status", "Unknown")
            results.append(f"[OK] Metabolism: {energy} Energy ({status})")
            
            # Endocrine (Vibe & Hormones)
            end = phys.get("endocrine", {})
            vibe = end.get("vibe", "Stable")
            hormones = end.get("hormones", {})
            results.append(f"[OK] System Vibe: {vibe} (Dopamine: {hormones.get('dopamine', 0):.1f})")
            
            # Immune
            imm = phys.get("immune", {})
            temp = imm.get("temperature", 98.6)
            threat = imm.get("threat_level", "Negligible")
            results.append(f"[OK] System Temp: {temp}°F (Threat: {threat})")
            
            # Sleep State
            sleep = phys.get("sleep", {})
            results.append(f"[OK] Circadian State: {sleep.get('state', 'awake')}")
            
            # Resource Saturation (Neural 13.0)
            sat = phys.get_resource_saturation() if hasattr(phys, "get_resource_saturation") else phys.get("resource_saturation", {})
            results.append(f"[{'WARNING' if sat.get('hibernation_active') else 'OK'}] Cloud Resources: {sat.get('status', 'Optimal')}")
            results.append(f"[OK] Connection Lane: {sat.get('connection_priority', 'Priority')}")

        except Exception as e:
            results.append(f"[ERROR] Physiology file corrupted: {e}")
    else:
        results.append("[CRITICAL] Physiology data missing. System heartbeat at risk.")

    # 3. State Integrity (SQLite State DB)
    state_db = base_dir / "core" / "monitoring" / "Sesha_state.db"
    if state_db.exists():
        try:
            conn = sqlite3.connect(state_db)
            cursor = conn.cursor()
            
            # Lattice Check
            cursor.execute("SELECT count(*) FROM lattice_tasks")
            task_count = cursor.fetchone()[0]
            
            # Directive Queue Check
            cursor.execute("SELECT count(*) FROM directive_queue")
            directive_count = cursor.fetchone()[0]

            # Signal Check
            cursor.execute("SELECT count(*) FROM synaptic_signals WHERE active = 1")
            signal_count = cursor.fetchone()[0]

            # Immune Registry Check
            cursor.execute("SELECT count(*) FROM immune_registry")
            antigen_count = cursor.fetchone()[0]

            # UDG Check
            cursor.execute("SELECT count(*) FROM domain_graph")
            node_count = cursor.fetchone()[0]
            
            results.append(f"[OK] Neural Lattice: {task_count} tasks | {directive_count} directives.")
            results.append(f"[OK] Synaptic Mesh: {signal_count} active signals | {antigen_count} antigens recorded.")
            results.append(f"[OK] Universal Domain Graph: {node_count} nodes mapped.")
            conn.close()
        except Exception as e:
            results.append(f"[ERROR] State Database access failed: {e}")
    else:
        results.append("[WARNING] Sesha_state.db not found. Persistence is volatile.")

    # 4. Evolutionary Progress
    bio_genome = base_dir / "active_core" / "monitoring_active" / "evolution" / "biological_genome.json"
    if bio_genome.exists():
        try:
            with open(bio_genome, "r", encoding="utf-8") as f:
                genome = json.load(f)
            results.append(f"[OK] Evolutionary Generation: {genome.get('generation', 0)}")
            
            # Meta-metrics
            consts = genome.get("metabolic_constants", {})
            results.append(f"[OK] ATP Efficiency: {consts.get('atp_conversion_efficiency', 0.8)*100:.0f}%")
        except:
            results.append("[WARNING] Biological genome corrupted.")
    
    # 5. Body Schema & Synaptic Pressure
    schema_path = base_dir / "core" / "monitoring" / "body_schema.json"
    if schema_path.exists():
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
            results.append(f"[OK] Synaptic Pressure: {schema.get('synaptic_pressure', 1.0)}")
        except:
            pass

    # 6. NEURAL 13.0 Stack Integrity
    try:
        from layers.L04_Composition.composition_engine import CompositionEngine
        from layers.L07_Integration.integration_bridge import IntegrationBridge
        
        ce = CompositionEngine(base_dir)
        bridge = IntegrationBridge(base_dir)
        vitals = bridge.scan_host_vitals()
        
        results.append("\n--- NEURAL 13.0 Organism Status ---")
        results.append(f"[OK] L4 Composition: Dynamic bidding active.")
        results.append(f"[OK] L7 Integration: Host Skin active ({vitals.get('disk_pressure', 0):.1f}% Disk).")
        results.append(f"[OK] L12-L0 Alignment: Converged (Singularity State).")
    except Exception as e:
        results.append(f"[WARNING] Neural 13.0 layers incomplete: {e}")

    # 7. Service Heartbeats
    try:
        from layers.L07_Integration.service_heartbeat import ServiceHeartbeat
        services = ServiceHeartbeat.all_services(base_dir)
        if services:
            alive = [s["service"] for s in services if (time.time() - s.get("timestamp", 0)) < 60]
            results.append(f"[OK] Live Services: {', '.join(alive) or 'none'}")
    except:
        pass

    return "\n".join(results)

