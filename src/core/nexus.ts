export type Genome = {
  id: string
  name: string
  version: number
  sensory: {
    modalities: string[]
    description: string
  }
  memory: {
    workingSlots: number
    episodicSlots: number
    semanticSlots: number
    description: string
  }
  planner: {
    strategy: "greedy" | "beam" | "tree"
    depth: number
    description: string
  }
  tools: {
    allowed: string[]
    maxCallsPerTurn: number
  }
  governance: {
    mode: "strict" | "balanced" | "sandbox"
    safetyMode: string
    blockedActions: string[]
    description: string
  }
  evolution: {
    mutationRate: number
    crossoverRate: number
    selectionSize: number
    description: string
  }
}

export type RuntimeStage = "observe" | "recall" | "plan" | "act" | "validate" | "learn"

export type RuntimeSnapshot = {
  tick: number
  energy: number
  stage: RuntimeStage
  lastAction: string
  lastResult: string
  memoryPressure: number
  governanceState: "Ready" | "Constrained" | "Alert"
  log: string[]
  alerts: string[]
}

export type Phenotype = {
  computeBudget: number
  mutationPressure: number
  traceDepth: number
}

const STAGES: RuntimeStage[] = ["observe", "recall", "plan", "act", "validate", "learn"]

function clamp(value: number, min: number, max: number) {
  return Math.max(min, Math.min(max, value))
}

function seededValue(seed: number) {
  const x = Math.sin(seed) * 10000
  return x - Math.floor(x)
}

export function createSeedGenome(): Genome {
  return {
    id: "NX-0001",
    name: "Nexus Genome",
    version: 1,
    sensory: {
      modalities: ["text", "files", "signals"],
      description: "Structured inputs only. No hidden channels.",
    },
    memory: {
      workingSlots: 8,
      episodicSlots: 64,
      semanticSlots: 16,
      description: "Working, episodic, and semantic memory are separate stores.",
    },
    planner: {
      strategy: "beam",
      depth: 3,
      description: "Small bounded search with explicit confidence and traceability.",
    },
    tools: {
      allowed: ["read", "write", "search"],
      maxCallsPerTurn: 3,
    },
    governance: {
      mode: "strict",
      safetyMode: "fail-closed",
      blockedActions: ["self-modify-rules", "silent-delete", "tool-escalation"],
      description: "Governance is immutable at runtime.",
    },
    evolution: {
      mutationRate: 0.08,
      crossoverRate: 0.5,
      selectionSize: 4,
      description: "Offline mutation and selection only.",
    },
  }
}

export function derivePhenotype(genome: Genome): Phenotype {
  const computeBudget =
    genome.memory.workingSlots * 2 +
    genome.memory.episodicSlots / 8 +
    genome.planner.depth * 10

  const mutationPressure = clamp(genome.evolution.mutationRate, 0, 1)
  const traceDepth = genome.planner.depth + genome.tools.allowed.length

  return {
    computeBudget: Math.round(computeBudget),
    mutationPressure,
    traceDepth,
  }
}

export function createRuntimeSnapshot(): RuntimeSnapshot {
  return {
    tick: 0,
    energy: 100,
    stage: "observe",
    lastAction: "Initialize genome",
    lastResult: "System ready",
    memoryPressure: 12,
    governanceState: "Ready",
    log: ["Genome loaded.", "Runtime initialized.", "Governance armed."],
    alerts: [],
  }
}

export function tickRuntime(snapshot: RuntimeSnapshot, genome: Genome): RuntimeSnapshot {
  const nextTick = snapshot.tick + 1
  const stage = STAGES[nextTick % STAGES.length]
  const energyDrain = genome.planner.depth * 0.6 + genome.memory.workingSlots * 0.15
  const nextEnergy = clamp(snapshot.energy - energyDrain + (stage === "learn" ? 1.2 : 0), 0, 100)
  const memoryPressure = clamp(snapshot.memoryPressure + (stage === "recall" ? 2 : -1), 0, 100)

  const lastActionMap: Record<RuntimeStage, string> = {
    observe: "Read environment",
    recall: "Fetch episodic memory",
    plan: "Assemble bounded plan",
    act: "Execute permitted action",
    validate: "Check policy and result",
    learn: "Write experience summary",
  }

  const lastResultMap: Record<RuntimeStage, string> = {
    observe: "Input sampled",
    recall: "Relevant memory restored",
    plan: "Plan bounded",
    act: "Action completed",
    validate: "Policy checked",
    learn: "Experience stored",
  }

  const nextLog = [
    `${String(nextTick).padStart(3, "0")} · ${stage} · ${lastResultMap[stage]}`,
    ...snapshot.log,
  ].slice(0, 6)

  const alerts = [...snapshot.alerts]
  let governanceState: RuntimeSnapshot["governanceState"] = "Ready"

  if (memoryPressure > 75) {
    alerts.unshift("Memory pressure exceeded safe threshold.")
    governanceState = "Constrained"
  }

  if (nextEnergy < 20) {
    alerts.unshift("Energy low. System is conserving compute.")
    governanceState = "Constrained"
  }

  if (stage === "act" && genome.governance.mode === "strict" && !genome.tools.allowed.includes("write")) {
    alerts.unshift("Attempted restricted action was blocked.")
    governanceState = "Alert"
  }

  return {
    tick: nextTick,
    energy: Math.round(nextEnergy),
    stage,
    lastAction: lastActionMap[stage],
    lastResult: lastResultMap[stage],
    memoryPressure: Math.round(memoryPressure),
    governanceState,
    log: nextLog,
    alerts: alerts.slice(0, 6),
  }
}

export function mutateGenome(genome: Genome): Genome {
  const seed = genome.version * 97
  const roll = seededValue(seed)

  const nextVersion = genome.version + 1
  const workingDelta = roll > 0.66 ? 1 : roll < 0.33 ? -1 : 0
  const plannerDelta = roll > 0.5 ? 1 : 0
  const mutationRateDelta = (seededValue(seed + 1) - 0.5) * 0.04

  const allowed = [...genome.tools.allowed]
  if (roll > 0.7 && !allowed.includes("inspect")) allowed.push("inspect")
  if (roll < 0.2 && allowed.length > 2) allowed.splice(allowed.indexOf("search"), 1)

  return {
    ...genome,
    version: nextVersion,
    memory: {
      ...genome.memory,
      workingSlots: clamp(genome.memory.workingSlots + workingDelta, 4, 32),
      episodicSlots: clamp(genome.memory.episodicSlots + (roll > 0.8 ? 8 : -4), 32, 128),
      semanticSlots: clamp(genome.memory.semanticSlots + (roll > 0.5 ? 2 : 0), 8, 64),
    },
    planner: {
      ...genome.planner,
      depth: clamp(genome.planner.depth + plannerDelta, 1, 6),
      strategy: roll > 0.75 ? "tree" : genome.planner.strategy,
    },
    tools: {
      ...genome.tools,
      allowed,
      maxCallsPerTurn: clamp(genome.tools.maxCallsPerTurn + (roll > 0.85 ? 1 : 0), 1, 6),
    },
    evolution: {
      ...genome.evolution,
      mutationRate: clamp(genome.evolution.mutationRate + mutationRateDelta, 0.01, 0.2),
      selectionSize: clamp(genome.evolution.selectionSize + (roll > 0.9 ? 1 : 0), 2, 8),
    },
  }
}
