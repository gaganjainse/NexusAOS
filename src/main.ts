import {
  createRuntimeSnapshot,
  createSeedGenome,
  derivePhenotype,
  mutateGenome,
  tickRuntime,
  type Genome,
  type RuntimeSnapshot,
} from "./core/nexus"

type AppState = {
  genome: Genome
  runtime: RuntimeSnapshot
  paused: boolean
  intervalId: number | null
}

const state: AppState = {
  genome: createSeedGenome(),
  runtime: createRuntimeSnapshot(),
  paused: false,
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
    if (state.paused) return
    state.runtime = tickRuntime(state.runtime, state.genome)
    render()
  }, 1400)
}

function formatList(items: string[]) {
  return items.map((item) => `<span class="chip">${item}</span>`).join("")
}

function render() {
  const phenotype = derivePhenotype(state.genome)

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
            <div class="stat"><span>Genome</span><strong>v${state.genome.version}</strong></div>
            <div class="stat"><span>Tick</span><strong>${state.runtime.tick}</strong></div>
            <div class="stat"><span>Energy</span><strong>${state.runtime.energy}%</strong></div>
            <div class="stat"><span>Policy</span><strong>${state.runtime.governanceState}</strong></div>
          </div>
        </div>
      </header>

      <section class="layout-3">
        <article class="panel card accent">
          <h2>Genome</h2>
          <div class="grid-2">
            <div class="field"><label>Identity</label><div>${state.genome.name} · ${state.genome.id}</div></div>
            <div class="field"><label>Version</label><div>v${state.genome.version}</div></div>
            <div class="field"><label>Sensory</label><div>${state.genome.sensory.modalities.join(", ")}</div></div>
            <div class="field"><label>Planner</label><div>${state.genome.planner.strategy} / depth ${state.genome.planner.depth}</div></div>
            <div class="field"><label>Memory</label><div>${state.genome.memory.episodicSlots} episodic slots</div></div>
            <div class="field"><label>Governance</label><div>${state.genome.governance.mode}</div></div>
          </div>
          <div class="subsection">
            <div class="section-title">Genome sections</div>
            <div class="stack">
              <div class="item"><span>Sensory</span><p>${state.genome.sensory.description}</p></div>
              <div class="item"><span>Memory</span><p>${state.genome.memory.description}</p></div>
              <div class="item"><span>Planner</span><p>${state.genome.planner.description}</p></div>
              <div class="item"><span>Tools</span><p>${state.genome.tools.allowed.join(", ")}</p></div>
              <div class="item"><span>Governance</span><p>${state.genome.governance.description}</p></div>
              <div class="item"><span>Evolution</span><p>${state.genome.evolution.description}</p></div>
            </div>
          </div>
        </article>

        <article class="panel card">
          <h2>Runtime</h2>
          <div class="runtime-box">
            <div>
              <div class="section-title">Current stage</div>
              <div class="stage">${state.runtime.stage}</div>
            </div>
            <div class="action-box">
              <div>Action</div>
              <strong>${state.runtime.lastAction}</strong>
            </div>
          </div>
          <div class="energy-bar"><div style="width:${state.runtime.energy}%"></div></div>
          <div class="metrics">
            <div class="stat"><span>Last result</span><strong>${state.runtime.lastResult}</strong></div>
            <div class="stat"><span>Memory pressure</span><strong>${state.runtime.memoryPressure}%</strong></div>
            <div class="stat"><span>Working memory</span><strong>${state.genome.memory.workingSlots}</strong></div>
            <div class="stat"><span>Trace depth</span><strong>${phenotype.traceDepth}</strong></div>
          </div>
          <div class="subsection">
            <div class="section-title">Execution log</div>
            <div class="stack compact">
              ${state.runtime.log.slice(0, 5).map((entry) => `<div class="item log">${entry}</div>`).join("")}
            </div>
          </div>
        </article>

        <article class="panel card">
          <h2>Governance</h2>
          <div class="field large">
            <label>Policy state</label>
            <div class="policy ${state.runtime.governanceState.toLowerCase()}">${state.runtime.governanceState}</div>
            <p>Governance is separate from runtime. Forbidden actions are logged instead of silently executed.</p>
          </div>
          <div class="metrics">
            <div class="stat"><span>Blocked</span><strong>${state.genome.governance.blockedActions.length}</strong></div>
            <div class="stat"><span>Permissions</span><strong>${state.genome.tools.allowed.length}</strong></div>
            <div class="stat"><span>Safety mode</span><strong>${state.genome.governance.safetyMode}</strong></div>
            <div class="stat"><span>Mutation</span><strong>${Math.round(phenotype.mutationPressure * 100)}%</strong></div>
          </div>
          <div class="subsection">
            <div class="section-title">Alerts</div>
            <div class="stack compact">
              ${
                state.runtime.alerts.length === 0
                  ? `<div class="item empty">No active alerts.</div>`
                  : state.runtime.alerts.map((entry) => `<div class="item alert">${entry}</div>`).join("")
              }
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
            <div class="stat"><span>Compute budget</span><strong>${phenotype.computeBudget}</strong></div>
            <div class="stat"><span>Mutation pressure</span><strong>${Math.round(phenotype.mutationPressure * 100)}%</strong></div>
            <div class="stat"><span>Tool budget</span><strong>${state.genome.tools.maxCallsPerTurn}</strong></div>
            <div class="stat"><span>Semantic memory</span><strong>${state.genome.memory.semanticSlots}</strong></div>
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
    state.genome = mutateGenome(state.genome)
    state.runtime = {
      ...state.runtime,
      alerts: [`Genome mutated to version ${state.genome.version}.`, ...state.runtime.alerts].slice(0, 6),
    }
    render()
  })

  reset?.addEventListener("click", () => {
    state.genome = createSeedGenome()
    state.runtime = createRuntimeSnapshot()
    state.paused = false
    render()
  })
}

render()
startLoop()
