# AOS — Agentic Operating System

AOS is an agentic operating system with biological metaphor architecture — metabolism, endocrine, immune, and motor layers for AI orchestration.

## What It Is

Most AI agents today are stateless. They get a prompt, run some tools, and forget everything. AOS explores what persistent, self-governing agents would look like by mapping operating-system concepts onto biological systems:

- **Metabolism** — energy/token budgeting with conservation mode
- **Endocrine** — hormonal state (dopamine, cortisol, serotonin) that gates tool access
- **Immune** — WBC patrol, antibody correction, fever response to anomalies
- **Motor** — autonomous file writes and command execution with physiological permissioning
- **Memory** — dream-cycle consolidation of task history into wisdom
- **Lattice** — synaptic task handoffs between roles
- **Fission/Fusion** — spawn child instances or merge branch capabilities

## Architecture

```
+-------------------------------------------------------------+
|                        SOVEREIGN (You)                      |
+-------------------------------------------------------------+
|  MCP Server (~50 tools) | CustomTkinter GUI (V5.0)          |
+---------------------------+---------------------------------+
|                                                             |
|  +----------------+  +----------------+  +---------------+  |
|  |  ORCHESTRATOR  |  |   LATTICE      |  |   SIGNAL      |  |
|  |  (CPU Loop)    |<->|  (Synapses)    |  |   ROUTER      |  |
|  +----------------+  +----------------+  +---------------+  |
|         |                  |                  |            |
|  +------+-----+  +--------+--------+  +------+-------+    |
|  |  PHYSIO    |  |  SENSES         |  |  MOTOR       |    |
|  |  GATE      |  |  (Filesystem)   |  |  (Executor)   |    |
|  +------------+  +-----------------+  +--------------+    |
|         |                  |                  |            |
|  +------+-----+  +--------+--------+  +------+-------+    |
|  |  METABOLISM|  |  ENDOCRINE      |  |  IMMUNE      |    |
|  |  (Energy)  |  |  (Hormones)     |  |  (WBC/Fever)  |    |
|  +------------+  +-----------------+  +--------------+    |
|                                                             |
+-------------------------------------------------------------+
|  Background Services: Pulse | Guardian | Senses | Orch      |
+-------------------------------------------------------------+
|  State: core/monitoring/*.json (JSON state management)      |
+-------------------------------------------------------------+
```

## Quick Start

### Prerequisites

- Python 3.9+
- Windows, macOS, or Linux

### Installation

```bash
git clone https://github.com/<your-username>/aos-agentic-operating-system.git
cd aos-agentic-operating-system

pip install -r mcp_server/python/requirements.txt
pip install customtkinter pillow opencv-python-headless
```

> **Note:** `requirements.txt` lists the core MCP dependencies. For the GUI and vision tools, you also need `customtkinter`, `pillow`, and `opencv-python-headless`.

### Run the MCP Server

```bash
python -m mcp_server.python.index
```

### Launch the GUI

```bash
python mcp_server/python/nexus_gui.py
```

## Usage Examples

### 1. Check System Energy Status

```python
from tools.physiology_engine import PhysiologyEngine
from pathlib import Path

engine = PhysiologyEngine(Path("."))
state = engine.get_state()["metabolism"]
pct = (state["current_energy"] / state["max_energy"]) * 100
print(f"Status: {state['status']} | Energy: {pct:.1f}%")
```

### 2. Dispatch a Task Through the Lattice

```python
from tools.nexus_lattice import LatticeEngine
from pathlib import Path

lattice = LatticeEngine(Path("."))
result = lattice.fire_synapse("Sovereign", "Motor", "MOTOR:write:hello.txt:world")
print(result)
```

### 3. Run WBC Immune Patrol

```python
from tools.antibody_engine import AntibodyEngine
from pathlib import Path

engine = AntibodyEngine(Path("."))
results = engine.patrol()
for r in results:
    print(r)
```

## Project Structure

```
aos-agentic-operating-system/
├── mcp_server/
│   └── python/
│       ├── index.py                  # FastMCP entry point (~50 tools)
│       ├── nexus_gui.py              # CustomTkinter GUI V5.0
│       ├── nexus_supervisor.py       # Background service supervisor
│       ├── nexus_pulse.py            # Heartbeat service
│       ├── nexus_guardian.py         # Self-healing service
│       ├── nexus_senses.py           # Filesystem watcher service
│       ├── nexus_orchestrator.py     # CPU decision loop
│       ├── nxp_forge.py              # Compiles DNA into .nxp pulse files
│       ├── nlg_compiler.py           # Compiles markdown into SQLite + YAML
│       ├── requirements.txt
│       └── tools/
│           ├── orchestrator_engine.py   # Closed-loop controller
│           ├── physiology_engine.py     # Unified state: metabolism, endocrine, immune
│           ├── physiological_gate.py    # Permission layer based on hormones
│           ├── nexus_lattice.py         # Synaptic task handoffs
│           ├── motor_engine.py          # Autonomous file/command execution
│           ├── memory_synth.py          # Dream-cycle consolidation
│           ├── antibody_engine.py       # Immune system: WBC patrol, antibodies
│           ├── nexus_liver.py           # Toxin filtration
│           ├── nexus_senses.py          # Sensory event feed
│           ├── signal_router.py         # Hormonal signal emission
│           ├── cellular_engine.py       # 12 biological components mapped to AOS
│           ├── fission_fusion_engine.py # Mitosis (spawn) and hybridization (merge)
│           ├── reproduction_engine.py   # Spore creation and instantiation
│           ├── mutation_engine.py       # DNA surgical edits
│           ├── vision_engine.py         # Image analysis
│           ├── video_engine.py          # Video frame analysis
│           ├── auto_repair.py           # Autonomous code repair
│           ├── system_diagnostics.py    # Deep-dive system verification
│           └── service_heartbeat.py     # Liveness tracking for services
├── core/
│   └── monitoring/                   # JSON state files
│       ├── physiology.json
│       ├── orchestrator_state.json
│       ├── lattice_state.json
│       ├── signals.json
│       ├── sensory_feed.json
│       ├── immune_cells.json
│       └── heartbeats/
├── plugins/
│   └── plugin_registry.py            # Plugins/MCPs/Skills/Subagents/Rules
├── tests/
│   └── test_aos_integration.py       # 12/12 integration tests
├── roles/                            # Role definitions
├── archives/                         # Fission/fusion archives, learning logs
├── LICENSE
└── README.md
```

## GUI Tabs (V5.0)

| Tab | Description |
|-----|-------------|
| Neural DNA | View and edit role logic/markdown |
| Synaptic Flow | Active lattice synapses and task handoffs |
| Autonomic Core | Orchestrator status, service heartbeats, cellular health |
| Immune System | Temperature, threat level, WBC patrol, antibody status |
| Platform Layers | Plugin registry, Cursor bridge, vision cache |
| Lineage | Fission/fusion event history |

## State Conventions

All persistent state lives in `core/monitoring/` as JSON files:

- `physiology.json` — metabolism, endocrine (hormones), immune (temperature, threat)
- `orchestrator_state.json` — tick count, status, pending directives
- `lattice_state.json` — synaptic history and active nodes
- `signals.json` — active hormonal signals with TTL
- `sensory_feed.json` — filesystem watch events
- `motor_log.json` — action history
- `immune_cells.json` — WBC, RBC, platelet counts

## Background Services

AOS runs autonomic services via `subprocess.Popen`. On Windows, they use `CREATE_NEW_CONSOLE` so they survive independently:

| Service | Description |
|---------|-------------|
| Pulse | Heartbeat emitter (keeps state alive) |
| Guardian | Self-healing monitor (auto-restarts crashed services) |
| Senses | Filesystem watcher (streams events to sensory feed) |
| Orchestrator | CPU decision loop (ticks every N seconds) |
| Supervisor | Boots and monitors all services |

## Physiological Gate

The gate is the central permission layer. High-risk tools are blocked based on:

- **Cortisol level** — stress hormones reduce permitted risk
- **Energy percentage** — critical energy suspends non-essential operations
- **Immune threat level** — fever/sepsis triggers automatic healing mode

Blocked tools include: `propose_dna_mutation`, `spawn_child_instance`, `execute_motor_command`, `dispatch_task`, and more.

## Integration Tests

```bash
python tests/test_aos_integration.py
```

Current status: **12/12 passing**

## Tech Stack

- Python 3.9+
- FastMCP (Model Context Protocol)
- CustomTkinter (GUI)
- JSON state management
- Subprocess orchestration

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT — see [LICENSE](LICENSE)

## Status

Built in 48 hours as a working prototype. Expect rough edges, inconsistent naming, and missing error handling. The biological metaphor is the core idea; the implementation is a proof of concept.

If you're building agents that need to run for days/weeks/months — not just seconds — I'd love your feedback.
