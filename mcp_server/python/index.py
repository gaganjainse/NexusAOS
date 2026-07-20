"""
Nexus Corporate OS - MCP Registry
Version: 2.0.0
Description: Central registration for autonomous organizational tools.
"""

import json
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Add local path to sys.path for tool importing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Tool Logic from specialized modules
from tools.system_diagnostics import run_diagnostics
from tools.auto_repair import AutoRepairEngine
from tools.signal_router import SignalRouter
from tools.nexus_lattice import LatticeEngine
from tools.memory_synth import MemorySynth
from tools.reproduction_engine import ReproductionEngine
from tools.mutation_engine import MutationEngine
from tools.physiology_engine import PhysiologyEngine
from tools.nexus_liver import NexusLiver
from tools.nexus_senses import NexusSenses
from tools.physiological_gate import PhysiologicalGate
from tools.motor_engine import MotorEngine
from tools.orchestrator_engine import OrchestratorEngine

# Initialize FastMCP Server
mcp = FastMCP("Nexus Corporate OS")
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- Resources ---

@mcp.resource("nexus://core/logic")
def get_logic() -> str:
    path = BASE_DIR / "core/exports/nexus_logic_export.json"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# --- Tools (Registry Only) ---

@mcp.tool()
def diagnose_os() -> str:
    """Performs deep-dive system logic and environment verification."""
    return run_diagnostics(BASE_DIR)

@mcp.tool()
def trigger_self_healing() -> str:
    """Triggers the Autonomous Repair Engine (ARE) to fix code deviations."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("trigger_self_healing")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    are = AutoRepairEngine(BASE_DIR)
    return are.scan_and_fix()

@mcp.tool()
def spawn_parallel_subagent(task_description: str, script_path: str = None) -> str:
    """
    Spawns a specialized Agentic Subagent for parallel task execution.
    Allows the OS to process noisy or long-running directives in the background.
    """
    allowed, msg = PhysiologicalGate(BASE_DIR).check("spawn_parallel_subagent")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    import subprocess
    import uuid
    subagent_id = str(uuid.uuid4())[:8]
    log_file = BASE_DIR / f"mcp_server/python/subagent_{subagent_id}.log"
    try:
        if script_path:
            abs_path = BASE_DIR / script_path if not os.path.isabs(script_path) else Path(script_path)
            subprocess.Popen([sys.executable, str(abs_path)],
                             stdout=open(log_file, "w"),
                             stderr=subprocess.STDOUT,
                             creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            return f"Subagent [{subagent_id}] spawned. Monitoring: {log_file}"
        return f"Subagent Context [{subagent_id}] initialized for: {task_description}"
    except Exception as e:
        return f"Spawn error: {str(e)}"

@mcp.tool()
def start_guardian_service() -> str:
    """Launches the background Nexus Guardian for real-time self-healing."""
    import subprocess
    guardian_path = BASE_DIR / "mcp_server/python/nexus_guardian.py"
    subprocess.Popen([sys.executable, str(guardian_path)],
                     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    return "Nexus Guardian service initiated in background console."

@mcp.tool()
def collect_intelligence() -> str:
    """Triggers the Oracle Scraper to gather new market and competitor signals."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("collect_intelligence")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    from oracle_scraper import OracleScraper
    scraper = OracleScraper()
    res = scraper.scrape_tech_news()
    return f"Intelligence collection complete. Found {len(res)} signals."

@mcp.tool()
def launch_human_viewer() -> str:
    """Autonomously launches the Nexus Desktop GUI (Human Viewing Layer)."""
    import subprocess
    gui_path = BASE_DIR / "mcp_server/python/nexus_gui.py"
    subprocess.Popen([sys.executable, str(gui_path)],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    return "Nexus GUI launched successfully."

@mcp.tool()
def get_energy_status() -> str:
    """Returns the current metabolic energy status (Healthy, Conserving, Critical)."""
    engine = PhysiologyEngine(BASE_DIR)
    state = engine.get_state()["metabolism"]
    percentage = (state['current_energy'] / state['max_energy']) * 100
    return f"Status: {state['status']} | Energy: {percentage:.1f}% ({state['current_energy']}/{state['max_energy']})"

@mcp.tool()
def log_energy_consumption(amount: int) -> str:
    """Logs the consumption of energy (tokens/units) and returns the new status."""
    engine = PhysiologyEngine(BASE_DIR)
    new_status = engine.consume_energy(amount)
    return f"Consumed {amount} units. New Status: {new_status}"

@mcp.tool()
def start_circulatory_system() -> str:
    """Launches the background Nexus Pulse (The Heart)."""
    import subprocess
    pulse_path = BASE_DIR / "mcp_server" / "python" / "nexus_pulse.py"
    subprocess.Popen([sys.executable, str(pulse_path)],
                     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    return "Nexus Pulse (Heartbeat) initiated in background."

@mcp.tool()
def emit_signal(signal_type: str, event_description: str, ttl: int = 300) -> str:
    """Emits a hormonal signal across the system with a specific TTL."""
    router = SignalRouter(BASE_DIR)
    return router.emit_signal(signal_type, {"event": event_description}, ttl_seconds=ttl)

@mcp.tool()
def get_active_signals() -> str:
    """Retrieves all currently active hormonal signals."""
    router = SignalRouter(BASE_DIR)
    signals = router.get_active_signals()
    if not signals: return "No active signals."
    return json.dumps(signals, indent=2)

@mcp.tool()
def dispatch_task(from_role: str, to_role: str, directive: str) -> str:
    """Dispatches a task through the Nexus Lattice (Synaptic Handoff)."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("dispatch_task")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    lattice = LatticeEngine(BASE_DIR)
    return lattice.fire_synapse(from_role, to_role, directive)

@mcp.tool()
def get_lattice_state() -> str:
    """Returns the current state of all active and historical synaptic nodes."""
    lattice = LatticeEngine(BASE_DIR)
    import json
    return json.dumps(lattice._read_state(), indent=2)

@mcp.tool()
def trigger_memory_consolidation() -> str:
    """Manually triggers the 'Dream Cycle' to synthesize experience from history."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("trigger_memory_consolidation")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    synth = MemorySynth(BASE_DIR)
    return synth.consolidate()

@mcp.tool()
def get_system_experience() -> str:
    """Retrieves a summary of consolidated memories and learned patterns."""
    synth = MemorySynth(BASE_DIR)
    return json.dumps(synth.get_wisdom_summary(), indent=2)

@mcp.tool()
def get_global_vibe() -> str:
    """Returns the current 'Emotional' state (Vibe) and hormonal levels of the OS."""
    engine = PhysiologyEngine(BASE_DIR)
    return json.dumps(engine.get_state()["endocrine"], indent=2)

@mcp.tool()
def generate_spore_export() -> str:
    """Packages the current OS state into a serialized 'Spore' for replication."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("generate_spore_export")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    engine = ReproductionEngine(BASE_DIR)
    return engine.create_spore()

@mcp.tool()
def spawn_child_instance(spore_name: str, target_path: str) -> str:
    """Instantiates a new Child OS from a specified Spore at the target path."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("spawn_child_instance")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    engine = ReproductionEngine(BASE_DIR)
    return engine.instantiate_spore(spore_name, Path(target_path))

@mcp.tool()
def propose_dna_mutation(target_file: str, snippet_to_replace: str, new_dna_text: str, reasoning: str) -> str:
    """Proposes and executes a mutation (surgical edit) to a Markdown DNA artifact."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("propose_dna_mutation")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    engine = MutationEngine(BASE_DIR)
    return engine.apply_mutation(target_file, snippet_to_replace, new_dna_text, reasoning)

@mcp.tool()
def report_system_anomaly(anomaly_type: str, severity: float) -> str:
    """Reports a system anomaly (logic drift, failure) to the Immune Engine."""
    engine = PhysiologyEngine(BASE_DIR)
    return engine.register_anomaly(anomaly_type, severity)

@mcp.tool()
def get_immune_status() -> str:
    """Returns the current 'Body Temperature' and threat level of the OS."""
    engine = PhysiologyEngine(BASE_DIR)
    return json.dumps(engine.get_state()["immune"], indent=2)

@mcp.tool()
def trigger_system_filtration() -> str:
    """Manually triggers the 'Excretion Cycle' (The Liver) to prune system toxins."""
    liver = NexusLiver(BASE_DIR)
    return liver.filter_toxins()

@mcp.tool()
def get_toxicity_report() -> str:
    """Retrieves current system 'Toxic Load' metrics from the Liver."""
    liver = NexusLiver(BASE_DIR)
    return json.dumps(liver.get_toxic_load(), indent=2)

@mcp.tool()
def start_sensory_system() -> str:
    """Launches the background Nexus Senses (Streaming Nerves) service."""
    import subprocess
    senses_path = BASE_DIR / "mcp_server" / "python" / "nexus_senses.py"
    subprocess.Popen([sys.executable, str(senses_path)],
                     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    return "Nexus Senses (Streaming Nerves) initiated in background."

@mcp.tool()
def get_sensory_feed(limit: int = 25) -> str:
    """Returns recent real-time sensory events from filesystem watchers."""
    senses = NexusSenses(BASE_DIR)
    return json.dumps(senses.get_feed(limit), indent=2)

@mcp.tool()
def get_sensory_status() -> str:
    """Returns sensory system health (active, deprived, watch paths)."""
    senses = NexusSenses(BASE_DIR)
    return json.dumps(senses.get_status(), indent=2)

@mcp.tool()
def register_sensory_watcher(relative_path: str) -> str:
    """Registers a directory for real-time filesystem perception."""
    senses = NexusSenses(BASE_DIR)
    return senses.register_watcher(relative_path)

@mcp.tool()
def get_physiological_dampening() -> str:
    """Returns which high-risk tools are blocked by current hormonal state."""
    gate = PhysiologicalGate(BASE_DIR)
    return json.dumps(gate.get_dampening_report(), indent=2)

@mcp.tool()
def execute_motor_write(relative_path: str, content: str) -> str:
    """Motor Agency: writes a file within the OS boundary."""
    motor = MotorEngine(BASE_DIR)
    return motor.write_file(relative_path, content)

@mcp.tool()
def execute_motor_command(command: str) -> str:
    """Motor Agency: runs an allowlisted shell command."""
    allowed, msg = PhysiologicalGate(BASE_DIR).check("execute_motor_command")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    motor = MotorEngine(BASE_DIR)
    return motor.run_command(command)

@mcp.tool()
def process_motor_queue() -> str:
    """Motor Agency: processes all pending MOTOR: lattice directives."""
    motor = MotorEngine(BASE_DIR)
    results = motor.process_lattice_queue()
    if not results:
        return "No pending motor directives."
    return "\n".join(results)

@mcp.tool()
def get_motor_status() -> str:
    """Returns motor engine action history and pending task count."""
    motor = MotorEngine(BASE_DIR)
    return json.dumps(motor.get_status(), indent=2)

@mcp.tool()
def boot_nexus_os() -> str:
    """Boots all autonomic services via the Supervisor (pulse, guardian, senses, orchestrator)."""
    import subprocess
    supervisor_path = BASE_DIR / "mcp_server" / "python" / "nexus_supervisor.py"
    subprocess.Popen([sys.executable, str(supervisor_path)],
                     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    return "Nexus Supervisor initiated. All autonomic services booting."

@mcp.tool()
def start_orchestrator() -> str:
    """Launches the background Nexus Orchestrator (CPU decision loop)."""
    import subprocess
    orch_path = BASE_DIR / "mcp_server" / "python" / "nexus_orchestrator.py"
    subprocess.Popen([sys.executable, str(orch_path)],
                     creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    return "Nexus Orchestrator (CPU loop) initiated in background."

@mcp.tool()
def submit_directive(directive_text: str, priority: int = 5) -> str:
    """Queues a Sovereign directive for autonomous Orchestrator execution."""
    orch = OrchestratorEngine(BASE_DIR)
    return orch.submit_directive(directive_text, priority)

@mcp.tool()
def get_orchestrator_status() -> str:
    """Returns Orchestrator tick count, pending directives, and routing weights."""
    orch = OrchestratorEngine(BASE_DIR)
    return json.dumps(orch.get_status(), indent=2)

@mcp.tool()
def get_service_heartbeats() -> str:
    """Returns liveness status of all autonomic background services."""
    from tools.service_heartbeat import ServiceHeartbeat
    return json.dumps(ServiceHeartbeat.all_services(BASE_DIR), indent=2)

@mcp.tool()
def run_immune_patrol() -> str:
    """Deploys WBC patrol and antibody correction mechanisms."""
    from tools.antibody_engine import AntibodyEngine
    engine = AntibodyEngine(BASE_DIR)
    results = engine.patrol()
    return "\n".join(results)

@mcp.tool()
def get_immune_cells_status() -> str:
    """Returns WBC, RBC, platelet, and antibody status."""
    from tools.antibody_engine import AntibodyEngine
    engine = AntibodyEngine(BASE_DIR)
    return json.dumps(engine.get_immune_cells_status(), indent=2)

@mcp.tool()
def get_cellular_health() -> str:
    """Returns health report for all mapped biological cell components."""
    from tools.cellular_engine import CellularEngine
    return json.dumps(CellularEngine(BASE_DIR).full_cell_report(), indent=2)

@mcp.tool()
def fission_branch(source_branch: str, target_name: str) -> str:
    """FISSION: Split a branch into an independent child AOS spore."""
    from tools.fission_fusion_engine import FissionFusionEngine
    return FissionFusionEngine(BASE_DIR).fission(source_branch, target_name)

@mcp.tool()
def fusion_branches(branch_a: str, branch_b: str, merged_name: str) -> str:
    """FUSION: Merge two branch pulses into a unified AXP firmware file."""
    from tools.fission_fusion_engine import FissionFusionEngine
    return FissionFusionEngine(BASE_DIR).fusion(branch_a, branch_b, merged_name)

@mcp.tool()
def analyze_image(image_path: str) -> str:
    """Analyzes an image: metadata, dimensions, brightness, visual classification."""
    from tools.vision_engine import VisionEngine
    return VisionEngine(BASE_DIR).extract_image_data(image_path)

@mcp.tool()
def analyze_video(video_path: str, max_frames: int = 5) -> str:
    """Analyzes a video: metadata and sample frame understanding."""
    from tools.video_engine import VideoEngine
    return json.dumps(VideoEngine(BASE_DIR).analyze_video(video_path, max_frames), indent=2)

@mcp.tool()
def get_plugin_registry_status() -> str:
    """Returns native Plugins/MCPs/Skills/Subagents/Rules/Commands/Hooks status."""
    import sys
    sys.path.insert(0, str(BASE_DIR / "plugins"))
    from plugin_registry import PluginRegistry
    return json.dumps(PluginRegistry(BASE_DIR).get_status(), indent=2)

if __name__ == "__main__":
    mcp.run()
