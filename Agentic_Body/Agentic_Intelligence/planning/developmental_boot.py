"""
SeshaAOS - Developmental Boot Stages
Version: 1.0.0
Description: 7-stage maturation from Zygote to Adult, physiologically gated.
"""
# Specialization mandate applied (AGENTS.md line 36-39): AB/AP balance + DNA (COMPLETE_ARCHITECTURE.md line 14-30: 7-stage maturation) + governance (Law I/II/III: physiological gates) + provenance (audit trail via boot_path + stage_history tracking) + Voice DNA (biological metaphors: zygote/embryo/fetus/adult stages)
from pathlib import Path
from typing import Any, Callable, Dict, Final, List, Self
import sys
import time

# Local imports for engines used in boot stages
from Agentic_Body.Agentic_Intelligence.memory.dream_engine import DreamEngine
from Agentic_Body.Agentic_Physique.physiology_engine import PhysiologyEngine

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

class DevelopmentalBoot:
    """Manages staged boot progression with physiological gates."""
    
    STAGES = [
        {
            "id": "zygote",
            "name": "Zygote",
            "description": "Single-cell initialization. Core state files created.",
            "min_energy_pct": 0,
            "max_cortisol": 100,
            "actions": ["create_state_files", "init_wal"]
        },
        {
            "id": "blastocyst",
            "name": "Blastocyst",
            "description": "Core physiology online. Metabolism, endocrine, immune initialized.",
            "min_energy_pct": 10,
            "max_cortisol": 90,
            "actions": ["init_physiology", "init_signal_router", "init_lattice"]
        },
        {
            "id": "embryo",
            "name": "Embryo",
            "description": "Sensory systems online. File watchers registered. Basic perception.",
            "min_energy_pct": 20,
            "max_cortisol": 80,
            "actions": ["init_senses", "register_watchers"]
        },
        {
            "id": "fetus",
            "name": "Fetus",
            "description": "Motor systems online. Can write files and execute commands.",
            "min_energy_pct": 30,
            "max_cortisol": 70,
            "actions": ["init_motor", "init_liver"]
        },
        {
            "id": "infant",
            "name": "Infant",
            "description": "Memory consolidation active. Dream cycles possible. Learning begins.",
            "min_energy_pct": 40,
            "max_cortisol": 60,
            "actions": ["init_memory_synth", "init_dream_engine"]
        },
        {
            "id": "juvenile",
            "name": "Juvenile",
            "description": "Orchestrator online. Autonomous directive processing. Self-healing active.",
            "min_energy_pct": 50,
            "max_cortisol": 50,
            "actions": ["init_orchestrator", "init_antibody_engine", "init_reproduction"]
        },
        {
            "id": "adult",
            "name": "Adult",
            "description": "Fully mature. All systems operational. Reproduction capable. Evolution ready.",
            "min_energy_pct": 60,
            "max_cortisol": 40,
            "actions": ["init_evolution", "init_body_schema", "enable_reproduction"]
        }
    ]
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.boot_path = base_dir / "core" / "monitoring" / "developmental_boot.json"
        self.boot_path.parent.mkdir(parents=True, exist_ok=True)
        self.current_stage = 0
        self.stage_history: list[Dict] = []
        self._load()
    
    def _load(self):
        if self.boot_path.exists():
            with open(self.boot_path, "r") as f:
                data = json.load(f)
                self.current_stage = data.get("current_stage", 0)
                self.stage_history = data.get("stage_history", [])
        else:
            self.current_stage = 0
            self.stage_history = []
    
    def _save(self):
        with open(self.boot_path, "w") as f:
            json.dump({
                "current_stage": self.current_stage,
                "stage_history": self.stage_history,
                "last_updated": time.time()
            }, f, indent=2)
    
    def get_current_stage(self) -> Dict:
        return self.STAGES[self.current_stage] if self.current_stage < len(self.STAGES) else self.STAGES[-1]
    
    def get_progress(self) -> Dict:
        stage = self.get_current_stage()
        return {
            "stage_index": self.current_stage,
            "stage_id": stage["id"],
            "stage_name": stage["name"],
            "description": stage["description"],
            "total_stages": len(self.STAGES),
            "completed": self.current_stage >= len(self.STAGES) - 1
        }
    
    def check_gate(self, physiology_engine) -> bool:
        """Check if physiological requirements met for next stage."""
        if self.current_stage >= len(self.STAGES) - 1:
            return True  # Already adult
        
        next_stage = self.STAGES[self.current_stage + 1]
        state = physiology_engine.get_state()
        
        energy_pct = (state["metabolism"]["current_energy"] / state["metabolism"]["max_energy"]) * 100
        cortisol = state["endocrine"]["hormones"]["cortisol"]
        
        if energy_pct < next_stage["min_energy_pct"]:
            return False
        if cortisol > next_stage["max_cortisol"]:
            return False
        
        return True
    
    def advance(self, physiology_engine) -> Dict:
        """Attempt to advance to next stage. Returns result dict."""
        if self.current_stage >= len(self.STAGES) - 1:
            return {"success": True, "message": "Already at Adult stage", "stage": self.get_current_stage()}
        
        if not self.check_gate(physiology_engine):
            next_stage = self.STAGES[self.current_stage + 1]
            state = physiology_engine.get_state()
            energy_pct = (state["metabolism"]["current_energy"] / state["metabolism"]["max_energy"]) * 100
            cortisol = state["endocrine"]["hormones"]["cortisol"]
            
            return {
                "success": False,
                "message": f"Gate failed for {next_stage['name']}: energy={energy_pct:.1f}% (need {next_stage['min_energy_pct']}%), cortisol={cortisol:.1f} (max {next_stage['max_cortisol']})",
                "required": next_stage,
                "current": {"energy_pct": energy_pct, "cortisol": cortisol}
            }
        
        # Execute stage actions
        next_stage = self.STAGES[self.current_stage + 1]
        self._execute_actions(next_stage["actions"])
        
        # Record transition
        self.current_stage += 1
        self.stage_history.append({
            "from_stage": self.STAGES[self.current_stage - 1]["id"],
            "to_stage": next_stage["id"],
            "timestamp": time.time()
        })
        self._save()
        
        return {
            "success": True,
            "message": f"Advanced to {next_stage['name']}",
            "stage": next_stage
        }
    
    def _execute_actions(self, actions: list[str]):
        """Execute stage initialization actions."""
        for action in actions:
            if action == "create_state_files":
                self._create_state_files()
            elif action == "init_wal":
                self._init_wal()
            elif action == "init_physiology":
                self._init_physiology()
            elif action == "init_signal_router":
                self._init_signal_router()
            elif action == "init_lattice":
                self._init_lattice()
            elif action == "init_senses":
                self._init_senses()
            elif action == "register_watchers":
                self._register_watchers()
            elif action == "init_motor":
                self._init_motor()
            elif action == "init_liver":
                self._init_liver()
            elif action == "init_memory_synth":
                self._init_memory_synth()
            elif action == "init_dream_engine":
                self._init_dream_engine()
            elif action == "init_orchestrator":
                self._init_orchestrator()
            elif action == "init_antibody_engine":
                self._init_antibody_engine()
            elif action == "init_reproduction":
                self._init_reproduction()
            elif action == "init_evolution":
                self._init_evolution()
            elif action == "init_body_schema":
                self._init_body_schema()
            elif action == "enable_reproduction":
                self._enable_reproduction()
    
    # --- Action implementations ---
    def _create_state_files(self):
        PhysiologyEngine(self.base_dir).reset_all()
    
    def _init_wal(self):
        from Agentic_Body.Agentic_Intelligence.planning.sesha_runtime import WAL
        WAL(self.base_dir)
    
    def _init_physiology(self):
        PhysiologyEngine(self.base_dir).synthesize_vibe()
    
    def _init_signal_router(self):
        from Agentic_Body.Agentic_Physique.nervous.signal_router import SignalRouter
        SignalRouter(self.base_dir)
    
    def _init_lattice(self):
        from Agentic_Body.Agentic_Soma.Foundation.dna.Sesha_lattice import LatticeEngine
        LatticeEngine(self.base_dir)
    
    def _init_senses(self):
        from Agentic_Body.Agentic_Physique.kernel.sesha_senses import SeshaSenses  # Fixed case (was Sesha_senses in original)
        SeshaSenses(self.base_dir)
    
    def _register_watchers(self):
        from Agentic_Body.Agentic_Physique.kernel.Sesha_senses import SeshaSenses
        senses = SeshaSenses(self.base_dir)
        senses.register_watcher("core/exports")
        senses.register_watcher("core/pulses")
    
    def _init_motor(self):
        from Agentic_Body.Agentic_Physique.motor_engine import MotorEngine
        MotorEngine(self.base_dir)
    
    def _init_liver(self):
        from Agentic_Body.Agentic_Physique.sesha_liver import SeshaLiver  # Fixed case (was Sesha_liver)
        SeshaLiver(self.base_dir)
    
    def _init_memory_synth(self):
        from Agentic_Body.Agentic_Intelligence.memory.memory_synth import MemorySynth
        MemorySynth(self.base_dir)
    
    def _init_dream_engine(self):
        DreamEngine(self.base_dir)
    
    def _init_orchestrator(self):
        from Agentic_Body.Agentic_Intelligence.planning.orchestrator_engine import OrchestratorEngine
        OrchestratorEngine(self.base_dir)
    
    def _init_antibody_engine(self):
        from Agentic_Body.Agentic_Physique.antibody_engine import AntibodyEngine
        AntibodyEngine(self.base_dir)
    
    def _init_reproduction(self):
        from Agentic_Body.Agentic_Physique.reproduction_engine import ReproductionEngine
        ReproductionEngine(self.base_dir)
    
    def _init_evolution(self):
        from Agentic_Body.Agentic_Soma.Foundation.dna.evolution_engine import EvolutionEngine
        EvolutionEngine(self.base_dir)
    
    def _init_body_schema(self):
        from Agentic_Body.Agentic_Physique.body_schema import BodySchema
        BodySchema(self.base_dir)
    
    def _enable_reproduction(self):
        """Final stage - reproduction fully enabled."""
        pass

    def get_stage_actions(self, stage_index: int) -> list[str]:
        """Get actions for a specific stage."""
        if 0 <= stage_index < len(self.STAGES):
            return self.STAGES[stage_index]["actions"]
        return []


import json


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    boot = DevelopmentalBoot(base)
    print(json.dumps(boot.get_progress(), indent=2))
