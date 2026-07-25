"""
SeshaAOS - Agentic Body (AB) Registry
Version: 3.0.0-GM (Golden Master)
Description: Standardized interface for the 11-System Soma.
Architecture: AB = AI + AM + AS
"""

from pathlib import Path
from typing import Any, Optional
import json
import sys

from mcp.server.fastmcp import FastMCP

_python_root = Path(__file__).resolve().parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent  # Project root

# --- PHYSIQUE (AP) ENGINES ---
from Agentic_Body.Agentic_Physique.metabolism_engine import MetabolismEngine
from Agentic_Body.Agentic_Physique.endocrine_engine import EndocrineEngine
from Agentic_Body.Agentic_Physique.physiology_engine import PhysiologyEngine
from Agentic_Body.Agentic_Physique.kernel.physique_engine import PhysiqueEngine
from Agentic_Body.Agentic_Physique.digestive_engine import DigestiveEngine
from Agentic_Body.Agentic_Physique.respiratory_engine import RespiratoryEngine
from Agentic_Body.Agentic_Physique.cardiorespiratory_loop import CardiorespiratoryLoop
from Agentic_Body.Agentic_Physique.antibody_engine import AntibodyEngine
from Agentic_Body.Agentic_Physique.kernel.physique_engine import PhysiqueEngine
from Agentic_Body.Agentic_Physique.power_governor import PowerGovernor
from Agentic_Body.Agentic_Physique.skeletal_engine import SkeletalEngine
from Agentic_Body.Agentic_Physique.volume_manager import VolumeManager
from Agentic_Body.Agentic_Physique.vigilance_reflex import VigilanceReflex

# --- MIND (AM) ENGINES ---
from Agentic_Body.Agentic_Intelligence.planning.orchestrator_engine import OrchestratorEngine
from Agentic_Body.Agentic_Soma.Foundation.dna.sesha_lattice import LatticeEngine
from Agentic_Body.Agentic_Soma.Foundation.dna.neural_canvas import NeuralCanvas
from Agentic_Body.Agentic_Intelligence.intelligence.thought_agent import ThoughtAgent
from Agentic_Body.Agentic_Soma.Foundation.dna.sesha_mesh import SeshaMesh
from Agentic_Body.Agentic_Physique.nervous.synaptic_mesh import SynapticMesh
from Agentic_Body.Agentic_Intelligence.memory.state_manager import StateManager
from Agentic_Body.Agentic_Soma.Foundation.governance.rbac_engine import RBACEngine
from Agentic_Body.Agentic_Soma.Foundation.dna.sesha_assimilator import SeshaAssimilator
from Agentic_Body.Agentic_Soma.Foundation.dna.evolution_engine import EvolutionEngine
from Agentic_Body.Agentic_Soma.Foundation.governance.wisdom_feed import WisdomFeed
from Agentic_Body.Agentic_Soma.Foundation.governance.queue_manager import QueueManager
from Agentic_Body.Agentic_Intelligence.planning.instinct_engine import InstinctEngine
from Agentic_Body.Agentic_Soma.Foundation.governance.moral_cortex import MoralCortex
from Agentic_Body.Agentic_Intelligence.intelligence.limbic_system import LimbicSystem
from Agentic_Body.Agentic_Intelligence.intelligence.synaptic_vm import SynapticVM
from Agentic_Body.Agentic_Intelligence.memory.context_pager import ContextPager
from Agentic_Body.Agentic_Soma.Foundation.governance.reward_system import RewardSystem
from Agentic_Body.Agentic_Intelligence.memory.memory_synth import MemorySynth
from Agentic_Body.Agentic_Intelligence.memory.uia_sentry import UIASentry
from Agentic_Body.Agentic_Physique.motor_engine import MotorEngine
from Agentic_Body.Agentic_Soma.Foundation.governance.privacy_shield import PrivacyShield
from Agentic_Body.Agentic_Soma.Foundation.governance.conversation_recorder import ConversationRecorder
from Agentic_Body.Agentic_Physique.nervous.hive_bridge import HiveBridge
from Agentic_Body.Agentic_Physique.nervous.transcended_substrate import TranscendedSubstrate
from Agentic_Body.Agentic_Intelligence.tools.vision_engine import VisionEngine

# --- MCP Server ---
mcp = FastMCP("SeshaAOS-AB")

# --- GATE ---
def _gate_allowed(tool_name: str) -> tuple[bool, str]:
    """Checks if a tool call is allowed by the Basal Ganglia Gate."""
    cortex = MoralCortex(BASE_DIR)
    allowed = cortex.is_allowed(tool_name)
    if not allowed:
        return False, f"Moral Cortex denied: {tool_name} violates ethical constraints."
    return True, ""

def _aos_response(status: str, payload: Any = None, message: str = "") -> str:
    """Standardized JSON response for all AB tools."""
    import json
    return json.dumps({"status": status, "payload": payload, "message": message})

# --- 1. METABOLIC & ENDOCRINE (L01/L02) ---

@mcp.tool()
def get_metabolic_state() -> str:
    """Returns current ATP, glucose, heat, and metabolic status."""
    eng = MetabolismEngine(BASE_DIR)
    return _aos_response("success", payload=eng.get_state())

@mcp.tool()
def consume_atp(amount: float) -> str:
    """Consumes ATP for tool execution."""
    eng = MetabolismEngine(BASE_DIR)
    return _aos_response("success", payload=eng.consume_energy(amount))

@mcp.tool()
def rest_recovery(duration_seconds: float) -> str:
    """Deep rest — full metabolic recovery (analogous to deep sleep)."""
    eng = MetabolismEngine(BASE_DIR)
    return _aos_response("success", payload=eng.rest_recovery(duration_seconds))

@mcp.tool()
def emergency_glucose() -> str:
    """Emergency glucose release (cortisol/adrenaline boost)."""
    eng = MetabolismEngine(BASE_DIR)
    return _aos_response("success", payload=eng.emergency_glucose())

@mcp.tool()
def get_endocrine_state() -> str:
    """Returns current hormone levels (cortisol, dopamine, serotonin, oxytocin, melatonin)."""
    eng = EndocrineEngine(BASE_DIR)
    return _aos_response("success", payload=eng.get_state())

@mcp.tool()
def trigger_hormone_surge(hormone: str, intensity: float = 1.0) -> str:
    """Triggers a controlled hormone surge for testing or simulation."""
    eng = EndocrineEngine(BASE_DIR)
    return _aos_response("success", payload=eng.trigger_surge(hormone, intensity))

# --- 2. PLANNING & ORCHESTRATION (L03/L04) ---

@mcp.tool()
def submit_directive(text: str, priority: int = 5) -> str:
    """Submits a sovereign directive to the Orchestrator."""
    orch = OrchestratorEngine(BASE_DIR)
    return _aos_response("success", payload=orch.submit(text, priority))

@mcp.tool()
def get_active_directives() -> str:
    """Returns all currently active directives in the cognitive buffer."""
    orch = OrchestratorEngine(BASE_DIR)
    return _aos_response("success", payload=orch.get_active())

@mcp.tool()
def queue_directive(text: str, priority: int | None = None) -> str:
    """Buffers a directive into the Cognitive Buffer. If priority is not provided, the system will autonomously assign one."""
    from Agentic_Body.Agentic_Intelligence.planning.queue_manager import QueueManager
    allowed, msg = _gate_allowed("queue_directive")
    if not allowed:
        return _aos_response("blocked", message=msg)
    qm = QueueManager(BASE_DIR)
    res = qm.defer_directive(text, priority)
    return _aos_response("success", message=res)

@mcp.tool()
def get_queued_directives() -> str:
    """Returns the list of deferred directives currently in the cognitive buffer."""
    from Agentic_Body.Agentic_Intelligence.planning.queue_manager import QueueManager
    qm = QueueManager(BASE_DIR)
    return _aos_response("success", payload=qm.list_queued())

# --- 3. INSTINCT & SELF-EVOLUTION (L05/L06) ---

@mcp.tool()
def trigger_instinct_check() -> str:
    """Runs the instinct engine to detect and execute autonomous survival behaviors."""
    eng = InstinctEngine(BASE_DIR)
    return _aos_response("success", payload=eng.run_check())

@mcp.tool()
def trigger_self_evolution() -> str:
    """Triggers the self-evolving kernel to mutate and improve the agent genome."""
    eng = EvolutionEngine(BASE_DIR)
    return _aos_response("success", payload=eng.evolve())

@mcp.tool()
def assimilate_knowledge(source: str) -> str:
    """Assimilates external knowledge into the agent's DNA (SeshaAssimilator)."""
    assimilator = SeshaAssimilator(BASE_DIR)
    return _aos_response("success", payload=assimilator.assimilate(source))

# --- 4. LIMBIC & SYNAPTIC (L07/L08) ---

@mcp.tool()
def get_limbic_state() -> str:
    """Returns the current limbic emotional state (valence, arousal, dominance)."""
    limbic = LimbicSystem(BASE_DIR)
    return _aos_response("success", payload=limbic.get_state())

@mcp.tool()
def trigger_limbic_response(stimulus: str) -> str:
    """Triggers a limbic emotional response to a stimulus."""
    limbic = LimbicSystem(BASE_DIR)
    return _aos_response("success", payload=limbic.respond(stimulus))

@mcp.tool()
def get_synaptic_state() -> str:
    """Returns the current state of the synaptic mesh (connections, weights)."""
    mesh = SynapticMesh(BASE_DIR)
    return _aos_response("success", payload=mesh.get_state())

@mcp.tool()
def trigger_synaptic_plasticity() -> str:
    """Triggers synaptic plasticity adaptation (Hebbian learning simulation)."""
    mesh = SynapticMesh(BASE_DIR)
    return _aos_response("success", payload=mesh.adapt())

# --- 5. PHYSIOLOGICAL HOMEOSTASIS (L01/L02/L03) ---

@mcp.tool()
def get_physiology_vitals() -> str:
    """Returns full physiological vitals: cardio, respiratory, digestive, metabolic."""
    phys = PhysiologyEngine(BASE_DIR)
    return _aos_response("success", payload=phys.get_state())

@mcp.tool()
def trigger_sleep_cycle() -> str:
    """Initiates a full sleep cycle: metabolic consolidation, memory synthesis, hormone reset."""
    from Agentic_Body.Agentic_Intelligence.memory.memory_synth import MemorySynth
    
    phys = PhysiologyEngine(BASE_DIR)
    phys.sleep()
    
    ms = MemorySynth(BASE_DIR)
    res = ms.consolidate()
    
    return _aos_response("success", payload=res, message=f"Sleep cycle complete. Energy restored to {res['new_energy']}. Vibe: {res['vibe']}")

@mcp.tool()
def trigger_synaptic_pruning(age_hours: int = 48) -> str:
    """Removes weak or expired synaptic patterns from the Neural Lattice."""
    ms = MemorySynth(BASE_DIR)
    res = ms.run_pruning(age_hours)
    return _aos_response("success", payload=res, message=f"Synaptic pruning complete. {res['pruned_count']} synapses disconnected.")

# --- 6. TRANSCENDED SUBSTRATE ---

@mcp.tool()
def trigger_transcended_pulse(topic: str, payload_json: str) -> str:
    """Fires a high-speed P2P pulse into the Transcended Substrate (Zenoh Mesh)."""
    allowed, msg = _gate_allowed("trigger_transcended_pulse")
    if not allowed:
        return _aos_response("blocked", message=msg)
    
    substrate = TranscendedSubstrate(BASE_DIR)
    try:
        payload = json.loads(payload_json)
        if not isinstance(payload, dict):
            payload = {"data": payload_json, "type": "string"}
    except Exception:  # noqa: BLE001
        payload = {"data": payload_json, "type": "string"}
        
    substrate.publish(topic, payload)
    return _aos_response("success", message=f"Pulse fired into topic: {topic}")

# --- 7. SOMATIC PERCEPTION & INPUT (Eyes & Hands) ---

@mcp.tool()
def capture_host_retina(left: int = 0, top: int = 0, right: int = 1920, bottom: int = 1080) -> str:
    """Neural 13.0: Vision - Captures a screenshot of the host PC (The Eyes)."""
    allowed, msg = _gate_allowed("capture_host_retina")
    if not allowed:
        return _aos_response("blocked", message=msg)
    
    vision = VisionEngine(BASE_DIR)
    path = vision.capture_screen(region=(left, top, right, bottom))
    return _aos_response("success", payload={"path": path}, message="Retina capture successful.")

@mcp.tool()
def send_somatic_input(keys: str) -> str:
    """Neural 13.0: Motor - Sends keyboard input to the host PC (The Hand)."""
    allowed, msg = _gate_allowed("send_somatic_input")
    if not allowed:
        return _aos_response("blocked", message=msg)
    
    motor = MotorEngine(BASE_DIR)
    res = motor.send_input(keys)
    return _aos_response("success", message=res)

@mcp.tool()
def focus_host_window(window_name: str) -> str:
    """Neural 13.5: Motor - Switches focus to a specific window on the PC (The Hand)."""
    allowed, msg = _gate_allowed("focus_host_window")
    if not allowed:
        return _aos_response("blocked", message=msg)
    
    motor = MotorEngine(BASE_DIR)
    res = motor.focus_window(window_name)
    return _aos_response("success", message=res)

@mcp.tool()
def inject_win32_pulse(window_name: str, message_type: str, w_param: int = 0, l_param: int = 0) -> str:
    """Neural 13.5: Direct Win32 Message Injection - Bypasses slow simulation (The Hand)."""
    allowed, msg = _gate_allowed("inject_win32_pulse")
    if not allowed:
        return _aos_response("blocked", message=msg)
    
    motor = MotorEngine(BASE_DIR)
    res = motor.inject_message(window_name, message_type, w_param, l_param)
    return _aos_response("success", message=res)

@mcp.tool()
def scan_semantic_desktop() -> str:
    """Neural 13.5: UIA Scan - Reads the internal structure of the desktop (The Eyes)."""
    allowed, msg = _gate_allowed("scan_semantic_desktop")
    if not allowed:
        return _aos_response("blocked", message=msg)
    
    sentry = UIASentry(BASE_DIR)
    res = sentry.scan_ui_elements()
    return _aos_response("success", payload=res, message="Semantic UI scan complete.")

# --- 8. HIVE NETWORK (L13) ---

@mcp.tool()
def trigger_hive_sync(mode: str = "exhale") -> str:
    """Synchronizes Sesha AOS state across all instances and models (Hive Network)."""
    allowed, msg = _gate_allowed("trigger_hive_sync")
    if not allowed:
        return _aos_response("blocked", message=msg)
    
    if mode not in ("exhale", "inhale"):
        return _aos_response("blocked", message=f"Invalid hive sync mode: {mode}. Allowed: exhale, inhale.")
    
    bridge = HiveBridge(BASE_DIR)
    if mode == "exhale":
        res = bridge.exhale_to_hive()
        return _aos_response("success", message=res)
    else:
        res = bridge.inhale_from_hive()
        return _aos_response("success", payload=res, message="Inhaled Hive state.")

# --- 9. TOTAL RECALL (L09) ---
# Provenance tracking: links audit/provenance trail (AUDIT_REPORT.md line 1-149 audit trail; mesh_hive_sync_status.md sync/provenance status; COMMIT_MESSAGE.md commit 40203ec NEURAL 15.0 specialization cycle; dataset/11_SYSTEM_MAPPING.md 11-system provenance framework; saved logs: bone_marrow.log / physiology.json / signal_history.json). Reference special framework (AGENTS.md line 36-39: specialization mandate + provenance tracking + cycle commit protocol + evolution tracking). Provenance applies to record_conversation_cycle (line 595-601) and total recall cycle.

@mcp.tool()
def record_conversation_cycle(prompt: str, thoughts: str, output: str) -> str:
    """Records the full A-Z cycle of a conversation turn for permanent provenance."""
    recorder = ConversationRecorder(BASE_DIR)
    file_name = recorder.record(prompt, thoughts, output)
    return _aos_response("success", message=f"Cycle recorded in {file_name}")

# --- 10. AGENTIC PHYSIQUE & PRIVACY (L07/L08) ---

@mcp.tool()
def run_privacy_sweep() -> str:
    """Neural 13.6: Scans the host for telemetry leaks and digital waste."""
    shield = PrivacyShield(BASE_DIR)
    leaks = shield.scan_telemetry_leaks()
    trash = shield.shred_trash()
    return _aos_response("success", payload={"leaks": leaks, "waste": trash}, message="Privacy sweep complete.")

@mcp.tool()
def diagnose_physique() -> str:
    """Neural 13.8: Diagnoses host hardware health, including power drain, driver status, and logical volumes."""
    physique = PhysiqueEngine(BASE_DIR)
    skeletal = SkeletalEngine(BASE_DIR)
    governor = PowerGovernor(BASE_DIR)
    
    power = governor.get_active_scheme()
    parasites = governor.find_battery_parasites()
    storage = skeletal.get_pc_health_status()
    
    return _aos_response("success", payload={
        "power_profile": power,
        "battery_parasites": parasites,
        "skeletal_vitals": storage
    }, message="Tripartite Physique diagnostic complete.")

@mcp.tool()
def optimize_soma_power(mode: str = "power_saver") -> str:
    """Neural 13.8: Adjusts the physical host's power limits to save ATP/Battery."""
    gov = PowerGovernor(BASE_DIR)
    if mode == "power_saver":
        res = gov.set_power_saver()
    else:
        res = gov.set_performance_mode()
    return _aos_response("success", message=res)

@mcp.tool()
def execute_logical_separation() -> str:
    """Neural 13.8: Physically isolates the Body's three cores into separate Soma volumes."""
    vm = VolumeManager(BASE_DIR)
    skeletal = SkeletalEngine(BASE_DIR)
    
    isolation = vm.simulate_isolation()
    sync = skeletal.distribute_to_volumes()
    
    return _aos_response("success", payload={
        "isolation_status": isolation,
        "volumes_synced": len(sync)
    }, message="Logical Soma Separation complete.")

if __name__ == "__main__":
    mcp.run()