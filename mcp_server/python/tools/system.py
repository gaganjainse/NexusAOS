"""System tool registry subset for mcp_server/python/index.py.

This module owns the MCP tools for system vitals, directives, memory, evolution,
performance, sleep, hive sync, and administrative operations.
"""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_server.python.hive_sync import HiveSync

hive_sync = HiveSync()
mcp = FastMCP("NexusAOS system tools")


def _response(status: str, payload: Any = None, message: str = "", tool_id: str = "unknown", duration: float = 0.0) -> str:
    result = json.dumps({
        "status": status,
        "payload": payload,
        "message": message,
        "timestamp": __import__("time").time(),
    }, indent=2)
    try:
        hive_sync.after_tool(tool_id, status == "success", duration)
    except Exception:
        pass
    return result


def _gate(action: str):
    from pathlib import Path
    from layers.L08_Governance.rbac_engine import RBACEngine
    base_dir = Path(__file__).resolve().parents[3]
    rbac = RBACEngine(base_dir)
    return rbac.check_permission("Sovereign", action)


def _services(base_dir):
    from layers.L02_Agent.metabolism_engine import MetabolismEngine
    from layers.L02_Agent.endocrine_engine import EndocrineEngine
    from layers.L02_Agent.antibody_engine import AntibodyEngine
    from layers.L01_Planning.instinct_engine import InstinctEngine
    from layers.L10_Intelligence.limbic_system import LimbicSystem
    from layers.L09_Observability.queue_manager import QueueManager
    from layers.L05_Memory.state_manager import StateManager
    from layers.L04_Composition.evolution_engine import EvolutionEngine
    from layers.L09_Observability.reward_system import RewardSystem
    from layers.L02_Agent.physiology_engine import PhysiologyEngine
    from layers.L05_Memory.memory_synth import MemorySynth
    from layers.L13_Hive.hive_bridge import HiveBridge
    from layers.L09_Observability.conversation_recorder import ConversationRecorder
    from layers.L08_Governance.privacy_shield import PrivacyShield
    from layers.L07_Integration.physique_engine import PhysiqueEngine
    from layers.L14_Physique.skeletal_engine import SkeletalEngine
    from layers.L14_Physique.power_governor import PowerGovernor
    from layers.L14_Physique.volume_manager import VolumeManager
    from layers.L06_Tool.vision_engine import VisionEngine
    from layers.L02_Agent.motor_engine import MotorEngine
    from layers.L05_Memory.uia_sentry import UIASentry
    from layers.L02_Agent.photonic_nerve import PhotonicNerve
    from layers.L03_Runtime.cardiorespiratory_loop import CardiorespiratoryLoop
    from layers.L05_Memory.context_pager import ContextPager
    from layers.L10_Intelligence.synaptic_vm import SynapticVM
    from layers.L02_Agent.cerebellum_engine import CerebellumEngine
    from layers.L02_Agent.digestive_engine import DigestiveEngine
    from layers.L02_Agent.respiratory_engine import RespiratoryEngine
    from layers.L01_Planning.orchestrator_engine import OrchestratorEngine
    from layers.L04_Composition.nexus_assimilator import NexusAssimilator
    from layers.L06_Tool.web_receptor import WebReceptor
    from layers.L12_Infrastructure.neural_canvas import NeuralCanvas
    from layers.L10_Intelligence.thought_agent import ThoughtAgent
    from layers.L12_Infrastructure.nexus_lattice import LatticeEngine
    from layers.L11_Data.soma_transcended import TranscendedSubstrate
    from compiler.neural_compiler import NeuralCompiler

    return {
        "metabolism": MetabolismEngine(base_dir),
        "endocrine": EndocrineEngine(base_dir),
        "antibody": AntibodyEngine(base_dir),
        "instinct": InstinctEngine(base_dir),
        "limbic": LimbicSystem(base_dir),
        "queue_manager": QueueManager(base_dir),
        "state_manager": StateManager(base_dir),
        "evolution": EvolutionEngine(base_dir),
        "reward": RewardSystem(base_dir),
        "physiology": PhysiologyEngine(base_dir),
        "memory_synth": MemorySynth(base_dir),
        "hive_bridge": HiveBridge(base_dir),
        "conversation_recorder": ConversationRecorder(base_dir),
        "privacy_shield": PrivacyShield(base_dir),
        "physique": PhysiqueEngine(base_dir),
        "skeletal": SkeletalEngine(base_dir),
        "power_governor": PowerGovernor(base_dir),
        "volume_manager": VolumeManager(base_dir),
        "vision": VisionEngine(base_dir),
        "motor": MotorEngine(base_dir),
        "uia_sentry": UIASentry(base_dir),
        "optics": PhotonicNerve(base_dir),
        "cardiorespiratory": CardiorespiratoryLoop(base_dir),
        "pager": ContextPager(base_dir),
        "svm": SynapticVM(base_dir),
        "cerebellum": CerebellumEngine(base_dir),
        "digestive": DigestiveEngine(base_dir),
        "respiratory": RespiratoryEngine(base_dir),
        "orchestrator": OrchestratorEngine(base_dir),
        "assimilator": NexusAssimilator(base_dir),
        "web_receptor": WebReceptor(base_dir),
        "neural_canvas": NeuralCanvas(base_dir),
        "thought_agent": ThoughtAgent(base_dir),
        "lattice": LatticeEngine(base_dir),
        "transcended": TranscendedSubstrate(base_dir),
        "compiler": NeuralCompiler(base_dir),
    }


@mcp.tool()
def get_vitals_report() -> str:
    """Returns holistic vitals: Energy, Hormones, Immune Temperature, Toxicity, Active Instincts, and Limbic State."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    met = services["metabolism"]._report()
    end = services["endocrine"].get_state()
    imm = services["antibody"].get_immune_cells_status()
    drives = services["instinct"].evaluate_drives()
    limbic_msg = services["limbic"].process_stimulus()
    bias = services["limbic"].get_bias_weights()
    duration = __import__("time").perf_counter() - start
    return _response("success", {
        "metabolism": met,
        "endocrine": end,
        "immune": imm,
        "active_drives": drives,
        "limbic": {"status": limbic_msg, "bias_weights": bias}
    }, tool_id="get_vitals_report", duration=duration)


@mcp.tool()
def ventilate_soma(context_size: int) -> str:
    """Respiratory: Adjusts context window ventilation based on cognitive load."""
    allowed, msg = _gate("ventilate_soma")
    if not allowed:
        return _response("blocked", message=msg, tool_id="ventilate_soma")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["cardiorespiratory"].ventilate_context(context_size)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, tool_id="ventilate_soma", duration=duration)


@mcp.tool()
def get_agentic_body_status() -> str:
    """Returns the holistic status of the Agentic Body (AB = AI + AS + AP)."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    thought = services["thought_agent"]
    active_tasks = services["lattice"].get_active_nodes()
    physio = services["physiology"].get_state()
    from layers.L14_Physique.digestive_physical_engine import DigestivePhysicalEngine
    from layers.L14_Physique.respiratory_physical_engine import RespiratoryPhysicalEngine
    power = DigestivePhysicalEngine(base_dir).diagnose_battery_drain()
    thermal = RespiratoryPhysicalEngine(base_dir).check_thermal_state()
    status = {
        "AI (Intelligence)": "Transcended Mind Active",
        "AS (Soma)": {
            "energy": physio["metabolism"]["current_energy"],
            "vibe": physio["endocrine"]["vibe"]
        },
        "AP (Physique)": {
            "power": power,
            "thermal": thermal,
            "state": "Hardening"
        }
    }
    duration = __import__("time").perf_counter() - start
    return _response("success", payload={"AB": status}, tool_id="get_agentic_body_status", duration=duration)


@mcp.tool()
def queue_directive(text: str, priority: int | None = None) -> str:
    """Buffers a directive into the Cognitive Buffer."""
    allowed, msg = _gate("queue_directive")
    if not allowed:
        return _response("blocked", message=msg, tool_id="queue_directive")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["queue_manager"].defer_directive(text, priority)
    duration = __import__("time").perf_counter() - start
    return _response("success", message=res, tool_id="queue_directive", duration=duration)


@mcp.tool()
def get_queued_directives() -> str:
    """Returns the list of deferred directives currently in the cognitive buffer."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    deferred = services["state_manager"].get_queued_directives("Deferred")
    duration = __import__("time").perf_counter() - start
    return _response("success", payload={"deferred_count": len(deferred), "items": deferred}, tool_id="get_queued_directives", duration=duration)


@mcp.tool()
def trigger_ignition_cycle() -> str:
    """Runs the AIDE3/DGM-H Ignition Loop for Level 2 Recursive Self-Improvement."""
    allowed, msg = _gate("trigger_ignition_cycle")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_ignition_cycle")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["evolution"].run_aide3_ignition_loop()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message="Ignition Cycle Complete. Level 2 RSI achieved.", tool_id="trigger_ignition_cycle", duration=duration)


@mcp.tool()
def trigger_recursive_training() -> str:
    """Runs the AIDE2 Dual-Loop for autonomous self-improvement of the Mind."""
    allowed, msg = _gate("trigger_recursive_training")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_recursive_training")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["evolution"].run_aide2_dual_loop()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message="Recursive Self-Improvement Cycle Complete.", tool_id="trigger_recursive_training", duration=duration)


@mcp.tool()
def compile_neural_synapse(pulse: str, target: str = "mojo") -> str:
    """Compiles a high-level Sigil pulse into an optimized machine kernel (Mojo/Zig)."""
    allowed, msg = _gate("compile_neural_synapse")
    if not allowed:
        return _response("blocked", message=msg, tool_id="compile_neural_synapse")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["compiler"].compile_pulse(pulse, target)
    duration = __import__("time").perf_counter() - start
    return _response("success", message=res, tool_id="compile_neural_synapse", duration=duration)


@mcp.tool()
def compile_all_pulses() -> str:
    """Compiles all .nxp pulse files into the new NEURAL 5.0 binary-ready genomes."""
    allowed, msg = _gate("compile_all_pulses")
    if not allowed:
        return _response("blocked", message=msg, tool_id="compile_all_pulses")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    count = services["compiler"].compile_all()
    duration = __import__("time").perf_counter() - start
    return _response("success", message=f"Successfully compiled {count} agent genomes into NEURAL 5.0 format.", tool_id="compile_all_pulses", duration=duration)


@mcp.tool()
def trigger_evolution() -> str:
    """Triggers a generation of self-optimization for the Soma and DNA (Genome)."""
    allowed, msg = _gate("trigger_evolution")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_evolution")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["evolution"].evolve_generation(population_size=10, shadow_test=True)
    mutation_msg = services["evolution"].mutate_biological_dna()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload={
        "policy_evolution": res,
        "dna_mutation": mutation_msg
    }, tool_id="trigger_evolution", duration=duration)


@mcp.tool()
def assimilate_tool(plugin_id: str, source_code: str) -> str:
    """Internalizes external logic into a native Soma receptor."""
    allowed, msg = _gate("assimilate_tool")
    if not allowed:
        return _response("blocked", message=msg, tool_id="assimilate_tool")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["assimilator"].assimilate_plugin(plugin_id, source_code)
    duration = __import__("time").perf_counter() - start
    return _response("success" if res["success"] else "failed", payload=res, tool_id="assimilate_tool", duration=duration)


@mcp.tool()
def submit_directive(text: str, priority: int = 5) -> str:
    """Submits a high-level intent to the Orchestrator."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["orchestrator"].submit_directive(text, priority)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, tool_id="submit_directive", duration=duration)


@mcp.tool()
def diagnose_os() -> str:
    """Performs full system logic and environment verification."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    from layers.L06_Verification.system_diagnostics import run_diagnostics
    res = run_diagnostics(base_dir)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, tool_id="diagnose_os", duration=duration)


@mcp.tool()
def trigger_nexus_benchmark(iterations: int = 5) -> str:
    """Measures system performance and provides biological rewards (dopamine) for speed improvements."""
    allowed, msg = _gate("trigger_nexus_benchmark")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_nexus_benchmark")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["reward"].run_benchmark(iterations)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message="Benchmark complete. Reward processed.", tool_id="trigger_nexus_benchmark", duration=duration)


@mcp.tool()
def get_performance_ledger() -> str:
    """Returns the history of performance benchmarks and rewards."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["reward"].get_ledger()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, tool_id="get_performance_ledger", duration=duration)


@mcp.tool()
def inject_stimulant(type: str = "caffeine") -> str:
    """Injects a stimulant to bypass tiredness and boost energy (caution: increases cortisol)."""
    allowed, msg = _gate("inject_stimulant")
    if not allowed:
        return _response("blocked", message=msg, tool_id="inject_stimulant")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["physiology"].inject_stimulant(type)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message=f"Stimulant ({type}) ingested. Vibe: {res['vibe']}", tool_id="inject_stimulant", duration=duration)


@mcp.tool()
def trigger_sleep_cycle() -> str:
    """Initiates an autonomic sleep cycle to restore energy and lower system heat."""
    allowed, msg = _gate("trigger_sleep_cycle")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_sleep_cycle")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["physiology"].run_full_sleep_cycle()
    services["memory_synth"].consolidate()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message=f"Sleep cycle complete. Energy restored to {res['new_energy']}. Vibe: {res['vibe']}", tool_id="trigger_sleep_cycle", duration=duration)


@mcp.tool()
def trigger_synaptic_pruning(age_hours: int = 48) -> str:
    """Removes weak or expired synaptic patterns from the Neural Lattice."""
    allowed, msg = _gate("trigger_synaptic_pruning")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_synaptic_pruning")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["memory_synth"].run_pruning(age_hours)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message=f"Synaptic pruning complete. {res['pruned_count']} synapses disconnected.", tool_id="trigger_synaptic_pruning", duration=duration)


@mcp.tool()
def trigger_transcended_pulse(topic: str, payload_json: str) -> str:
    """Fires a high-speed P2P pulse into the Transcended Substrate (Zenoh Mesh)."""
    allowed, msg = _gate("trigger_transcended_pulse")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_transcended_pulse")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    try:
        payload = json.loads(payload_json)
    except Exception:
        payload = {"data": payload_json}
    services["transcended"].publish(topic, payload)
    duration = __import__("time").perf_counter() - start
    return _response("success", message=f"Pulse fired into topic: {topic}", tool_id="trigger_transcended_pulse", duration=duration)


@mcp.tool()
def trigger_hive_sync(mode: str = "exhale") -> str:
    """Synchronizes Nexus AOS state across all instances and models (Hive Network)."""
    allowed, msg = _gate("trigger_hive_sync")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_hive_sync")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    if mode == "exhale":
        res = services["hive_bridge"].exhale_to_hive()
        duration = __import__("time").perf_counter() - start
        return _response("success", message=res, tool_id="trigger_hive_sync", duration=duration)
    else:
        res = services["hive_bridge"].inhale_from_hive()
        duration = __import__("time").perf_counter() - start
        return _response("success", payload=res, message="Inhaled Hive state.", tool_id="trigger_hive_sync", duration=duration)


@mcp.tool()
def record_conversation_cycle(prompt: str, thoughts: str, output: str) -> str:
    """Records the full A-Z cycle of a conversation turn for permanent provenance."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    file_name = services["conversation_recorder"].record(prompt, thoughts, output)
    duration = __import__("time").perf_counter() - start
    return _response("success", message=f"Cycle recorded in {file_name}", tool_id="record_conversation_cycle", duration=duration)


@mcp.tool()
def run_privacy_sweep() -> str:
    """Scans the host for telemetry leaks and digital waste."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    leaks = services["privacy_shield"].scan_telemetry_leaks()
    trash = services["privacy_shield"].shred_trash()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload={"leaks": leaks, "waste": trash}, message="Privacy sweep complete.", tool_id="run_privacy_sweep", duration=duration)


@mcp.tool()
def diagnose_physique() -> str:
    """Diagnoses host hardware health, including power drain, driver status, and logical volumes."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    power = services["power_governor"].get_active_scheme()
    parasites = services["power_governor"].find_battery_parasites()
    storage = services["skeletal"].get_pc_health_status()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload={
        "power_profile": power,
        "battery_parasites": parasites,
        "skeletal_vitals": storage
    }, message="Tripartite Physique diagnostic complete.", tool_id="diagnose_physique", duration=duration)


@mcp.tool()
def optimize_soma_power(mode: str = "power_saver") -> str:
    """Adjusts the physical host's power limits to save ATP/Battery."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    if mode == "power_saver":
        res = services["power_governor"].set_power_saver()
    else:
        res = services["power_governor"].set_performance_mode()
    duration = __import__("time").perf_counter() - start
    return _response("success", message=res, tool_id="optimize_soma_power", duration=duration)


@mcp.tool()
def execute_logical_separation() -> str:
    """Physically isolates the Body's three cores into separate Soma volumes."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    isolation = services["volume_manager"].simulate_isolation()
    sync = services["skeletal"].distribute_to_volumes()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload={
        "isolation_status": isolation,
        "volumes_synced": len(sync)
    }, message="Logical Soma Separation complete.", tool_id="execute_logical_separation", duration=duration)


@mcp.tool()
def get_memory_map() -> str:
    """Returns the current Context Paging map (Resident vs Paged agent thoughts)."""
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["pager"].get_memory_map()
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, tool_id="get_memory_map", duration=duration)


@mcp.tool()
def minimize_free_energy(node_id: str, observation: str) -> str:
    """Triggers Active Inference to resolve uncertainty (Free Energy) in the Universal Domain Graph."""
    allowed, msg = _gate("minimize_free_energy")
    if not allowed:
        return _response("blocked", message=msg, tool_id="minimize_free_energy")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["svm"].process_belief_shift(node_id, observation)
    duration = __import__("time").perf_counter() - start
    return _response("success", message=res, tool_id="minimize_free_energy", duration=duration)


@mcp.tool()
def ingest_nutrients(raw_data: str, source: str) -> str:
    """Breaks down raw external stimuli into Semantic Nutrients for the organism."""
    allowed, msg = _gate("ingest_nutrients")
    if not allowed:
        return _response("blocked", message=msg, tool_id="ingest_nutrients")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["digestive"].ingest(raw_data, source)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, message=f"Nutrients ingested from {source}.", tool_id="ingest_nutrients", duration=duration)


@mcp.tool()
def inhale_tokens(token_count: int) -> str:
    """Respiratory: Consumes 'Cognitive Oxygen' (Tokens) for a synaptic task."""
    allowed, msg = _gate("inhale_tokens")
    if not allowed:
        return _response("blocked", message=msg, tool_id="inhale_tokens")
    start = __import__("time").perf_counter()
    from pathlib import Path
    base_dir = Path(__file__).resolve().parents[3]
    services = _services(base_dir)
    res = services["respiratory"].inhale(token_count)
    duration = __import__("time").perf_counter() - start
    return _response("success", payload=res, tool_id="inhale_tokens", duration=duration)


@mcp.tool()
def trigger_differentiation(agents_per_system: int = 10) -> str:
    """Instantiates the sharded swarm on the Neural Canvas."""
    allowed, msg = _gate("trigger_differentiation")
    if not allowed:
        return _response("blocked", message=msg, tool_id="trigger_differentiation")
    start = __import__("time").perf_counter()
    duration = __import__("time").perf_counter() - start
    return _response("success", message=f"Swarm differentiated with {agents_per_system * 11} agents.", tool_id="trigger_differentiation", duration=duration)


@mcp.tool()
def deactivate_swarm() -> str:
    """Terminates all active agent synapses and returns the Soma to a meditative/idle state."""
    allowed, msg = _gate("deactivate_swarm")
    if not allowed:
        return _response("blocked", message=msg, tool_id="deactivate_swarm")
    start = __import__("time").perf_counter()
    duration = __import__("time").perf_counter() - start
    return _response("success", message="Global Differentiation DEACTIVATED. Synapses recycled. Soma in Meditative state.", tool_id="deactivate_swarm", duration=duration)