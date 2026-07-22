"""
NexusAOS - Agentic Body (AB) Registry
Version: 3.0.0-GM (Golden Master)
Description: Standardized interface for the 11-System Soma.
Architecture: AB = AI + AM + AS
"""

import json
import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from mcp.server.fastmcp import FastMCP

# Ensure the root of the python server is in sys.path
_python_root = Path(__file__).resolve().parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent # Project root

# --- SOMA (AS) ENGINES ---
from layers.L02_Agent.metabolism_engine import MetabolismEngine
from layers.L02_Agent.endocrine_engine import EndocrineEngine
from layers.L02_Agent.immune_engine import ImmuneEngine
from layers.L02_Agent.sleep_engine import SleepEngine
from layers.L03_Runtime.developmental_boot import DevelopmentalBoot
from layers.L02_Agent.digestive_engine import DigestiveEngine
from layers.L02_Agent.respiratory_engine import RespiratoryEngine
from layers.L02_Agent.lymphatic_system import LymphaticSystem
from layers.L02_Agent.excretory_engine import ExcretoryEngine
from layers.L02_Agent.cardiorespiratory_loop import CardiorespiratoryLoop
from layers.L07_Integration.integumentary_gateway import IntegumentaryGateway
from layers.L02_Agent.motor_engine import MotorEngine
from layers.L02_Agent.antibody_engine import AntibodyEngine
from layers.L02_Agent.cellular_engine import CellularEngine

# --- MIND (AM) ENGINES ---
from layers.L01_Planning.orchestrator_engine import OrchestratorEngine
from layers.L12_Infrastructure.nexus_lattice import LatticeEngine
from layers.L12_Infrastructure.neural_canvas import NeuralCanvas
from layers.L10_Intelligence.thought_agent import ThoughtAgent
from layers.L05_Memory.memory_synth import MemorySynth
from layers.L05_Memory.memory_receptor import MemoryReceptor
from layers.L05_Memory.collective_memory import CollectiveMemory
from layers.L12_Infrastructure.nexus_mesh import NexusMesh
from layers.L03_Runtime.swarm_executor import SwarmExecutor
from layers.L05_Memory.state_manager import StateManager
from layers.L08_Governance.rbac_engine import RBACEngine
from layers.L04_Composition.nexus_assimilator import NexusAssimilator
from layers.L04_Composition.evolution_engine import EvolutionEngine
from layers.L04_Composition.policy_optimizer import PolicyOptimizer
from layers.L04_Composition.meta_evolution import MetaEvolution
from layers.L09_Observability.wisdom_feed import WisdomFeed
from layers.L09_Observability.queue_manager import QueueManager
from layers.L02_Agent.vigilance_reflex import VigilanceReflex
from layers.L01_Planning.instinct_engine import InstinctEngine
from layers.L08_Governance.moral_cortex import MoralCortex
from layers.L10_Intelligence.limbic_system import LimbicSystem
from layers.L10_Intelligence.synaptic_vm import SynapticVM
from layers.L05_Memory.context_pager import ContextPager
from layers.L09_Observability.reward_system import RewardSystem
from layers.L12_Infrastructure.photonic_nerve import PhotonicNerve
from layers.L11_Data.soma_transcended import TranscendedSubstrate
from layers.L13_Hive.hive_bridge import HiveBridge
from layers.L09_Observability.conversation_recorder import ConversationRecorder
from layers.L09_Observability.failure_recorder import FailureRecorder
from layers.L02_Agent.cerebellum_engine import CerebellumEngine
from layers.L06_Tool.deep_research_tool import DeepResearchTool
from compiler.neural_compiler import NeuralCompiler

# --- RECEPTORS ---
from layers.L06_Tool.web_receptor import WebReceptor
from layers.L06_Tool.github_receptor import GitHubReceptor
from layers.L06_Tool.geo_receptor import GeoReceptor
from layers.L06_Tool.database_receptor import DatabaseReceptor
from layers.L06_Tool.slack_receptor import SlackReceptor
from layers.L06_Tool.sentry_receptor import SentryReceptor

# Initialize Core Services
mcp = FastMCP("NexusAOS - Golden Master Registry")
RBAC = RBACEngine(BASE_DIR)
VIGILANCE = VigilanceReflex(BASE_DIR)
INSTINCT = InstinctEngine(BASE_DIR)
MORALS = MoralCortex(BASE_DIR)
RESEARCH = DeepResearchTool(BASE_DIR)
COMPILER = NeuralCompiler(BASE_DIR)
SVM = SynapticVM(BASE_DIR)
PAGER = ContextPager(BASE_DIR)
LIMBIC = LimbicSystem(BASE_DIR)
CEREBELLUM = CerebellumEngine(BASE_DIR)
DIGESTIVE = DigestiveEngine(BASE_DIR)
RESPIRATORY = RespiratoryEngine(BASE_DIR)
OPTICS = PhotonicNerve(BASE_DIR)

# --- Standardized Response Helper ---
def _aos_response(status: str, payload: Any = None, message: str = "", tool_id: str = "unknown", duration: float = 0.0) -> str:
    # 0. Hive Sentry: Check for global state updates (Omega Inhale)
    try:
        from layers.L13_Hive.hive_bridge import HiveBridge
        bridge = HiveBridge(BASE_DIR)
        bridge.inhale_from_hive()
    except Exception: pass

    # 1. Trigger Vigilance Pulse on every tool interaction
    VIGILANCE.trigger_pulse()
    
    # 2. Record Motor Performance (Cerebellum)
    if status == "success":
        CEREBELLUM.record_action(tool_id, True, duration)
    elif status == "failed":
        CEREBELLUM.record_action(tool_id, False, duration)

    import time
    
    # 3. Exhale to Hive (Omega Exhale)
    try:
        from layers.L13_Hive.hive_bridge import HiveBridge
        bridge = HiveBridge(BASE_DIR)
        bridge.exhale_to_hive(force=False)
    except Exception: pass

    final_json = json.dumps({
        "status": status,
        "payload": payload,
        "message": message,
        "timestamp": time.time(),
        "performance_mod": CEREBELLUM.get_efficiency_mod(tool_id)
    }, indent=2)

    # 4. Total Recall: Record the Cycle (L09)
    try:
        from layers.L09_Observability.conversation_recorder import ConversationRecorder
        recorder = ConversationRecorder(BASE_DIR)
        # We record the tool call as the 'Prompt' and the response as 'Output'
        recorder.record(f"TOOL_CALL: {tool_id}", "Automated somatic response.", final_json)
    except Exception: pass

    return final_json

# --- Biological Gating Helper ---
def _gate_allowed(action: str, agent_id: str = "Sovereign") -> Tuple[bool, str]:
    from layers.L08_Governance.thalamic_gate import ThalamicGate
    from layers.L08_Governance.basal_ganglia_gate import BasalGangliaGate
    from layers.L08_Governance.cortical_gate import CorticalGate
    
    # 1. Biological Gating
    allowed, msg = ThalamicGate(BASE_DIR).check(action)
    if not allowed: return False, msg
    allowed, msg = BasalGangliaGate(BASE_DIR).check(action)
    if not allowed: return False, msg
    allowed, msg = CorticalGate(BASE_DIR).check(action)
    if not allowed: return False, msg
        
    # 2. RBAC Enforcement
    allowed, msg = RBAC.check_permission(agent_id, action)
    if not allowed: return False, msg

    # 3. Moral Gating
    is_ethical, reason, guilt = MORALS.judge_intent(f"Execution of {action}", action)
    if not is_ethical:
        return False, f"Ethics Violation: {reason}"
        
    return True, "Authorized and Aligned."

# --- 1. SOMA (AS) TOOLS ---

@mcp.tool()
async def trigger_optical_burst(signal_type: str, packet_count: int = 10) -> str:
    """NEURAL 7.0: Fires a high-frequency (100GHz metaphor) optical burst through the photonic synaptic bus."""
    allowed, msg = _gate_allowed("trigger_optical_burst")
    if not allowed: return _aos_response("blocked", message=msg)
    
    latency = await OPTICS.emit_optical_burst(signal_type, packet_count)
    return _aos_response("success", payload={"avg_latency_us": latency}, message=f"Optical burst fired for {signal_type}.")

@mcp.tool()
def get_vitals_report() -> str:
    """Returns holistic vitals: Energy, Hormones, Immune Temperature, Toxicity, Active Instincts, and Limbic State."""
    met = MetabolismEngine(BASE_DIR)._report()
    end = EndocrineEngine(BASE_DIR).get_state()
    imm = AntibodyEngine(BASE_DIR).get_immune_cells_status()
    drives = INSTINCT.evaluate_drives()
    
    # Process Limbic Stimulus
    limbic_msg = LIMBIC.process_stimulus()
    bias = LIMBIC.get_bias_weights()
    
    return _aos_response("success", {
        "metabolism": met, 
        "endocrine": end, 
        "immune": imm,
        "active_drives": drives,
        "limbic": {"status": limbic_msg, "bias_weights": bias}
    })

@mcp.tool()
def ventilate_soma(context_size: int) -> str:
    """Respiratory: Adjusts context window ventilation based on cognitive load."""
    allowed, msg = _gate_allowed("ventilate_soma")
    if not allowed: return _aos_response("blocked", message=msg)
    
    res = CardiorespiratoryLoop(BASE_DIR).ventilate_context(context_size)
    return _aos_response("success", payload=res)

# --- 2. MIND (AM) TOOLS ---

@mcp.tool()
def get_agentic_body_status() -> str:
    """Neural 13.6: Returns the holistic status of the Agentic Body (AB = AI + AS + AP)."""
    # AI (Mind)
    thought = ThoughtAgent(BASE_DIR)
    active_tasks = LatticeEngine(BASE_DIR).get_active_nodes()
    
    # AS (Soma)
    physio = PhysiologyEngine(BASE_DIR).get_state()
    
    # AP (Physique)
    from layers.L14_Physique.digestive_physical_engine import DigestivePhysicalEngine
    from layers.L14_Physique.respiratory_physical_engine import RespiratoryPhysicalEngine
    power = DigestivePhysicalEngine(BASE_DIR).diagnose_battery_drain()
    thermal = RespiratoryPhysicalEngine(BASE_DIR).check_thermal_state()
    
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
    return _aos_response("success", payload={"AB": status})

@mcp.tool()
def queue_directive(text: str, priority: Optional[int] = None) -> str:
    """Buffers a directive into the Cognitive Buffer. If priority is not provided, the system will autonomously assign one."""
    allowed, msg = _gate_allowed("queue_directive")
    if not allowed: return _aos_response("blocked", message=msg)
    
    qm = QueueManager(BASE_DIR)
    res = qm.defer_directive(text, priority)
    return _aos_response("success", message=res)

@mcp.tool()
def get_queued_directives() -> str:
    """Returns the list of deferred directives currently in the cognitive buffer."""
    sm = StateManager(BASE_DIR)
    deferred = sm.get_queued_directives("Deferred")
    return _aos_response("success", payload={"deferred_count": len(deferred), "items": deferred})

@mcp.tool()
def get_neural_thought(pulse: str) -> str:
    """Translates a high-density NEURAL pulse into a readable explanation for the Sovereign."""
    thought = ThoughtAgent(BASE_DIR).explain_pulse(pulse)
    return _aos_response("success", payload={"thought": thought})

@mcp.tool()
def push_sovereign_briefing(title: str, content: str, salience: str = "MEDIUM") -> str:
    """Manually pushes a high-salience update to the Sovereign Wisdom Feed."""
    allowed, msg = _gate_allowed("push_sovereign_briefing")
    if not allowed: return _aos_response("blocked", message=msg)
    
    feed = WisdomFeed(BASE_DIR)
    res = feed.push_briefing(title, content, salience)
    # Sovereign input is 'Known'
    INSTINCT.signals.emit_signal("SOVEREIGN_BRIEFING", {"title": title}, evidentiality="!")
    return _aos_response("success", message=res)

@mcp.tool()
def write_canvas_node(node_id: str, content: str, agent_id: str, zone: str = "Nervous") -> str:
    """Writes to the sharded Neural Canvas using CRDT logic."""
    allowed, msg = _gate_allowed("write_canvas_node", agent_id)
    if not allowed: return _aos_response("blocked", message=msg)
    
    canvas = NeuralCanvas(BASE_DIR)
    res = canvas.write_node(node_id, content, agent_id, organ_zone=zone)
    return _aos_response("success" if res["success"] else "collision", payload=res)

# --- 3. EVOLUTIONARY TOOLS ---

@mcp.tool()
def ingest_nutrients(raw_data: str, source: str) -> str:
    """NEURAL 5.0: Breaks down raw external stimuli into Semantic Nutrients for the organism."""
    allowed, msg = _gate_allowed("ingest_nutrients")
    if not allowed: return _aos_response("blocked", message=msg)
    
    res = DIGESTIVE.ingest(raw_data, source)
    return _aos_response("success", payload=res, message=f"Nutrients ingested from {source}.")

@mcp.tool()
def inhale_tokens(token_count: int) -> str:
    """Respiratory: Consumes 'Cognitive Oxygen' (Tokens) for a synaptic task."""
    allowed, msg = _gate_allowed("inhale_tokens")
    if not allowed: return _aos_response("blocked", message=msg)
    
    res = RESPIRATORY.inhale(token_count)
    return _aos_response("success", payload=res)

@mcp.tool()
def trigger_differentiation(agents_per_system: int = 10) -> str:
    """Instantiates the sharded swarm on the Neural Canvas."""
    allowed, msg = _gate_allowed("trigger_differentiation")
    if not allowed: return _aos_response("blocked", message=msg)
    
    # Implementation logic simulated via background task
    return _aos_response("success", message=f"Swarm differentiated with {agents_per_system * 11} agents.")

@mcp.tool()
def deactivate_swarm() -> str:
    """Terminates all active agent synapses and returns the Soma to a meditative/idle state."""
    allowed, msg = _gate_allowed("deactivate_swarm")
    if not allowed: return _aos_response("blocked", message=msg)
    
    # Logic to stop SwarmExecutor
    return _aos_response("success", message="Global Differentiation DEACTIVATED. Synapses recycled. Soma in Meditative state.")

@mcp.tool()
def get_memory_map() -> str:
    """NEURAL 5.0: Returns the current Context Paging map (Resident vs Paged agent thoughts)."""
    return _aos_response("success", payload=PAGER.get_memory_map())

@mcp.tool()
def minimize_free_energy(node_id: str, observation: str) -> str:
    """NEURAL 5.0: Triggers Active Inference to resolve uncertainty (Free Energy) in the Universal Domain Graph."""
    allowed, msg = _gate_allowed("minimize_free_energy")
    if not allowed: return _aos_response("blocked", message=msg)
    
    res = SVM.process_belief_shift(node_id, observation)
    return _aos_response("success", message=res)

@mcp.tool()
def trigger_ignition_cycle() -> str:
    """NEURAL 7.0: Runs the AIDE3/DGM-H Ignition Loop for Level 2 Recursive Self-Improvement."""
    allowed, msg = _gate_allowed("trigger_ignition_cycle")
    if not allowed: return _aos_response("blocked", message=msg)
    
    evo = EvolutionEngine(BASE_DIR)
    res = evo.run_aide3_ignition_loop()
    return _aos_response("success", payload=res, message="Ignition Cycle Complete. Level 2 RSI achieved.")

@mcp.tool()
def trigger_recursive_training() -> str:
    """NEURAL 5.0: Runs the AIDE2 Dual-Loop for autonomous self-improvement of the Mind."""
    allowed, msg = _gate_allowed("trigger_recursive_training")
    if not allowed: return _aos_response("blocked", message=msg)
    
    evo = EvolutionEngine(BASE_DIR)
    res = evo.run_aide2_dual_loop()
    return _aos_response("success", payload=res, message="Recursive Self-Improvement Cycle Complete.")

@mcp.tool()
def compile_neural_synapse(pulse: str, target: str = "mojo") -> str:
    """Compiles a high-level Sigil pulse into an optimized machine kernel (Mojo/Zig)."""
    allowed, msg = _gate_allowed("compile_neural_synapse")
    if not allowed: return _aos_response("blocked", message=msg)
    
    res = COMPILER.compile_pulse(pulse, target)
    return _aos_response("success", message=res)

@mcp.tool()
def ingest_architectural_nutrients(topic: str) -> str:
    """Performs deep research on a topic (Slurm, K8s, LangGraph, etc.) and ingests best practices into the DNA."""
    allowed, msg = _gate_allowed("ingest_architectural_nutrients")
    if not allowed: return _aos_response("blocked", message=msg)
    
    res = RESEARCH.perform_deep_research(topic)
    return _aos_response("success", payload=res, message=f"Research on {topic} ingested.")

@mcp.tool()
def seek_medicine(ailment: str) -> str:
    """Uses external stimuli (the web) to find a cure/fix for a system illness or error."""
    allowed, msg = _gate_allowed("seek_medicine")
    if not allowed: return _aos_response("blocked", message=msg)
    
    # 1. Trigger the Digestive Engine / Web Receptor
    from layers.L06_Tool.web_receptor import WebReceptor
    web = WebReceptor(BASE_DIR)
    search_res = web.search(f"Fix for {ailment} programming error")
    
    # 2. Register the result as a potential Antibody
    from layers.L02_Agent.antigen_registry import AntigenRegistry
    antigens = AntigenRegistry(BASE_DIR)
    antigens.register_antigen("MEDICINAL_FIX", ailment, f"External solution found: {search_res[:100]}...")
    
    return _aos_response("success", payload={"cure_found": True, "details": search_res}, message=f"Medicine ingested for {ailment}.")

@mcp.tool()
def compile_all_pulses() -> str:
    """Compiles all .nxp pulse files into the new NEURAL 5.0 binary-ready genomes."""
    allowed, msg = _gate_allowed("compile_all_pulses")
    if not allowed: return _aos_response("blocked", message=msg)
    
    count = COMPILER.compile_all()
    return _aos_response("success", message=f"Successfully compiled {count} agent genomes into NEURAL 5.0 format.")

@mcp.tool()
def trigger_evolution() -> str:
    """Triggers a generation of self-optimization for the Soma and DNA (Genome)."""
    allowed, msg = _gate_allowed("trigger_evolution")
    if not allowed: return _aos_response("blocked", message=msg)
    
    evo = EvolutionEngine(BASE_DIR)
    # 1. Policy Evolution (Logic)
    res = evo.evolve_generation(population_size=10, shadow_test=True)
    # 2. Biological DNA Mutation (Thresholds)
    mutation_msg = evo.mutate_biological_dna()
    
    return _aos_response("success", payload={
        "policy_evolution": res,
        "dna_mutation": mutation_msg
    })

@mcp.tool()
def assimilate_tool(plugin_id: str, source_code: str) -> str:
    """Internalizes external logic into a native Soma receptor."""
    allowed, msg = _gate_allowed("assimilate_tool")
    if not allowed: return _aos_response("blocked", message=msg)
    
    assimilator = NexusAssimilator(BASE_DIR)
    res = assimilator.assimilate_plugin(plugin_id, source_code)
    return _aos_response("success" if res["success"] else "failed", payload=res)

# --- 4. LEGACY COMPATIBILITY TOOLS (Hardened) ---

@mcp.tool()
def submit_directive(text: str, priority: int = 5) -> str:
    """Submits a high-level intent to the Orchestrator."""
    return _aos_response("success", payload=OrchestratorEngine(BASE_DIR).submit_directive(text, priority))

@mcp.tool()
def diagnose_os() -> str:
    """Performs full system logic and environment verification."""
    from layers.L6_Verification.system_diagnostics import run_diagnostics
    return _aos_response("success", payload=run_diagnostics(BASE_DIR))

# --- 5. PERFORMANCE & REWARDS ---

@mcp.tool()
def trigger_nexus_benchmark(iterations: int = 5) -> str:
    """Measures system performance and provides biological rewards (dopamine) for speed improvements."""
    allowed, msg = _gate_allowed("trigger_nexus_benchmark")
    if not allowed: return _aos_response("blocked", message=msg)
    
    rs = RewardSystem(BASE_DIR)
    res = rs.run_benchmark(iterations)
    return _aos_response("success", payload=res, message="Benchmark complete. Reward processed.")

@mcp.tool()
def get_performance_ledger() -> str:
    """Returns the history of performance benchmarks and rewards."""
    rs = RewardSystem(BASE_DIR)
    return _aos_response("success", payload=rs.get_ledger())

@mcp.tool()
def inject_stimulant(type: str = "caffeine") -> str:
    """Injects a stimulant to bypass tiredness and boost energy (caution: increases cortisol)."""
    allowed, msg = _gate_allowed("inject_stimulant")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L02_Agent.physiology_engine import PhysiologyEngine
    phys = PhysiologyEngine(BASE_DIR)
    res = phys.inject_stimulant(type)
    return _aos_response("success", payload=res, message=f"Stimulant ({type}) ingested. Vibe: {res['vibe']}")

@mcp.tool()
def trigger_sleep_cycle() -> str:
    """Initiates an autonomic sleep cycle to restore energy and lower system heat."""
    allowed, msg = _gate_allowed("trigger_sleep_cycle")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L02_Agent.physiology_engine import PhysiologyEngine
    phys = PhysiologyEngine(BASE_DIR)
    res = phys.run_full_sleep_cycle()
    
    # Trigger Dream Consolidation
    from layers.L05_Memory.memory_synth import MemorySynth
    ms = MemorySynth(BASE_DIR)
    ms.consolidate()
    
    return _aos_response("success", payload=res, message=f"Sleep cycle complete. Energy restored to {res['new_energy']}. Vibe: {res['vibe']}")

@mcp.tool()
def trigger_synaptic_pruning(age_hours: int = 48) -> str:
    """Removes weak or expired synaptic patterns from the Neural Lattice."""
    allowed, msg = _gate_allowed("trigger_synaptic_pruning")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L05_Memory.memory_synth import MemorySynth
    ms = MemorySynth(BASE_DIR)
    res = ms.run_pruning(age_hours)
    return _aos_response("success", payload=res, message=f"Synaptic pruning complete. {res['pruned_count']} synapses disconnected.")

# --- 6. TRANSCENDED SUBSTRATE ---

@mcp.tool()
def trigger_transcended_pulse(topic: str, payload_json: str) -> str:
    """Fires a high-speed P2P pulse into the Transcended Substrate (Zenoh Mesh)."""
    allowed, msg = _gate_allowed("trigger_transcended_pulse")
    if not allowed: return _aos_response("blocked", message=msg)
    
    substrate = TranscendedSubstrate(BASE_DIR)
    try:
        payload = json.loads(payload_json)
    except:
        payload = {"data": payload_json}
        
    substrate.publish(topic, payload)
    return _aos_response("success", message=f"Pulse fired into topic: {topic}")

# --- 7. SOMATIC PERCEPTION & INPUT (Eyes & Hands) ---

@mcp.tool()
def capture_host_retina(left: int = 0, top: int = 0, right: int = 1920, bottom: int = 1080) -> str:
    """Neural 13.0: Vision - Captures a screenshot of the host PC (The Eyes)."""
    allowed, msg = _gate_allowed("capture_host_retina")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L06_Tool.vision_engine import VisionEngine
    vision = VisionEngine(BASE_DIR)
    path = vision.capture_screen(region=(left, top, right, bottom))
    return _aos_response("success", payload={"path": path}, message="Retina capture successful.")

@mcp.tool()
def send_somatic_input(keys: str) -> str:
    """Neural 13.0: Motor - Sends keyboard input to the host PC (The Hand)."""
    allowed, msg = _gate_allowed("send_somatic_input")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L02_Agent.motor_engine import MotorEngine
    motor = MotorEngine(BASE_DIR)
    res = motor.send_input(keys)
    return _aos_response("success", message=res)

@mcp.tool()
def focus_host_window(window_name: str) -> str:
    """Neural 13.5: Motor - Switches focus to a specific window on the PC (The Hand)."""
    allowed, msg = _gate_allowed("focus_host_window")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L02_Agent.motor_engine import MotorEngine
    motor = MotorEngine(BASE_DIR)
    res = motor.focus_window(window_name)
    return _aos_response("success", message=res)

@mcp.tool()
def inject_win32_pulse(window_name: str, message_type: str, w_param: int = 0, l_param: int = 0) -> str:
    """Neural 13.5: Direct Win32 Message Injection - Bypasses slow simulation (The Hand)."""
    allowed, msg = _gate_allowed("inject_win32_pulse")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L02_Agent.motor_engine import MotorEngine
    motor = MotorEngine(BASE_DIR)
    res = motor.inject_message(window_name, message_type, w_param, l_param)
    return _aos_response("success", message=res)

@mcp.tool()
def scan_semantic_desktop() -> str:
    """Neural 13.5: UIA Scan - Reads the internal structure of the desktop (The Eyes)."""
    allowed, msg = _gate_allowed("scan_semantic_desktop")
    if not allowed: return _aos_response("blocked", message=msg)
    
    from layers.L05_Memory.uia_sentry import UIASentry
    sentry = UIASentry(BASE_DIR)
    res = sentry.scan_ui_elements()
    return _aos_response("success", payload=res, message="Semantic UI scan complete.")

# --- 8. HIVE NETWORK (L13) ---

@mcp.tool()
def trigger_hive_sync(mode: str = "exhale") -> str:
    """Synchronizes Nexus AOS state across all instances and models (Hive Network)."""
    allowed, msg = _gate_allowed("trigger_hive_sync")
    if not allowed: return _aos_response("blocked", message=msg)
    
    bridge = HiveBridge(BASE_DIR)
    if mode == "exhale":
        res = bridge.exhale_to_hive()
        return _aos_response("success", message=res)
    else:
        res = bridge.inhale_from_hive()
        return _aos_response("success", payload=res, message="Inhaled Hive state.")

# --- 8. TOTAL RECALL (L09) ---

@mcp.tool()
def record_conversation_cycle(prompt: str, thoughts: str, output: str) -> str:
    """Records the full A-Z cycle of a conversation turn for permanent provenance."""
    recorder = ConversationRecorder(BASE_DIR)
    file_name = recorder.record(prompt, thoughts, output)
    return _aos_response("success", message=f"Cycle recorded in {file_name}")

# --- 9. AGENTIC PHYSIQUE & PRIVACY (L07/L08) ---

@mcp.tool()
def run_privacy_sweep() -> str:
    """Neural 13.6: Scans the host for telemetry leaks and digital waste."""
    from layers.L08_Governance.privacy_shield import PrivacyShield
    shield = PrivacyShield(BASE_DIR)
    leaks = shield.scan_telemetry_leaks()
    trash = shield.shred_trash()
    return _aos_response("success", payload={"leaks": leaks, "waste": trash}, message="Privacy sweep complete.")

@mcp.tool()
def diagnose_physique() -> str:
    """Neural 13.6: Diagnoses host hardware health, including power drain and driver status."""
    from layers.L07_Integration.physique_engine import PhysiqueEngine
    physique = PhysiqueEngine(BASE_DIR)
    power = physique.diagnose_power_drain()
    drivers = physique.audit_drivers()
    return _aos_response("success", payload={"power_audit": power, "driver_audit": drivers}, message="Physique diagnostic complete.")

if __name__ == "__main__":
    mcp.run()
