import { invoke } from "@tauri-apps/api/core"
import type { DashboardSnapshot } from "./types"

type AppState = {
  snapshot: DashboardSnapshot | null
  paused: boolean
  busy: boolean
  intervalId: number | null
}

const state: AppState = {
  snapshot: null,
  paused: false,
  busy: false,
  intervalId: null,
}

const root = document.getElementById("root")
if (!root) {
  throw new Error("Missing root element")
}

function stopLoop() {
  if (state.intervalId !== null) {
    window.clearInterval(state.intervalId)
    state.intervalId = null
  }
}

function startLoop() {
  stopLoop()
  state.intervalId = window.setInterval(() => {
    if (state.paused || state.busy || !state.snapshot) return
    void refreshFromBackend("tick_state")
  }, 1400)
}

async function refreshFromBackend(command: "snapshot" | "tick_state" | "mutate_genome" | "reset_state") {
  state.busy = true
  try {
    state.snapshot = await invoke<DashboardSnapshot>(command)
    render()
  } finally {
    state.busy = false
  }
}

function renderLoading(message: string) {
  root.innerHTML = `
    <div class="page-shell">
      <header class="hero panel">
        <div class="badge">NexusAOS v2 Recovery Build</div>
        <h1>Loading runtime…</h1>
        <p>${message}</p>
      </header>
    </div>
  `
}

function render() {
  if (!state.snapshot) {
    renderLoading("Fetching the Rust backend snapshot.")
    return
  }

  const { genome, runtime, phenotype } = state.snapshot

  root.innerHTML = `
    <div class="page-shell">
      <header class="hero panel">
        <div class="hero-top">
          <div>
            <div class="badge">NexusAOS v2 Recovery Build</div>
            <h1>Genome-driven cognitive shell</h1>
            <p>
              Rust runtime, Tauri desktop shell, and a minimal TypeScript dashboard.
              The genome is structured, runtime is explicit, and governance is fail-closed.
            </p>
          </div>
          <div class="stats-grid">
            <div class="stat"><span>Genome</span><strong>v${genome.version}</strong></div>
            <div class="stat"><span>Tick</span><strong>${runtime.tick}</strong></div>
            <div class="stat"><span>Energy</span><strong>${runtime.energy}%</strong></div>
            <div class="stat"><span>Policy</span><strong>${runtime.governance_state}</strong></div>
          </div>
        </div>
      </header>

      <section class="layout-3">
        <article class="panel card accent">
          <h2>Genome</h2>
          <div class="grid-2">
            <div class="field"><label>Identity</label><div>${genome.name} · ${genome.id}</div></div>
            <div class="field"><label>Version</label><div>v${genome.version}</div></div>
            <div class="field"><label>Sensory</label><div>${genome.sensory.modalities.join(", ")}</div></div>
            <div class="field"><label>Planner</label><div>${genome.planner.strategy} / depth ${genome.planner.depth}</div></div>
            <div class="field"><label>Memory</label><div>${genome.memory.episodic_slots} episodic slots</div></div>
            <div class="field"><label>Governance</label><div>${genome.governance.mode}</div></div>
          </div>
          <div class="subsection">
            <div class="section-title">Genome sections</div>
            <div class="stack">
              <div class="item"><span>Sensory</span><p>${genome.sensory.description}</p></div>
              <div class="item"><span>Memory</span><p>${genome.memory.description}</p></div>
              <div class="item"><span>Planner</span><p>${genome.planner.description}</p></div>
              <div class="item"><span>Tools</span><p>${genome.tools.allowed.join(", ")}</p></div>
              <div class="item"><span>Governance</span><p>${genome.governance.description}</p></div>
              <div class="item"><span>Evolution</span><p>${genome.evolution.description}</p></div>
            </div>
          </div>
        </article>

        <article class="panel card">
          <h2>Runtime</h2>
          <div class="runtime-box">
            <div>
              <div class="section-title">Current stage</div>
              <div class="stage">${runtime.stage}</div>
            </div>
            <div class="action-box">
              <div>Action</div>
              <strong>${runtime.last_action}</strong>
            </div>
          </div>
          <div class="energy-bar"><div style="width:${runtime.energy}%"></div></div>
          <div class="metrics">
            <div class="stat"><span>Last result</span><strong>${runtime.last_result}</strong></div>
            <div class="stat"><span>Memory pressure</span><strong>${runtime.memory_pressure}%</strong></div>
            <div class="stat"><span>Working memory</span><strong>${genome.memory.working_slots}</strong></div>
            <div class="stat"><span>Trace depth</span><strong>${phenotype.trace_depth}</strong></div>
          </div>
          <div class="subsection">
            <div class="section-title">Execution log</div>
            <div class="stack compact">
              ${runtime.log.slice(0, 5).map((entry) => `<div class="item log">${entry}</div>`).join("")}
            </div>
          </div>
        </article>

        <article class="panel card">
          <h2>Governance</h2>
          <div class="field large">
            <label>Policy state</label>
            <div class="policy ${runtime.governance_state}">${runtime.governance_state}</div>
            <p>Governance is separate from runtime. Forbidden actions are logged instead of silently executed.</p>
          </div>
          <div class="metrics">
            <div class="stat"><span>Blocked</span><strong>${genome.governance.blocked_actions.length}</strong></div>
            <div class="stat"><span>Permissions</span><strong>${genome.tools.allowed.length}</strong></div>
            <div class="stat"><span>Safety mode</span><strong>${genome.governance.safety_mode}</strong></div>
            <div class="stat"><span>Mutation</span><strong>${Math.round(phenotype.mutation_pressure * 100)}%</strong></div>
          </div>
          <div class="subsection">
            <div class="section-title">Alerts</div>
            <div class="stack compact">
              ${runtime.alerts.length === 0 ? `<div class="item empty">No active alerts.</div>` : runtime.alerts.map((entry) => `<div class="item alert">${entry}</div>`).join("")}
            </div>
          </div>
        </article>
      </section>

      <section class="layout-2">
        <article class="panel card">
          <h2>Controls</h2>
          <div class="controls">
            <button id="toggle">${state.paused ? "Resume runtime" : "Pause runtime"}</button>
            <button id="mutate" class="primary">Mutate genome</button>
            <button id="reset">Reset seed</button>
          </div>
          <div class="metrics">
            <div class="stat"><span>Compute budget</span><strong>${phenotype.compute_budget}</strong></div>
            <div class="stat"><span>Mutation pressure</span><strong>${Math.round(phenotype.mutation_pressure * 100)}%</strong></div>
            <div class="stat"><span>Tool budget</span><strong>${genome.tools.max_calls_per_turn}</strong></div>
            <div class="stat"><span>Semantic memory</span><strong>${genome.memory.semantic_slots}</strong></div>
          </div>
        </article>

        <article class="panel card">
          <h2>System map</h2>
          <div class="stack">
            <div class="item"><span>Genome</span><p>Declarative architecture and policy</p></div>
            <div class="item"><span>Expression</span><p>Builds phenotype from genome</p></div>
            <div class="item"><span>Runtime</span><p>Observe → plan → act → log</p></div>
            <div class="item"><span>Memory</span><p>Working, episodic, semantic</p></div>
            <div class="item"><span>Governance</span><p>Hard stop for unsafe actions</p></div>
            <div class="item"><span>Evolution</span><p>Offline mutation and selection</p></div>
          </div>
        </article>
      </section>

      <footer class="footer">NexusAOS recovery phase 1 · Rust runtime · Tauri shell · vanilla TypeScript UI</footer>
    </div>
  `

  const toggle = document.getElementById("toggle")
  const mutate = document.getElementById("mutate")
  const reset = document.getElementById("reset")

  toggle?.addEventListener("click", () => {
    state.paused = !state.paused
    render()
  })

  mutate?.addEventListener("click", () => {
    void refreshFromBackend("mutate_genome")
  })

  reset?.addEventListener("click", () => {
    state.paused = false
    void refreshFromBackend("reset_state")
  })
}

async function bootstrap() {
  await refreshFromBackend("snapshot")
  startLoop()
}

bootstrap().catch((error) => {
  console.error(error)
  renderLoading("Failed to load the backend runtime.")
})
