use crate::model::{DashboardSnapshot, Genome, RuntimeSnapshot};

#[derive(Debug)]
pub struct NexusState {
    pub genome: Genome,
    pub runtime: RuntimeSnapshot,
}

impl Default for NexusState {
    fn default() -> Self {
        Self {
            genome: Genome::default(),
            runtime: RuntimeSnapshot::default(),
        }
    }
}

impl NexusState {
    pub fn snapshot(&self) -> DashboardSnapshot {
        DashboardSnapshot {
            genome: self.genome.clone(),
            runtime: self.runtime.clone(),
            phenotype: self.genome.derive_phenotype(),
        }
    }

    pub fn tick(&mut self) -> DashboardSnapshot {
        self.runtime = self.runtime.tick(&self.genome);
        self.snapshot()
    }

    pub fn mutate(&mut self) -> DashboardSnapshot {
        self.genome = self.genome.mutate();
        self.runtime.alerts.insert(0, format!("Genome mutated to version {}.", self.genome.version));
        self.runtime.alerts.truncate(6);
        self.snapshot()
    }

    pub fn reset(&mut self) -> DashboardSnapshot {
        *self = Self::default();
        self.snapshot()
    }
}
