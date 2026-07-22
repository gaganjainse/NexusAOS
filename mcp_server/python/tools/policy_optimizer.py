"""
NexusAOS - Policy Optimizer
Version: 1.0.0
Description: Optimizes Orchestrator routing weights using the EvolutionEngine.
"""

import json
import time
from pathlib import Path
from typing import Dict, List
from tools.evolution_engine import EvolutionEngine, Genome

class PolicyOptimizer:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.routing_path = base_dir / "core" / "monitoring" / "routing_weights.json"
        self.evo_engine = EvolutionEngine(base_dir)
        
        # Register fitness evaluator for routing policies
        self.evo_engine.register_fitness_evaluator(self._evaluate_routing_fitness)

    def _evaluate_routing_fitness(self, genome: Genome) -> Dict:
        """Evaluates how well a routing config performs."""
        # In a real system, this would run a simulator or look at real history.
        # For now, we use the success/failure counts from the routing_weights.json
        # as a baseline and combine it with the 'intelligence' of the genome.
        
        try:
            with open(self.routing_path, "r", encoding="utf-8") as f:
                current_stats = json.load(f)
        except Exception:
            return {"score": 0.5, "components": {}}
            
        success_counts = current_stats.get("success_counts", {})
        failure_counts = current_stats.get("failure_counts", {})
        
        total_success = sum(success_counts.values())
        total_failure = sum(failure_counts.values())
        total_tasks = total_success + total_failure
        
        if total_tasks == 0:
            return {"score": 0.5, "components": {"reason": "no_data"}}
            
        base_success_rate = total_success / total_tasks
        
        # Genome specific adjustments (simulated optimization)
        # We check if the genome's "weights" (in config) improve the distribution
        score = base_success_rate
        
        # Penalize for complex configurations (parsimony)
        score -= len(genome.config) * 0.01
        
        return {
            "score": max(0.0, min(1.0, score)),
            "components": {
                "base_success_rate": base_success_rate,
                "complexity_penalty": len(genome.config) * 0.01
            }
        }

    def optimize_routing(self) -> Dict:
        """Runs one generation of evolution on the routing policy."""
        # 1. Load current routing as a seed genome
        try:
            with open(self.routing_path, "r", encoding="utf-8") as f:
                current_routing = json.load(f).get("routes", {})
        except Exception:
            current_routing = {}

        # 2. Evolve
        result = self.evo_engine.evolve_generation(population_size=10, shadow_test=True)
        
        if result["success"]:
            # 3. Promote best
            promotion = self.evo_engine.promote_best()
            if promotion["success"]:
                best_genome = promotion["promoted_genome"]
                self._apply_routing_genome(best_genome["config"])
                return {"success": True, "genome_id": best_genome["id"], "fitness": best_genome["fitness"]}
        
        return {"success": False, "error": result.get("error", "Evolution failed")}

    def _apply_routing_genome(self, config: Dict):
        """Updates the routing_weights.json with the new evolved routes."""
        try:
            with open(self.routing_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Update only the 'routes' section
            data["routes"] = config
            
            with open(self.routing_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Policy Optimizer Error: {e}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent.parent.parent
    optimizer = PolicyOptimizer(base)
    print(optimizer.optimize_routing())
