# AOS — Agentic Operating System

> An open-source orchestration framework for persistent AI agents, built on biological metaphor: metabolism, endocrine, immune, motor, memory, and nervous systems.

## What is AOS?

AOS is a Python-based agentic operating system that gives AI agents a persistent physiological layer. Instead of stateless LLM calls that forget everything between prompts, AOS agents have:

- **Metabolism** — energy/token budgeting with conservation mode
- **Endocrine** — hormonal state (dopamine, cortisol, serotonin) that gates tool access
- **Immune** — autonomous WBC patrol, antibody correction, fever response to anomalies
- **Motor** — file writes and command execution with physiological permissioning
- **Memory** — dream-cycle consolidation of task history into wisdom artifacts
- **Nervous (Lattice)** — synaptic task handoffs between roles
- **Fission/Fusion** — spawn child instances or merge branch capabilities

Built on [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) with ~50 tools, a real-time customtkinter GUI, and autonomous background services.

## Quick Start

```bash
# Clone
git clone https://github.com/<your-username>/aos.git
cd aos

# Install dependencies
pip install -r mcp_server/python/requirements.txt

# Run the MCP server
python -m mcp_server.python.index

# Or launch the Neural Terminal GUI
python mcp_server/python/nexus_gui.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Sovereign (You)                       │
│  submit_directive | boot | status | patrol | cleanse     │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              Orchestrator Engine (CPU Loop)              │
│  tick() → senses → signals → directives → maintenance    │
└───────┬──────────────┬──────────────┬───────────────────┘
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ Senses  │   │ Lattice │   │ Motor   │
   │ (Nerves)│   │(Synapses│   │ (Hand)  │
   └────┬────┘   └────┬────┘   └────┬────┘
        │             │              │
   ┌────▼────────────▼───────┐      │
   │    Physiological Gate    │◄─────┘
   │  (Cortisol/Energy gating)│
   └────┬─────────────────────┘
        │
   ┌────▼──────────────────────────────────────┐
   │          Physiology Engine                │
   │  ┌──────────┬──────────┬──────────────┐  │
   │  │ Metabolism│ Endocrine│    Immune    │  │
   │  │ (Energy)  │ (Mood)   │ (Temperature)│  │
   │  └──────────┴──────────┴──────────────┘  │
   └──────────────────────────────────────────┘
```

## Example: Using AOS

```python
from mcp_server.python.tools.orchestrator_engine import OrchestratorEngine
from pathlib import Path

orch = OrchestratorEngine(Path("."))

# Queue a directive
result = orch.submit_directive("diagnose system", priority=5)
print(result)
# → Directive [a3f8b2c1] queued: diagnose system

# Run one CPU tick
tick = orch.tick()
print(tick["tick"])
# → 1
```

## Example: Physiological Gating

```python
from mcp_server.python.tools.physiology_engine import PhysiologyEngine
from mcp_server.python.tools.physiological_gate import PhysiologicalGate
from pathlib import Path

gate = PhysiologicalGate(Path("."))
allowed, msg = gate.check("propose_dna_mutation")
print(allowed, msg)
# → False "Mutation blocked: Cortisol too high or immune inflammation active."
```

## Example: Immune Patrol

```python
from mcp_server.python.tools.antibody_engine import AntibodyEngine
from pathlib import Path

engine = AntibodyEngine(Path("."))
results = engine.patrol()
for r in results:
    print(r)
# → [ANTIBODY AB-1712345678] corrupted_json: Restored monitoring/lattice_state.json from backup.
```

## Background Services

| Service | Script | Role |
|---------|--------|------|
| Pulse | `nexus_pulse.py` | Heartbeat every 60s — intelligence, memory, filtration |
| Guardian | `nexus_guardian.py` | Self-healing monitor — DNA integrity, metabolic check |
| Senses | `nexus_senses.py` | Filesystem watcher — real-time event stream |
| Orchestrator | `nexus_orchestrator.py` | CPU loop — senses → decision → motor → memory |
| Supervisor | `nexus_supervisor.py` | Boots and monitors all services |

## Project Structure

```
aos/
├── archives/                     # DNA (rules, roles, protocols)
│   └── core/
│       ├── foundation/           # Immutable constitution
│       ├── protocols/            # Filtration, immune, operating rules
│       ├── roles/                # Organizational role definitions
│       └── learning/             # Consolidated wisdom artifacts
├── core/
│   ├── exports/                  # Compiled logic graph (SQLite + YAML)
│   ├── monitoring/               # JSON state files
│   ├── nlg/                      # Natural language logic graph
│   └── pulses/                   # Firmware pulse files (.nxp)
├── mcp_server/
│   ├── python/
│   │   ├── index.py              # FastMCP server — tool registry
│   │   ├── nexus_gui.py          # Neural Terminal GUI
│   │   ├── nexus_pulse.py        # Heartbeat service
│   │   ├── nexus_orchestrator.py # CPU loop
│   │   ├── nexus_guardian.py     # Self-healing monitor
│   │   ├── nexus_senses.py       # Filesystem watcher
│   │   └── tools/                # Engine modules
│   │       ├── physiology_engine.py
│   │       ├── endocrine_engine.py
│   │       ├── antibody_engine.py
│   │       ├── motor_engine.py
│   │       ├── nexus_liver.py
│   │       ├── memory_synth.py
│   │       ├── nexus_lattice.py
│   │       ├── fission_fusion_engine.py
│   │       ├── signal_router.py
│   │       ├── physiological_gate.py
│   │       ├── vision_engine.py
│   │       └── video_engine.py
│   └── node/
│       └── index.ts              # TypeScript MCP entry point
├── plugins/
│   ├── core_plugin.py
│   ├── browser_plugin.py
│   ├── vision_plugin.py
│   └── plugin_registry.py
├── roles/                        # Role definitions
├── tests/
│   └── test_aos_integration.py   # Integration test suite
└── .cursor/                      # IDE rules, skills, commands, hooks
```

## Tests

```bash
python tests/test_aos_integration.py
```

Current status: **12/12 passing**

## License

MIT — see [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Status

Building in public. This is a working prototype. Expect rough edges. Feedback, bug reports, and PRs are welcome.

---

*Built in 48 hours after graduating B.Tech CSE. Shipped July 2026.*
