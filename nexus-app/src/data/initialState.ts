import {
  FileNode,
  AOSService,
  MCPTool,
  DBTable,
  GitCommit,
  SystemProcess,
  ChatMessage,
  CoreWorkspaceState,
} from "../types/nexus";

export const INITIAL_FILES: FileNode[] = [
  {
    name: "nexus_aos",
    path: "nexus_aos",
    type: "folder",
    children: [
      {
        name: "src",
        path: "nexus_aos/src",
        type: "folder",
        children: [
          {
            name: "main.py",
            path: "nexus_aos/src/main.py",
            type: "file",
            gitStatus: "M",
            language: "python",
            content: `import sys
import time
from core.orchestrator import OrchestratorEngine
from core.vitals import HostVitalsMonitor

def evolve():
    """Main evolutionary loop for Nexus-AOS"""
    orchestrator = OrchestratorEngine()
    vitals = HostVitalsMonitor()
    
    print("[NEXUS-AOS] Bootstrapping Homeostatic Control Loop...")
    while True:
        state = vitals.scan_host()
        if state.ischemia > 80.0:
            print(f"[ALARM] Ischemia high ({state.ischemia}%). Triggering disk conservation.")
            orchestrator.trigger_conservation()
            
        orchestrator.pulse()
        time.sleep(1.0)

if __name__ == "__main__":
    evolve()
`,
          },
          {
            name: "sovereign_terminal.py",
            path: "nexus_aos/src/sovereign_terminal.py",
            type: "file",
            gitStatus: "A",
            language: "python",
            content: `# Sovereign Terminal UI Engine
class SovereignTerminal:
    def __init__(self, theme="android_studio_dark"):
        self.theme = theme
        self.quadrants = ["L1_Explorer", "L2_Editor", "L3_Tools", "L4_BottomBar"]
        self.pet_companion = "Nexus-alpha"
        
    def render_workspace(self):
        return f"Rendering {len(self.quadrants)} layout zones with companion {self.pet_companion}."
`,
          },
        ],
      },
      {
        name: "core",
        path: "nexus_aos/core",
        type: "folder",
        children: [
          {
            name: "orchestrator.py",
            path: "nexus_aos/core/orchestrator.py",
            type: "file",
            gitStatus: "none",
            language: "python",
            content: `class OrchestratorEngine:
    def __init__(self):
        self.active_agents = ["Orchestrator-01", "Guardian-AOS", "Motor-AOS"]
        
    def pulse(self):
        # Heartbeat dispatch cycle
        pass

    def trigger_conservation(self):
        print("[ORCHESTRATOR] Purging temporary caches & vector buffers.")
`,
          },
          {
            name: "vitals.py",
            path: "nexus_aos/core/vitals.py",
            type: "file",
            gitStatus: "none",
            language: "python",
            content: `class HostVitalsMonitor:
    def scan_host(self):
        class State:
            ischemia = 79.1 # Disk C %
            hypoxia = 0     # CPU stress %
            fever = 37.2    # Temp °C
            energy = 78     # %
        return State()
`,
          },
        ],
      },
      {
        name: "tests",
        path: "nexus_aos/tests",
        type: "folder",
        children: [
          {
            name: "test_vitals.py",
            path: "nexus_aos/tests/test_vitals.py",
            type: "file",
            gitStatus: "none",
            language: "python",
            content: `def test_vitals_homeostasis():
    from core.vitals import HostVitalsMonitor
    m = HostVitalsMonitor()
    s = m.scan_host()
    assert s.energy > 50
    assert s.fever < 40.0
`,
          },
        ],
      },
      {
        name: "assets",
        path: "nexus_aos/assets",
        type: "folder",
        children: [
          {
            name: "nexus_logo.svg",
            path: "nexus_aos/assets/nexus_logo.svg",
            type: "file",
            gitStatus: "none",
            content: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="100%" height="100%">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00f2fe;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#4facfe;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="240" height="240" rx="40" fill="#09090b" />
  <circle cx="120" cy="120" r="80" fill="none" stroke="url(#grad1)" stroke-width="6" filter="url(#glow)" />
  <polygon points="120,50 175,150 65,150" fill="none" stroke="#a855f7" stroke-width="4" />
  <circle cx="120" cy="120" r="16" fill="#00f2fe" />
  <text x="120" y="210" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">NEXUS SOVEREIGN</text>
</svg>`,
          },
          {
            name: "neural_architecture.png",
            path: "nexus_aos/assets/neural_architecture.png",
            type: "file",
            gitStatus: "none",
            content: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='800' height='450' fill='%2309090b'><rect width='100%' height='100%' fill='%2309090b'/><circle cx='400' cy='225' r='120' fill='none' stroke='%2300f2fe' stroke-width='4'/><text x='400' y='230' fill='%2300f2fe' font-family='sans-serif' font-size='20' text-anchor='middle'>NEURAL MESH ARCHITECTURE</text></svg>",
          },
        ],
      },
      {
        name: "data",
        path: "nexus_aos/data",
        type: "folder",
        children: [
          {
            name: "vitals_telemetry.csv",
            path: "nexus_aos/data/vitals_telemetry.csv",
            type: "file",
            gitStatus: "none",
            content: `Timestamp,CPU_Usage_Pct,Mem_Usage_MB,Disk_C_Pct,Temperature_C,Status
2026-07-21 20:00:00,12.4,340,78.5,37.0,Homeostatic
2026-07-21 20:05:00,15.8,355,78.8,37.1,Homeostatic
2026-07-21 20:10:00,42.1,410,79.0,37.3,Hypoxic
2026-07-21 20:15:00,88.2,520,81.4,38.5,Feverish
2026-07-21 20:20:00,18.0,360,79.1,37.2,Conservation`,
          },
          {
            name: "nexus_config.json",
            path: "nexus_aos/data/nexus_config.json",
            type: "file",
            gitStatus: "M",
            content: `{
  "system": {
    "version": "13.0.4",
    "codename": "Sovereign-Alpha",
    "theme": "android_studio_dark"
  },
  "modules": [
    { "id": "mcp_server", "enabled": true, "port": 8080 },
    { "id": "vitals_patrol", "intervalMs": 1000 },
    { "id": "pet_3d_companion", "voiceSynthesis": true }
  ],
  "security": {
    "sandbox": true,
    "maxMemoryMB": 1024
  }
}`,
          },
        ],
      },
      {
        name: "docs",
        path: "nexus_aos/docs",
        type: "folder",
        children: [
          {
            name: "architecture_whitepaper.md",
            path: "nexus_aos/docs/architecture_whitepaper.md",
            type: "file",
            gitStatus: "none",
            content: `# Nexus-AOS System Architecture

> **Sovereign Operating System Kernel v13.0**

## Core Objectives
1. **Homeostatic Self-Healing**: Real-time telemetry monitoring for thermal and disk pressure.
2. **Dual-Interface Paradigm**: Seamless transition between Sovereign Command Line and LLM Core Workspace.
3. **MCP Tool Expansion**: Standardized Model Context Protocol integration.

### System Diagram
- \`L1_Explorer\`: Hierarchical file tree & directives
- \`L2_Editor\`: Multi-tab code editor, inbuilt browser, AI chat
- \`L3_Tools\`: MCP tool drawer, DB manager, Git graph
- \`L4_BottomBar\`: Terminal console, build pipelines, problems
`,
          },
          {
            name: "system_manual.pdf",
            path: "nexus_aos/docs/system_manual.pdf",
            type: "file",
            gitStatus: "none",
            content: `%PDF-1.7
1 0 obj
<< /Title (Nexus-AOS Sovereign User Manual)
   /Author (Nexus Kernel)
   /Subject (Operating Instructions) >>
endobj
2 0 obj
<< /Type /Page /Pages [Page 1, Page 2, Page 3] >>
endobj`,
          },
        ],
      },
      {
        name: "media",
        path: "nexus_aos/media",
        type: "folder",
        children: [
          {
            name: "startup_chime.mp3",
            path: "nexus_aos/media/startup_chime.mp3",
            type: "file",
            gitStatus: "none",
            content: "https://actions.google.com/sounds/v1/science_fiction/digital_scan.ogg",
          },
          {
            name: "cyber_kernel.mp4",
            path: "nexus_aos/media/cyber_kernel.mp4",
            type: "file",
            gitStatus: "none",
            content: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
          },
        ],
      },
    ],
  },
];

export const INITIAL_SERVICES: AOSService[] = [
  {
    name: "Pulse",
    description: "Heartbeat execution & temporal synchronizer",
    status: "online",
    uptime: "14h 22m",
    lastTick: "1.2s ago",
    logs: [
      "[09:14:02] Pulse tick #5201 completed in 1.4ms",
      "[09:14:03] Pulse tick #5202 completed in 1.2ms",
    ],
  },
  {
    name: "Guardian",
    description: "Self-healing & anomaly containment system",
    status: "online",
    uptime: "14h 22m",
    lastTick: "2.5s ago",
    logs: [
      "[09:12:00] Immune sweep clear. No toxic processes detected.",
      "[09:13:30] Memory hygiene verified.",
    ],
  },
  {
    name: "Senses",
    description: "FileSystem watcher & host environment listener",
    status: "online",
    uptime: "14h 22m",
    lastTick: "0.4s ago",
    logs: [
      "[09:14:00] FS change detected in /src/main.py",
      "[09:14:01] Re-indexing workspace AST...",
    ],
  },
  {
    name: "Orchestrator",
    description: "CPU loop agent coordinator & task scheduler",
    status: "online",
    uptime: "14h 20m",
    lastTick: "0.8s ago",
    logs: [
      "[09:10:00] Sub-task dispatch queue empty. Standing by.",
      "[09:13:10] Executed directive DIR-101.",
    ],
  },
  {
    name: "Supervisor",
    description: "Boot monitor & supervisor process",
    status: "online",
    uptime: "14h 22m",
    lastTick: "5.0s ago",
    logs: ["[09:00:00] Supervisor initialized host process PID 12452."],
  },
];

export const INITIAL_TOOLS: MCPTool[] = [
  {
    id: "tool_motor_exec",
    name: "motor_exec",
    category: "motor",
    description: "Execute terminal commands or code routines securely inside the sandboxed environment.",
    params: [
      { name: "command", type: "string", defaultVal: "python -m pytest", description: "Shell command line" },
      { name: "timeout", type: "number", defaultVal: "30", description: "Timeout in seconds" },
    ],
  },
  {
    id: "tool_lattice_query",
    name: "lattice_query",
    category: "lattice",
    description: "Query the code semantic graph for symbols, callers, and class dependencies.",
    params: [{ name: "query", type: "string", defaultVal: "OrchestratorEngine", description: "Symbol or class name" }],
  },
  {
    id: "tool_immune_scan",
    name: "immune_scan",
    category: "immune",
    description: "Run diagnostic vulnerability & disk bloat patrol.",
    params: [{ name: "mode", type: "string", defaultVal: "deep", description: "Scan mode: quick | deep | repair" }],
  },
  {
    id: "tool_memory_consolidate",
    name: "memory_consolidate",
    category: "memory",
    description: "Consolidate active context buffer into long-term wisdom artifacts.",
    params: [{ name: "target_tag", type: "string", defaultVal: "architecture_v1", description: "Wisdom tag" }],
  },
  {
    id: "tool_evolve_skill",
    name: "evolve_skill",
    category: "evolve",
    description: "Hot-load a new skill or optimize an existing execution kernel.",
    params: [{ name: "skill_name", type: "string", defaultVal: "disk_io_optimizer", description: "Target skill name" }],
  },
];

export const INITIAL_DB_TABLES: DBTable[] = [
  {
    name: "nexus_directives",
    rowsCount: 2,
    columns: ["id", "text", "status", "priority", "created_at"],
    data: [
      { id: "DIR-101", text: "Design Nexus App spec", status: "Completed", priority: "High", created_at: "2026-07-21 19:40:00" },
      { id: "DIR-102", text: "/patrol Run immune check", status: "Completed", priority: "Medium", created_at: "2026-07-21 19:48:00" },
    ],
  },
  {
    name: "vitals_history",
    rowsCount: 3,
    columns: ["id", "energy", "ischemia", "fever", "vibe", "timestamp"],
    data: [
      { id: 1, energy: 75, ischemia: 78.5, fever: 37.0, vibe: 0.20, timestamp: "2026-07-21 19:30:00" },
      { id: 2, energy: 76, ischemia: 79.0, fever: 37.1, vibe: 0.28, timestamp: "2026-07-21 19:40:00" },
      { id: 3, energy: 78, ischemia: 79.1, fever: 37.2, vibe: 0.34, timestamp: "2026-07-21 19:50:00" },
    ],
  },
  {
    name: "memory_artifacts",
    rowsCount: 2,
    columns: ["id", "tag", "summary", "tokens"],
    data: [
      { id: "MEM-01", tag: "sovereign_terminal_dna", summary: "Android Studio 4-quadrant architecture specs", tokens: 1240 },
      { id: "MEM-02", tag: "pet_companion_states", summary: "Dynamic facial expressions & endocrine coupling", tokens: 890 },
    ],
  },
];

export const INITIAL_GIT_COMMITS: GitCommit[] = [
  {
    hash: "a9f2c14",
    author: "Sovereign Master <user@nexus.aoi>",
    message: "feat: dual-interface specification & pet companion engine",
    date: "12 mins ago",
    branch: "main",
    isHead: true,
  },
  {
    hash: "b7e41d8",
    author: "Nexus-alpha <ai@nexus.aoi>",
    message: "core: synchronize homeostatic vitals protocol with host disk C",
    date: "45 mins ago",
    branch: "main",
  },
  {
    hash: "c3d100e",
    author: "Sovereign Master <user@nexus.aoi>",
    message: "init: bootstrap Nexus-AOS kernel v13.0",
    date: "2 hours ago",
    branch: "main",
  },
];

export const MOCK_PROCESSES: SystemProcess[] = [
  { name: "nexus_aos", pid: 12452, cpu: "12%", mem: "340M", path: "./mcp_server/python/" },
  { name: "chrome", pid: 8892, cpu: "8%", mem: "1.2G", path: "C:/Program Files/Google/Chrome/" },
  { name: "python", pid: 6731, cpu: "5%", mem: "210M", path: "./layers/L5_Reasoning/" },
  { name: "node (vite)", pid: 14092, cpu: "3%", mem: "180M", path: "/usr/local/bin/node" },
  { name: "code_runner", pid: 9912, cpu: "1%", mem: "95M", path: "./tools/runner" },
];

export const INITIAL_CHAT: ChatMessage[] = [
  {
    id: "chat-1",
    sender: "nexus",
    text: "Greeting Sovereign Master. I am Nexus-α, online and bound to this workspace. Both Sovereign Terminal and Nexus Core are synchronized.",
    timestamp: "19:50",
  },
];

export const INITIAL_CORE_STATE: CoreWorkspaceState = {
  focusFile: "nexus_aos/src/main.py",
  directiveBoard: {
    currentDirective: "Design & Execute Nexus App Dual-Interface Specification",
    subtasks: [
      { text: "L1 Explorer with Project, Directives & System tabs", done: true },
      { text: "L2 Center Code Editor, AI Chat, Diff & Docs", done: true },
      { text: "L3 Tools Panel with MCP, Playground, DB & Git", done: true },
      { text: "L4 Bottom Bar with Shell, Build & Problems", done: true },
      { text: "Pet companion dynamic state coupling", done: true },
    ],
    blockers: [],
  },
  openFiles: ["nexus_aos/src/main.py", "nexus_aos/src/sovereign_terminal.py"],
  activeSignals: [
    { signal: "⚡ Energy", level: "78%", source: "Metabolism", since: "Always", status: "Homeostatic" },
    { signal: "🩸 Ischemia", level: "79.1%", source: "Disk C", since: "14 min", status: "Conservation" },
    { signal: "💨 Hypoxia", level: "0%", source: "CPU", since: "—", status: "Normal" },
    { signal: "🔥 Fever", level: "37.2°C", source: "Immune", since: "—", status: "Normal" },
    { signal: "💚 Vibe", level: "+0.34", source: "Endocrine", since: "—", status: "Positive" },
  ],
  agents: [
    { name: "Orchestrator-01", type: "Coordinator", status: "Active", load: "12%" },
    { name: "Guardian-AOS", type: "Immune Patrol", status: "Active", load: "3%" },
    { name: "Motor-AOS", type: "Tool Executor", status: "Standby", load: "0%" },
  ],
  instincts: [
    { name: "Curiosity / Exploration", drive: "High", weight: 0.85 },
    { name: "Homeostatic Survival", drive: "High", weight: 0.90 },
    { name: "Code Precision", drive: "Maximum", weight: 0.98 },
  ],
  memoryStream: [
    { title: "Consolidation_20260721.md", file: "core/memory/consolidation_1.md", date: "10 mins ago", category: "Architecture" },
    { title: "Wisdom_Pet_Endocrine.md", file: "archive/learnings/endocrine.md", date: "1 hour ago", category: "Companion" },
  ],
  pulseLog: [
    { time: "19:50:01", text: "Pulse tick #5201 - Vitals homeostatic", category: "info" },
    { time: "19:50:15", text: "Senses: File change detected in main.py", category: "info" },
    { time: "19:51:02", text: "Immune: Checked Disk C status (79.1%)", category: "warn" },
  ],
};
