"""
NexusAOS - MCP Registry
Version: 2.0.0
Description: Central registration for autonomous organizational tools.
"""

import json
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

_tools_parent = Path(__file__).resolve().parent
if str(_tools_parent) not in sys.path:
    sys.path.insert(0, str(_tools_parent))

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Import Tool Logic from specialized modules
from tools.system_diagnostics import run_diagnostics
from tools.auto_repair import AutoRepairEngine
from tools.nexus_lattice import LatticeEngine
from tools.memory_synth import MemorySynth
from tools.reproduction_engine import ReproductionEngine
from tools.mutation_engine import MutationEngine
from tools.nexus_liver import NexusLiver
from tools.nexus_senses import NexusSenses
from tools.thalamic_gate import ThalamicGate
from tools.basal_ganglia_gate import BasalGangliaGate
from tools.cortical_gate import CorticalGate
from tools.motor_engine import MotorEngine
from tools.orchestrator_engine import OrchestratorEngine
from tools.web_receptor import WebReceptor
from tools.memory_receptor import MemoryReceptor
from tools.body_schema import BodySchema
from tools.dream_engine import DreamEngine
from tools.github_receptor import GitHubReceptor
from tools.geo_receptor import GeoReceptor
from tools.database_receptor import DatabaseReceptor
from tools.slack_receptor import SlackReceptor
from tools.sentry_receptor import SentryReceptor
from tools.developmental_boot import DevelopmentalBoot
from tools.excalidraw_receptor import ExcalidrawReceptor
from tools.tldraw_receptor import TldrawReceptor
from tools.metabolism_engine import MetabolismEngine
from tools.endocrine_engine import EndocrineEngine
from tools.immune_engine import ImmuneEngine
from tools.sleep_engine import SleepEngine
from tools.digestive_engine import DigestiveEngine
from tools.respiratory_engine import RespiratoryEngine
from tools.skeletal_registry import SkeletalRegistry
from tools.integumentary_interface import IntegumentaryInterface
from tools.lymphatic_system import LymphaticSystem
from tools.excretory_engine import ExcretoryEngine
from tools.fission_fusion_engine import FissionFusionEngine
from tools.oxidation_model import OxidationModel
from tools.antibody_engine import AntibodyEngine
from tools.cellular_engine import CellularEngine
from tools.service_heartbeat import ServiceHeartbeat

# Initialize FastMCP Server
mcp = FastMCP("NexusAOI - Core Registry")

# --- Resources ---

@mcp.resource("nexus://core/logic")
def get_logic() -> str:
    path = BASE_DIR / "core/exports/nexus_aos_logic_export.json"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# --- Helpers ---

def _gate_allowed(action: str) -> tuple[bool, str]:
    allowed, msg = ThalamicGate(BASE_DIR).check(action)
    if not allowed:
        return allowed, msg
    allowed, msg = BasalGangliaGate(BASE_DIR).check(action)
    if not allowed:
        return allowed, msg
    return CorticalGate(BASE_DIR).check(action)

# --- Tools (Registry Only) ---

@mcp.tool()
def diagnose_os() -> str:
    """Performs deep-dive system logic and environment verification."""
    return run_diagnostics(BASE_DIR)

@mcp.tool()
def trigger_self_healing() -> str:
    """Triggers the Autonomous Repair Engine (ARE) to fix code deviations."""
    allowed, msg = _gate_allowed("trigger_self_healing")
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
    allowed, msg = _gate_allowed("spawn_parallel_subagent")
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
    guardian_path = BASE_DIR / "mcp_server/python/services/nexus_guardian.py"
    subprocess.Popen([sys.executable, str(guardian_path)],
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    return "Nexus Guardian service initiated in background console."

@mcp.tool()
def collect_intelligence() -> str:
    """Triggers the Oracle Scraper to gather new market and competitor signals."""
    allowed, msg = _gate_allowed("collect_intelligence")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    sys.path.insert(0, str(BASE_DIR / "mcp_server/python/scraper"))
    scraper = OracleScraper()
    res = scraper.scrape_tech_news()
    return f"Intelligence collection complete. Found {len(res)} signals."

@mcp.tool()
def browse_url(url: str) -> str:
    """Fetches a URL and returns extracted text content."""
    try:
        import requests
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned = "\n".join(lines[:200])
        return cleaned or "No readable content extracted."
    except Exception as e:
        return f"Browse error: {str(e)}"

@mcp.tool()
def query_knowledge(query: str) -> str:
    """Searches local knowledge base for relevant documents."""
    try:
        import faiss, json, numpy as np
        from tools.embedding_encoder import EmbeddingEncoder
        kb_path = BASE_DIR / "core/knowledge/faiss_index.bin"
        meta_path = BASE_DIR / "core/knowledge/index_meta.json"
        if not kb_path.exists() or not meta_path.exists():
            return "Knowledge base not found."
        index = faiss.read_index(str(kb_path))
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)["docs"]
        encoder = EmbeddingEncoder()
        q_vec = np.array([encoder.encode(query)], dtype="float32")
        scores, ids = index.search(q_vec, 5)
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if int(idx) < len(meta):
                doc = meta[int(idx)]
                results.append(f"- {doc.get('source','?')}: {doc.get('snippet','')[:220]}")
        return "\n".join(results) if results else "No relevant documents found."
    except Exception as e:
        return f"Knowledge query error: {str(e)}"

@mcp.tool()
def spawn_swarm(task_description: str, max_agents: int = 3) -> str:
    """Spawns a coordinated swarm of subagents for parallel task execution."""
    allowed, msg = _gate_allowed("spawn_swarm")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    return SwarmExecutor(BASE_DIR).run(task_description, max_agents=max_agents)

@mcp.tool()
def create_note(content: str, tags: str = "") -> str:
    """Creates a new system note and stores it in the memory synth."""
    allowed, msg = _gate_allowed("create_note")
    if not allowed:
        return f"PERMISSION DENIED: {msg}"
    MemorySynth(BASE_DIR).add(content, tags=tags)
    return "Note created."

@mcp.tool()
def get_system_status() -> str:
    """Returns current system state: vitals, sleep, energy, and recent signals."""
    metabolism = MetabolismEngine(BASE_DIR)
    sleep = SleepEngine(BASE_DIR)
    immune = ImmuneEngine(BASE_DIR)
    status = {
        "metabolism": {
            "energy": getattr(metabolism, "energy", None),
            "thermal_state": getattr(metabolism, "thermal_state", None),
        },
        "sleep": sleep.get_circadian_metrics() if hasattr(sleep, "get_circadian_metrics") else {},
        "immune": immune.get_status() if hasattr(immune, "get_status") else {},
    }
    return json.dumps(status, indent=2)

# Additional biology-focused tool wrappers can be registered here as needed.
# Existing receptor, lattice, dream, and script tool registrations are preserved
# in the full registry set maintained by FastMCP discovery.
