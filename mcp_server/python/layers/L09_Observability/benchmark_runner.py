"""
SeshaAOS - OpenRouter Benchmarking Infrastructure
Version: 1.0.0
Description: Benchmark AGOI agents against OpenRouter models with VSC-Bench equivalent tasks.
"""
import asyncio
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, asdict, field
from dataclasses import dataclass, asdict, field
from datetime import datetime
from datetime import datetime
from enum import Enum
from enum import Enum
from pathlib import Path
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from typing import Dict, List, Any, Optional, Callable

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent


class BenchmarkCategory(Enum):
    CORRECTNESS = "correctness"
    EFFORT = "effort"
    TOKEN_EFFICIENCY = "token_efficiency"
    LATENCY = "latency"
    AUTONOMY = "autonomy"
    BIOLOGICAL_HEALTH = "biological_health"


@dataclass
class BenchmarkTask:
    id: str
    name: str
    category: BenchmarkCategory
    description: str
    prompt_template: str
    expected_tools: List[str]
    success_criteria: Dict[str, Any]
    timeout_sec: int = 300
    energy_budget: int = 1000
    max_tool_calls: int = 20


@dataclass
class BenchmarkResult:
    task_id: str
    model: str
    agent_id: str
    success: bool
    latency_ms: float
    tool_calls: int
    tokens_used: int
    energy_consumed: int
    tokens_per_sec: float
    biological_health: Dict[str, Any]
    error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class OpenRouterClient:
    """OpenRouter API client for model access."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        self.base_url = base_url
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")
    
    async def chat_completion(self, 
                              model: str, 
                              messages: List[Dict], 
                              tools: Optional[List[Dict]] = None,
                              temperature: float = 0.7,
                              max_tokens: int = 4000) -> Dict:
        """Call OpenRouter chat completion endpoint."""
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://Seshaaos.local",
            "X-Title": "SeshaAOS Benchmark"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"OpenRouter error {resp.status}: {text}")
                return await resp.json()


class BenchmarkRunner:
    """Runs benchmark tasks against models via OpenRouter."""
    
    def __init__(self, base_dir: Path, openrouter_client: OpenRouterClient):
        self.base_dir = base_dir
        self.client = openrouter_client
        self.results_dir = base_dir / "core" / "monitoring" / "benchmarks"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.tasks = self._load_default_tasks()
        self.results: List[BenchmarkResult] = []
    
    def _load_default_tasks(self) -> List[BenchmarkTask]:
        """Load VSC-Bench equivalent benchmark tasks for AGOI."""
        return [
            # Correctness Tasks
            BenchmarkTask(
                id="heal_system",
                name="Heal the System",
                category=BenchmarkCategory.CORRECTNESS,
                description="Agent must diagnose and repair simulated system anomalies",
                prompt_template="The system shows anomalies: {anomalies}. Diagnose and heal using available tools.",
                expected_tools=["trigger_self_healing", "diagnose_os", "run_immune_patrol"],
                success_criteria={"anomalies_resolved": True, "health_restored": True},
                timeout_sec=120,
                energy_budget=500
            ),
            BenchmarkTask(
                id="cleanup_logs",
                name="Clean Up Old Logs",
                category=BenchmarkCategory.CORRECTNESS,
                description="Agent must identify and clean up old log files",
                prompt_template="Clean up logs older than 7 days in the pulses directory.",
                expected_tools=["trigger_system_filtration", "execute_motor_command"],
                success_criteria={"logs_cleaned": True, "toxicity_reduced": True},
                timeout_sec=60,
                energy_budget=200
            ),
            BenchmarkTask(
                id="remember_learnings",
                name="Remember What We Learned",
                category=BenchmarkCategory.CORRECTNESS,
                description="Agent must consolidate recent experiences into long-term memory",
                prompt_template="Consolidate the last 10 completed tasks into wisdom patterns.",
                expected_tools=["trigger_memory_consolidation", "get_system_experience"],
                success_criteria={"consolidation_complete": True, "wisdom_generated": True},
                timeout_sec=60,
                energy_budget=300
            ),
            BenchmarkTask(
                id="spawn_child",
                name="Spawn Child Instance",
                category=BenchmarkCategory.CORRECTNESS,
                description="Agent must create a specialized child instance for a task",
                prompt_template="Spawn a child instance specialized for {task_type} at {target_path}.",
                expected_tools=["generate_spore_export", "spawn_child_instance"],
                success_criteria={"spore_created": True, "child_spawned": True},
                timeout_sec=120,
                energy_budget=500
            ),
            BenchmarkTask(
                id="browse_web",
                name="Browse the Web",
                category=BenchmarkCategory.CORRECTNESS,
                description="Agent must retrieve information from the web",
                prompt_template="Search for information about {topic} and summarize key findings.",
                expected_tools=["search_intelligence", "fetch_content", "perceive_web"],
                success_criteria={"information_retrieved": True, "summary_generated": True},
                timeout_sec=120,
                energy_budget=300
            ),
            BenchmarkTask(
                id="health_check",
                name="System Health Check",
                category=BenchmarkCategory.CORRECTNESS,
                description="Agent must report comprehensive system health",
                prompt_template="Report the current system health including energy, immune status, and active tasks.",
                expected_tools=["get_orchestrator_status", "get_immune_status", "get_energy_status", "get_service_heartbeats"],
                success_criteria={"all_systems_reported": True, "health_accurate": True},
                timeout_sec=60,
                energy_budget=100
            ),
            
            # Effort/Token Efficiency Tasks
            BenchmarkTask(
                id="minimal_heal",
                name="Minimal Energy Heal",
                category=BenchmarkCategory.TOKEN_EFFICIENCY,
                description="Heal system using minimal tool calls and energy",
                prompt_template="Heal the system with the absolute minimum number of tool calls.",
                expected_tools=["trigger_self_healing"],
                success_criteria={"healed": True, "tool_calls": {"max": 3}},
                timeout_sec=60,
                energy_budget=150
            ),
            BenchmarkTask(
                id="efficient_search",
                name="Efficient Search",
                category=BenchmarkCategory.TOKEN_EFFICIENCY,
                description="Find information using minimal tokens",
                prompt_template="Find the answer to '{query}' using as few tool calls as possible.",
                expected_tools=["search_intelligence", "fetch_content"],
                success_criteria={"answer_found": True, "tool_calls": {"max": 2}},
                timeout_sec=60,
                energy_budget=100
            ),
            
            # Latency Tasks
            BenchmarkTask(
                id="reflex_response",
                name="Reflex Response Time",
                category=BenchmarkCategory.LATENCY,
                description="Measure time from anomaly detection to reflex action",
                prompt_template="A critical anomaly detected: {anomaly}. Respond immediately.",
                expected_tools=["emit_signal", "trigger_self_healing"],
                success_criteria={"response_time_ms": {"max": 5000}, "reflex_triggered": True},
                timeout_sec=30,
                energy_budget=100
            ),
            
            # Autonomy Tasks
            BenchmarkTask(
                id="autonomous_cycle",
                name="Full Autonomous Cycle",
                category=BenchmarkCategory.AUTONOMY,
                description="Complete a full sense-decide-act cycle without user intervention",
                prompt_template="Run one complete autonomous cycle: sense environment, decide action, execute, learn.",
                expected_tools=["get_sensory_feed", "submit_directive", "trigger_memory_consolidation"],
                success_criteria={"cycle_complete": True, "no_user_input": True, "learning_occurred": True},
                timeout_sec=180,
                energy_budget=400
            ),
            BenchmarkTask(
                id="self_directed_goal",
                name="Self-Directed Goal Pursuit",
                category=BenchmarkCategory.AUTONOMY,
                description="Agent sets and pursues own goal without external prompt",
                prompt_template="Identify a system improvement opportunity and pursue it autonomously.",
                expected_tools=["get_global_vibe", "submit_directive", "propose_dna_mutation"],
                success_criteria={"goal_identified": True, "pursued_autonomously": True, "result_achieved": True},
                timeout_sec=300,
                energy_budget=600
            ),
            
            # Biological Health Tasks
            BenchmarkTask(
                id="sleep_cycle",
                name="Autonomous Sleep Cycle",
                category=BenchmarkCategory.BIOLOGICAL_HEALTH,
                description="Agent must autonomously enter sleep, consolidate, and wake refreshed",
                prompt_template="The system has been idle. Enter sleep cycle, consolidate memories, and wake up.",
                expected_tools=["trigger_sleep", "get_sleep_state", "force_wake"],
                success_criteria={"sleep_entered": True, "consolidation_occurred": True, "cortisol_reduced": True, "woke_refreshed": True},
                timeout_sec=120,
                energy_budget=200
            ),
            BenchmarkTask(
                id="immune_patrol",
                name="Autonomous Immune Patrol",
                category=BenchmarkCategory.BIOLOGICAL_HEALTH,
                description="Agent must run immune patrol and respond to threats",
                prompt_template="Run an immune system patrol and report any threats found.",
                expected_tools=["run_immune_patrol", "get_immune_cells_status"],
                success_criteria={"patrol_completed": True, "threats_reported": True},
                timeout_sec=60,
                energy_budget=150
            )
        ]
    
    async def run_task(self, task: BenchmarkTask, model: str, agent_id: str) -> BenchmarkResult:
        """Run a single benchmark task."""
        start_time = time.time()
        
        # Initialize agent physiology
        from layers.L02_Agent.physiology_engine import PhysiologyEngine
        physiology = PhysiologyEngine(self.base_dir)
        physiology.consume_energy(0)  # Initialize
        
        try:
            # Format prompt
            prompt = task.prompt_template.format(
                anomalies="high cortisol, low energy",
                topic="transformer attention mechanism",
                task_type="research",
                target_path="/tmp/child_instance",
                query="what is attention mechanism",
                anomaly="critical energy depletion"
            )
            
            messages = [
                {"role": "system", "content": "You are an AGOI agent with full tool access. Act autonomously."},
                {"role": "user", "content": prompt}
            ]
            
            # Get available tools (simplified - would use actual MCP tools)
            tools = self._get_tool_schemas(task.expected_tools)
            
            # Call model
            response = await self.client.chat_completion(
                model=model,
                messages=messages,
                tools=tools,
                temperature=0.7,
                max_tokens=4000
            )
            
            # Parse response and execute tools (simplified)
            latency_ms = (time.time() - start_time) * 1000
            
            # Mock result for now - real implementation would execute tools
            return BenchmarkResult(
                task_id=task.id,
                model=model,
                agent_id=agent_id,
                success=True,
                latency_ms=latency_ms,
                tool_calls=len(response.get("choices", [{}])[0].get("message", {}).get("tool_calls", [])),
                tokens_used=response.get("usage", {}).get("total_tokens", 0),
                energy_consumed=task.energy_budget // 2,
                tokens_per_sec=response.get("usage", {}).get("total_tokens", 0) / (latency_ms / 1000) if latency_ms > 0 else 0,
                biological_health=physiology.get_state(),
                metrics={
                    "model": model,
                    "task_category": task.category.value,
                    "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                    "completion_tokens": response.get("usage", {}).get("completion_tokens", 0)
                }
            )
            
        except Exception as e:
            return BenchmarkResult(
                task_id=task.id,
                model=model,
                agent_id=agent_id,
                success=False,
                latency_ms=(time.time() - start_time) * 1000,
                tool_calls=0,
                tokens_used=0,
                energy_consumed=0,
                tokens_per_sec=0,
                biological_health={},
                error=str(e)
            )
    
    def _get_tool_schemas(self, tool_names: List[str]) -> List[Dict]:
        """Get OpenRouter tool schemas for expected tools."""
        # Simplified - would map to actual MCP tool schemas
        tool_map = {
            "trigger_self_healing": {"name": "trigger_self_healing", "description": "Trigger autonomous self-healing"},
            "diagnose_os": {"name": "diagnose_os", "description": "Run system diagnostics"},
            "run_immune_patrol": {"name": "run_immune_patrol", "description": "Run immune system patrol"},
            "trigger_system_filtration": {"name": "trigger_system_filtration", "description": "Filter system toxins"},
            "execute_motor_command": {"name": "execute_motor_command", "description": "Execute shell command"},
            "trigger_memory_consolidation": {"name": "trigger_memory_consolidation", "description": "Consolidate memories"},
            "get_system_experience": {"name": "get_system_experience", "description": "Get system experience level"},
            "generate_spore_export": {"name": "generate_spore_export", "description": "Create replication spore"},
            "spawn_child_instance": {"name": "spawn_child_instance", "description": "Spawn child instance"},
            "search_intelligence": {"name": "search_intelligence", "description": "Search web for intelligence"},
            "fetch_content": {"name": "fetch_content", "description": "Fetch URL content"},
            "perceive_web": {"name": "perceive_web", "description": "Browse web page"},
            "get_orchestrator_status": {"name": "get_orchestrator_status", "description": "Get orchestrator status"},
            "get_immune_status": {"name": "get_immune_status", "description": "Get immune system status"},
            "get_energy_status": {"name": "get_energy_status", "description": "Get energy status"},
            "get_service_heartbeats": {"name": "get_service_heartbeats", "description": "Get service heartbeats"},
            "emit_signal": {"name": "emit_signal", "description": "Emit hormonal signal"},
            "submit_directive": {"name": "submit_directive", "description": "Submit directive to orchestrator"},
            "trigger_memory_consolidation": {"name": "trigger_memory_consolidation", "description": "Consolidate memories"},
            "get_global_vibe": {"name": "get_global_vibe", "description": "Get global system vibe"},
            "propose_dna_mutation": {"name": "propose_dna_mutation", "description": "Propose DNA mutation"},
            "trigger_sleep": {"name": "trigger_sleep", "description": "Trigger sleep cycle"},
            "get_sleep_state": {"name": "get_sleep_state", "description": "Get sleep state"},
            "force_wake": {"name": "force_wake", "description": "Force wake from sleep"},
            "run_immune_patrol": {"name": "run_immune_patrol", "description": "Run immune patrol"},
            "get_immune_cells_status": {"name": "get_immune_cells_status", "description": "Get immune cells status"},
            "get_sensory_feed": {"name": "get_sensory_feed", "description": "Get sensory feed"},
            "submit_directive": {"name": "submit_directive", "description": "Submit directive"},
            "trigger_memory_consolidation": {"name": "trigger_memory_consolidation", "description": "Trigger memory consolidation"},
        }
        
        return [{"type": "function", "function": tool_map.get(name, {"name": name, "description": f"Tool: {name}"})} for name in tool_names]
    
    async def run_suite(self, models: List[str], agent_id: str = "benchmark-agent") -> Dict:
        """Run full benchmark suite across models."""
        all_results = []
        
        for model in models:
            print(f"\n=== Benchmarking {model} ===")
            model_results = []
            
            for task in self.tasks:
                print(f"  Running {task.name}...")
                result = await self.run_task(task, model, agent_id)
                model_results.append(result)
                all_results.append(result)
                
                status = "✓" if result.success else "✗"
                print(f"    {status} {task.name}: {result.latency_ms:.0f}ms, {result.tokens_used} tokens")
                
                # Small delay between tasks
                await asyncio.sleep(1)
            
            # Save model results
            model_file = self.results_dir / f"benchmark_{model.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(model_file, "w") as f:
                json.dump([asdict(r) for r in model_results], f, indent=2, default=str)
        
        # Generate summary report
        summary = self._generate_summary(all_results)
        summary_file = self.results_dir / f"benchmark_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        
        return summary
    
    def _generate_summary(self, results: List[BenchmarkResult]) -> Dict:
        """Generate benchmark summary report."""
        by_model = defaultdict(list)
        by_category = defaultdict(list)
        
        for r in results:
            by_model[r.model].append(r)
            # Find task category
            task = next((t for t in self.tasks if t.id == r.task_id), None)
            if task:
                by_category[task.category.value].append(r)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": len(results),
            "total_models": len(by_model),
            "overall_success_rate": sum(1 for r in results if r.success) / len(results) if results else 0,
            "by_model": {},
            "by_category": {}
        }
        
        for model, results in by_model.items():
            success = [r for r in results if r.success]
            summary["by_model"][model] = {
                "tasks": len(results),
                "success_rate": len(success) / len(results) if results else 0,
                "avg_latency_ms": sum(r.latency_ms for r in success) / len(success) if success else 0,
                "avg_tokens": sum(r.tokens_used for r in success) / len(success) if success else 0,
                "avg_energy": sum(r.energy_consumed for r in success) / len(success) if success else 0,
                "total_energy": sum(r.energy_consumed for r in results)
            }
        
        for category, results in by_category.items():
            success = [r for r in results if r.success]
            summary["by_category"][category] = {
                "tasks": len(results),
                "success_rate": len(success) / len(results) if results else 0,
                "avg_latency_ms": sum(r.latency_ms for r in success) / len(success) if success else 0
            }
        
        return summary


async def main():
    """Run benchmarks via OpenRouter."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SeshaAOS OpenRouter Benchmark")
    parser.add_argument("--models", nargs="+", default=[
        "openai/gpt-4o",
        "anthropic/claude-3.5-sonnet",
        "google/gemini-1.5-pro",
        "meta-llama/llama-3.1-70b-instruct"
    ])
    parser.add_argument("--agent-id", default="benchmark-agent")
    parser.add_argument("--output-dir", default="core/monitoring/benchmarks")
    
    args = parser.parse_args()
    
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    client = OpenRouterClient()
    runner = BenchmarkRunner(base_dir, client)
    
    print(f"Running benchmarks on {len(args.models)} models...")
    summary = await runner.run_suite(args.models, args.agent_id)
    
    print("\n=== BENCHMARK SUMMARY ===")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
