export type PlannerStrategy = "greedy" | "beam" | "tree"
export type GovernanceMode = "strict" | "balanced" | "sandbox"
export type RuntimeStage = "observe" | "recall" | "plan" | "act" | "validate" | "learn"
export type GovernanceState = "ready" | "constrained" | "alert"

export interface Genome {
  id: string
  name: string
  version: number
  sensory: {
    modalities: string[]
    description: string
  }
  memory: {
    working_slots: number
    episodic_slots: number
    semantic_slots: number
    description: string
  }
  planner: {
    strategy: PlannerStrategy
    depth: number
    description: string
  }
  tools: {
    allowed: string[]
    max_calls_per_turn: number
  }
  governance: {
    mode: GovernanceMode
    safety_mode: string
    blocked_actions: string[]
    description: string
  }
  evolution: {
    mutation_rate: number
    crossover_rate: number
    selection_size: number
    description: string
  }
}

export interface Phenotype {
  compute_budget: number
  mutation_pressure: number
  trace_depth: number
}

export interface RuntimeSnapshot {
  tick: number
  energy: number
  stage: RuntimeStage
  last_action: string
  last_result: string
  memory_pressure: number
  governance_state: GovernanceState
  log: string[]
  alerts: string[]
}

export interface DashboardSnapshot {
  genome: Genome
  runtime: RuntimeSnapshot
  phenotype: Phenotype
}
