use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Genome {
    pub id: String,
    pub name: String,
    pub version: u32,
    pub sensory: SensoryGene,
    pub memory: MemoryGene,
    pub planner: PlannerGene,
    pub tools: ToolGene,
    pub governance: GovernanceGene,
    pub evolution: EvolutionGene,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SensoryGene {
    pub modalities: Vec<String>,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryGene {
    pub working_slots: u32,
    pub episodic_slots: u32,
    pub semantic_slots: u32,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlannerGene {
    pub strategy: PlannerStrategy,
    pub depth: u32,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum PlannerStrategy {
    Greedy,
    Beam,
    Tree,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolGene {
    pub allowed: Vec<String>,
    pub max_calls_per_turn: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernanceGene {
    pub mode: GovernanceMode,
    pub safety_mode: String,
    pub blocked_actions: Vec<String>,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum GovernanceMode {
    Strict,
    Balanced,
    Sandbox,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvolutionGene {
    pub mutation_rate: f64,
    pub crossover_rate: f64,
    pub selection_size: u32,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Phenotype {
    pub compute_budget: u32,
    pub mutation_pressure: f64,
    pub trace_depth: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RuntimeStage {
    Observe,
    Recall,
    Plan,
    Act,
    Validate,
    Learn,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RuntimeSnapshot {
    pub tick: u32,
    pub energy: u32,
    pub stage: RuntimeStage,
    pub last_action: String,
    pub last_result: String,
    pub memory_pressure: u32,
    pub governance_state: GovernanceState,
    pub log: Vec<String>,
    pub alerts: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum GovernanceState {
    Ready,
    Constrained,
    Alert,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DashboardSnapshot {
    pub genome: Genome,
    pub runtime: RuntimeSnapshot,
    pub phenotype: Phenotype,
}

impl Default for Genome {
    fn default() -> Self {
        Self {
            id: "NX-0001".to_string(),
            name: "Nexus Genome".to_string(),
            version: 1,
            sensory: SensoryGene {
                modalities: vec!["text".to_string(), "files".to_string(), "signals".to_string()],
                description: "Structured inputs only. No hidden channels.".to_string(),
            },
            memory: MemoryGene {
                working_slots: 8,
                episodic_slots: 64,
                semantic_slots: 16,
                description: "Working, episodic, and semantic memory are separate stores.".to_string(),
            },
            planner: PlannerGene {
                strategy: PlannerStrategy::Beam,
                depth: 3,
                description: "Small bounded search with explicit confidence and traceability.".to_string(),
            },
            tools: ToolGene {
                allowed: vec!["read".to_string(), "write".to_string(), "search".to_string()],
                max_calls_per_turn: 3,
            },
            governance: GovernanceGene {
                mode: GovernanceMode::Strict,
                safety_mode: "fail-closed".to_string(),
                blocked_actions: vec![
                    "self-modify-rules".to_string(),
                    "silent-delete".to_string(),
                    "tool-escalation".to_string(),
                ],
                description: "Governance is immutable at runtime.".to_string(),
            },
            evolution: EvolutionGene {
                mutation_rate: 0.08,
                crossover_rate: 0.5,
                selection_size: 4,
                description: "Offline mutation and selection only.".to_string(),
            },
        }
    }
}

impl Genome {
    pub fn derive_phenotype(&self) -> Phenotype {
        let compute_budget = self.memory.working_slots * 2 + self.memory.episodic_slots / 8 + self.planner.depth * 10;
        let trace_depth = self.planner.depth + self.tools.allowed.len() as u32;
        Phenotype {
            compute_budget,
            mutation_pressure: self.evolution.mutation_rate.clamp(0.0, 1.0),
            trace_depth,
        }
    }

    pub fn mutate(&self) -> Self {
        let next_version = self.version + 1;
        let working_slots = self.memory.working_slots.saturating_add(1).clamp(4, 32);
        let episodic_slots = self.memory.episodic_slots.saturating_add(8).clamp(32, 128);
        let semantic_slots = self.memory.semantic_slots.saturating_add(2).clamp(8, 64);
        let planner_depth = self.planner.depth.saturating_add(1).clamp(1, 6);
        let selection_size = self.evolution.selection_size.saturating_add(1).clamp(2, 8);

        let mut allowed = self.tools.allowed.clone();
        if !allowed.iter().any(|item| item == "inspect") {
            allowed.push("inspect".to_string());
        }

        Self {
            version: next_version,
            memory: MemoryGene {
                working_slots,
                episodic_slots,
                semantic_slots,
                ..self.memory.clone()
            },
            planner: PlannerGene {
                depth: planner_depth,
                strategy: PlannerStrategy::Tree,
                ..self.planner.clone()
            },
            tools: ToolGene {
                allowed,
                max_calls_per_turn: self.tools.max_calls_per_turn.saturating_add(1).clamp(1, 6),
            },
            evolution: EvolutionGene {
                mutation_rate: (self.evolution.mutation_rate + 0.01).clamp(0.01, 0.20),
                crossover_rate: self.evolution.crossover_rate,
                selection_size,
                ..self.evolution.clone()
            },
            ..self.clone()
        }
    }
}

impl Default for RuntimeSnapshot {
    fn default() -> Self {
        Self {
            tick: 0,
            energy: 100,
            stage: RuntimeStage::Observe,
            last_action: "Initialize genome".to_string(),
            last_result: "System ready".to_string(),
            memory_pressure: 12,
            governance_state: GovernanceState::Ready,
            log: vec![
                "Genome loaded.".to_string(),
                "Runtime initialized.".to_string(),
                "Governance armed.".to_string(),
            ],
            alerts: Vec::new(),
        }
    }
}

impl RuntimeSnapshot {
    pub fn tick(&self, genome: &Genome) -> Self {
        let next_tick = self.tick.saturating_add(1);
        let stage = match next_tick % 6 {
            0 => RuntimeStage::Observe,
            1 => RuntimeStage::Recall,
            2 => RuntimeStage::Plan,
            3 => RuntimeStage::Act,
            4 => RuntimeStage::Validate,
            _ => RuntimeStage::Learn,
        };

        let energy_drain = genome.planner.depth.saturating_mul(2).saturating_add(genome.memory.working_slots / 2);
        let next_energy = self.energy.saturating_sub(energy_drain).min(100);
        let next_memory_pressure = self
            .memory_pressure
            .saturating_add(match stage {
                RuntimeStage::Recall => 2,
                RuntimeStage::Learn => 1,
                _ => 0,
            })
            .saturating_sub(1)
            .min(100);

        let (last_action, last_result) = match stage {
            RuntimeStage::Observe => ("Read environment", "Input sampled"),
            RuntimeStage::Recall => ("Fetch episodic memory", "Relevant memory restored"),
            RuntimeStage::Plan => ("Assemble bounded plan", "Plan bounded"),
            RuntimeStage::Act => ("Execute permitted action", "Action completed"),
            RuntimeStage::Validate => ("Check policy and result", "Policy checked"),
            RuntimeStage::Learn => ("Write experience summary", "Experience stored"),
        };

        let mut alerts = self.alerts.clone();
        let mut governance_state = GovernanceState::Ready;

        if next_memory_pressure > 75 {
            alerts.insert(0, "Memory pressure exceeded safe threshold.".to_string());
            governance_state = GovernanceState::Constrained;
        }

        if next_energy < 20 {
            alerts.insert(0, "Energy low. System is conserving compute.".to_string());
            governance_state = GovernanceState::Constrained;
        }

        if matches!(stage, RuntimeStage::Act) && !genome.tools.allowed.iter().any(|item| item == "write") {
            alerts.insert(0, "Attempted restricted action was blocked.".to_string());
            governance_state = GovernanceState::Alert;
        }

        let mut log = self.log.clone();
        log.insert(0, format!("{:03} · {:?} · {}", next_tick, stage, last_result));
        log.truncate(6);
        alerts.truncate(6);

        Self {
            tick: next_tick,
            energy: next_energy,
            stage,
            last_action: last_action.to_string(),
            last_result: last_result.to_string(),
            memory_pressure: next_memory_pressure,
            governance_state,
            log,
            alerts,
        }
    }
}
