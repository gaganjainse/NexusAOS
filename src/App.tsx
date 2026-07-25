import { useEffect, useMemo, useState, type ReactNode } from "react"
import {
  Activity,
  Cpu,
  Dna,
  Pause,
  Play,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Workflow,
  Layers3,
} from "lucide-react"
import {
  createSeedGenome,
  derivePhenotype,
  mutateGenome,
  createRuntimeSnapshot,
  tickRuntime,
  type Genome,
  type RuntimeSnapshot,
} from "./core/nexus"

type CardProps = {
  title: string
  icon: ReactNode
  children: ReactNode
  tone?: "default" | "accent" | "muted"
}

function Card({ title, icon, children, tone = "default" }: CardProps) {
  const toneClasses =
    tone === "accent"
      ? "border-cyan-400/30 bg-cyan-400/10 shadow-[0_0_0_1px_rgba(34,211,238,0.12)]"
      : tone === "muted"
        ? "border-slate-700/80 bg-slate-900/70"
        : "border-white/10 bg-slate-950/70"

  return (
    <section className={`rounded-3xl border p-5 backdrop-blur-sm ${toneClasses}`}>
      <div className="mb-4 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-300">
          {icon}
        </div>
        <h2 className="text-base font-semibold tracking-tight text-slate-100">{title}</h2>
      </div>
      {children}
    </section>
  )
}

function SectionLabel({ children }: { children: ReactNode }) {
  return <p className="text-[11px] uppercase tracking-[0.25em] text-slate-400">{children}</p>
}

function MetricPill({
  label,
  value,
  accent = false,
}: {
  label: string
  value: string
  accent?: boolean
}) {
  return (
    <div
      className={`rounded-2xl border px-3 py-2 ${
        accent ? "border-cyan-400/25 bg-cyan-400/10" : "border-white/10 bg-white/5"
      }`}
    >
      <div className="text-[10px] uppercase tracking-[0.2em] text-slate-400">{label}</div>
      <div className="mt-1 text-sm font-medium text-slate-100">{value}</div>
    </div>
  )
}

function GenomeChip({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-3 py-2">
      <div className="text-[10px] uppercase tracking-[0.2em] text-slate-400">{label}</div>
      <div className="mt-1 text-sm font-medium text-slate-100">{value}</div>
    </div>
  )
}

export default function App() {
  const [genome, setGenome] = useState<Genome>(() => createSeedGenome())
  const [runtime, setRuntime] = useState<RuntimeSnapshot>(() => createRuntimeSnapshot())
  const [paused, setPaused] = useState(false)

  const phenotype = useMemo(() => derivePhenotype(genome), [genome])

  useEffect(() => {
    if (paused) return

    const timer = window.setInterval(() => {
      setRuntime((current) => tickRuntime(current, genome))
    }, 1600)

    return () => window.clearInterval(timer)
  }, [genome, paused])

  const handleMutate = () => {
    setGenome((current) => {
      const nextGenome = mutateGenome(current)
      setRuntime((prev) => ({
        ...prev,
        alerts: [`Genome mutated to version ${nextGenome.version}.`, ...prev.alerts].slice(0, 6),
      }))
      return nextGenome
    })
  }

  const handleReset = () => {
    setGenome(createSeedGenome())
    setRuntime(createRuntimeSnapshot())
    setPaused(false)
  }

  const togglePaused = () => setPaused((current) => !current)

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,#142038_0%,#090d16_42%,#06070b_100%)] text-slate-100">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-6 px-4 py-4 sm:px-6 lg:px-8">
        <header className="rounded-3xl border border-white/10 bg-slate-950/70 p-5 shadow-2xl shadow-black/25 backdrop-blur">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.22em] text-cyan-200">
                <Dna className="h-3.5 w-3.5" />
                NexusAOS v2 Recovery Build
              </div>
              <div>
                <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
                  Genome-driven cognitive shell.
                </h1>
                <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
                  A clean implementation of the recovery blueprint: a structured genome, an
                  explicit runtime loop, a hard governance layer, and a visible evolution path.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <MetricPill label="Genome" value={`v${genome.version}`} accent />
              <MetricPill label="Runtime" value={`Tick ${runtime.tick}`} />
              <MetricPill label="Energy" value={`${runtime.energy}%`} />
              <MetricPill label="Policy" value={runtime.governanceState} />
            </div>
          </div>
        </header>

        <section className="grid gap-4 xl:grid-cols-[1.15fr_1fr_1fr]">
          <Card title="Genome" icon={<Dna className="h-5 w-5" />} tone="accent">
            <div className="grid gap-3 sm:grid-cols-2">
              <GenomeChip label="Identity" value={`${genome.name} • ${genome.id}`} />
              <GenomeChip label="Version" value={`v${genome.version}`} />
              <GenomeChip label="Sensory" value={genome.sensory.modalities.join(", ")} />
              <GenomeChip
                label="Planner"
                value={`${genome.planner.strategy} / depth ${genome.planner.depth}`}
              />
              <GenomeChip label="Memory" value={`${genome.memory.episodicSlots} episodic slots`} />
              <GenomeChip label="Governance" value={genome.governance.mode} />
            </div>

            <div className="mt-5 space-y-3">
              <SectionLabel>Genome sections</SectionLabel>
              <div className="space-y-3">
                {[
                  ["Sensory", genome.sensory.description],
                  ["Memory", genome.memory.description],
                  ["Planner", genome.planner.description],
                  ["Tools", genome.tools.allowed.join(", ")],
                  ["Governance", genome.governance.description],
                  ["Evolution", genome.evolution.description],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-2xl border border-white/10 bg-white/5 p-3">
                    <div className="text-xs uppercase tracking-[0.2em] text-slate-400">{label}</div>
                    <div className="mt-1 text-sm leading-6 text-slate-200">{value}</div>
                  </div>
                ))}
              </div>
            </div>
          </Card>

          <Card title="Runtime" icon={<Workflow className="h-5 w-5" />}>
            <div className="space-y-4">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <SectionLabel>Current stage</SectionLabel>
                    <div className="mt-1 text-2xl font-semibold text-white">{runtime.stage}</div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-slate-950/70 px-3 py-2 text-right">
                    <div className="text-[10px] uppercase tracking-[0.2em] text-slate-400">Action</div>
                    <div className="mt-1 text-sm font-medium text-cyan-200">{runtime.lastAction}</div>
                  </div>
                </div>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-cyan-400 via-sky-400 to-indigo-400 transition-all duration-500"
                    style={{ width: `${runtime.energy}%` }}
                  />
                </div>

                <div className="mt-3 grid grid-cols-2 gap-3">
                  <MetricPill label="Last result" value={runtime.lastResult} />
                  <MetricPill label="Memory pressure" value={`${runtime.memoryPressure}%`} />
                </div>
              </div>

              <div className="grid gap-3 sm:grid-cols-2">
                <MetricPill label="Working memory" value={`${genome.memory.workingSlots} slots`} />
                <MetricPill label="Episodic memory" value={`${genome.memory.episodicSlots} slots`} />
                <MetricPill label="Semantic memory" value={`${genome.memory.semanticSlots} slots`} />
                <MetricPill label="Tool budget" value={`${genome.tools.maxCallsPerTurn} calls / turn`} />
              </div>

              <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
                <SectionLabel>Execution log</SectionLabel>
                <div className="mt-3 space-y-2 text-sm">
                  {runtime.log.slice(0, 5).map((entry, index) => (
                    <div
                      key={index}
                      className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-slate-200"
                    >
                      {entry}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          <Card title="Governance" icon={<ShieldCheck className="h-5 w-5" />}>
            <div className="space-y-4">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <SectionLabel>Policy state</SectionLabel>
                <div className="mt-2 text-xl font-semibold text-white">{runtime.governanceState}</div>
                <p className="mt-2 text-sm leading-6 text-slate-300">
                  Governance stays separate from runtime. Any forbidden action becomes a logged
                  failure instead of a hidden mutation.
                </p>
              </div>

              <div className="grid gap-3">
                <MetricPill label="Blocked actions" value={genome.governance.blockedActions.join(", ")} />
                <MetricPill label="Permissions" value={genome.tools.allowed.join(", ")} />
                <MetricPill label="Safety mode" value={genome.governance.safetyMode} accent />
              </div>

              <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4">
                <SectionLabel>Alerts</SectionLabel>
                <div className="mt-3 space-y-2 text-sm">
                  {runtime.alerts.length === 0 ? (
                    <div className="rounded-xl border border-dashed border-white/10 px-3 py-2 text-slate-400">
                      No active alerts.
                    </div>
                  ) : (
                    runtime.alerts.map((entry, index) => (
                      <div
                        key={index}
                        className="rounded-xl border border-amber-400/20 bg-amber-400/10 px-3 py-2 text-amber-100"
                      >
                        {entry}
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </Card>
        </section>

        <section className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
          <Card title="Controls" icon={<Cpu className="h-5 w-5" />}>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={togglePaused}
                className="inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-slate-100 transition hover:border-cyan-400/30 hover:bg-cyan-400/10"
              >
                {paused ? <Play className="h-4 w-4" /> : <Pause className="h-4 w-4" />}
                {paused ? "Resume runtime" : "Pause runtime"}
              </button>
              <button
                onClick={handleMutate}
                className="inline-flex items-center gap-2 rounded-2xl border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-sm font-medium text-cyan-100 transition hover:bg-cyan-400/20"
              >
                <Sparkles className="h-4 w-4" />
                Mutate genome
              </button>
              <button
                onClick={handleReset}
                className="inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-slate-100 transition hover:border-white/20 hover:bg-white/10"
              >
                <RefreshCw className="h-4 w-4" />
                Reset seed
              </button>
            </div>

            <div className="mt-5 grid gap-3 md:grid-cols-3">
              <MetricPill label="Compute budget" value={`${phenotype.computeBudget} units`} />
              <MetricPill label="Mutation pressure" value={`${Math.round(phenotype.mutationPressure * 100)}%`} />
              <MetricPill label="Trace depth" value={`${phenotype.traceDepth} steps`} />
            </div>

            <div className="mt-5 rounded-2xl border border-white/10 bg-slate-950/70 p-4">
              <SectionLabel>Implementation note</SectionLabel>
              <p className="mt-2 text-sm leading-6 text-slate-300">
                This shell intentionally keeps the genome structured, the runtime explicit, and
                governance outside the mutation path. That is the first usable recovery layer.
              </p>
            </div>
          </Card>

          <Card title="System map" icon={<Layers3 className="h-5 w-5" />}>
            <div className="space-y-3">
              {[
                ["Genome", "Declarative architecture and policy"],
                ["Expression", "Builds phenotype from genome"],
                ["Runtime", "Observe → plan → act → log"],
                ["Memory", "Working, episodic, semantic"],
                ["Governance", "Hard stop for unsafe actions"],
                ["Evolution", "Offline mutation and selection"],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl border border-white/10 bg-white/5 p-3">
                  <div className="text-sm font-medium text-white">{label}</div>
                  <div className="mt-1 text-sm leading-6 text-slate-300">{value}</div>
                </div>
              ))}
            </div>

            <div className="mt-4 rounded-2xl border border-emerald-400/20 bg-emerald-400/10 p-4">
              <div className="flex items-center gap-2 text-sm font-medium text-emerald-100">
                <Activity className="h-4 w-4" />
                Build status
              </div>
              <p className="mt-2 text-sm leading-6 text-emerald-50/90">
                The repository now has a canonical starting point instead of mythology-heavy
                scaffolding.
              </p>
            </div>
          </Card>
        </section>

        <footer className="pb-4 text-center text-xs uppercase tracking-[0.25em] text-slate-500">
          NexusAOS recovery phase 1 · structured genome · explicit runtime · separated governance
        </footer>
      </div>
    </main>
  )
}
