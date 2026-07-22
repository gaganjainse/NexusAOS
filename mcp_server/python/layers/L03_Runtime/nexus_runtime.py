"""
NexusAOS - Unified Async Runtime
"""
import asyncio
import json
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
import sys
if str(BASE_DIR / "mcp_server" / "python") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))

class WAL:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.wal_dir = base_dir / "core" / "monitoring" / "wal"
        self.wal_dir.mkdir(exist_ok=True, parents=True)
        self.current_wal = self.wal_dir / f"wal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.lock = asyncio.Lock()

    async def append(self, event_type: str, data: dict):
        async with self.lock:
            timestamp = datetime.now().isoformat()
            event = {
                "timestamp": timestamp,
                "type": event_type,
                "data": data,
            }
            with open(self.current_wal, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")

    async def read_all(self):
        events = []
        for wal_file in sorted(self.wal_dir.glob("wal_*.log")):
            with open(wal_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        return events

class NexusRuntime:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.wal = WAL(base_dir)
        self.running = False
        self.tasks = []

        from layers.L02_Agent.sleep_engine import SleepEngine
        from layers.L02_Agent.metabolism_engine import MetabolismEngine
        from layers.L02_Agent.immune_engine import ImmuneEngine
        from layers.L02_Agent.endocrine_engine import EndocrineEngine
        from layers.L02_Agent.digestive_engine import DigestiveEngine
        from layers.L02_Agent.respiratory_engine import RespiratoryEngine
        from layers.L02_Agent.lymphatic_system import LymphaticSystem
        from layers.L02_Agent.excretory_engine import ExcretoryEngine
        from layers.L02_Agent.cardiorespiratory_loop import CardiorespiratoryLoop
        from layers.L07_Integration.integumentary_gateway import IntegumentaryGateway
        from layers.L01_Planning.thought_agent import ThoughtAgent
        from layers.L09_Observability.wisdom_feed import WisdomFeed
        from layers.L09_Observability.queue_manager import QueueManager
        from layers.L02_Agent.vigilance_reflex import VigilanceReflex
        from layers.L12_Infrastructure.reflex_arc import ReflexArc
        from layers.L01_Planning.instinct_engine import InstinctEngine
        from layers.L10_Intelligence.limbic_system import LimbicSystem
        from layers.L02_Agent.cerebellum_engine import CerebellumEngine
        from layers.L09_Observability.reward_system import RewardSystem
        from layers.L05_Memory.memory_synth import MemorySynth

        self.sleep = SleepEngine(base_dir)
        self.metabolism = MetabolismEngine(base_dir)
        self.immune = ImmuneEngine(base_dir)
        self.endocrine = EndocrineEngine(base_dir)
        self.digestive = DigestiveEngine(base_dir)
        self.respiratory = RespiratoryEngine(base_dir)
        self.lymphatic = LymphaticSystem(base_dir)
        self.excretory = ExcretoryEngine(base_dir)
        self.cardio = CardiorespiratoryLoop(base_dir)
        self.skin = IntegumentaryGateway(base_dir)
        self.thought = ThoughtAgent(base_dir)
        self.wisdom = WisdomFeed(base_dir)
        self.queue = QueueManager(base_dir)
        self.vigilance = VigilanceReflex(base_dir)
        self.reflex = ReflexArc(base_dir)
        self.instinct = InstinctEngine(base_dir)
        self.limbic = LimbicSystem(base_dir)
        self.cerebellum = CerebellumEngine(base_dir)
        self.rewards = RewardSystem(base_dir)
        self.memory = MemorySynth(base_dir)

    async def homeostasis_loop(self):
        """Maintains internal balance and pushes proactive briefings."""
        tick_count = 0
        while self.running:
            # 1. Spinal Cord: Reflex Arc (Fast Path)
            reflex_actions = self.reflex.check_reflexes()
            for action in reflex_actions:
                await self.wal.append("reflex", {"action": action})
                self.wisdom.push_briefing("Autonomic Reflex", action, "HIGH")

            # 2. Limbic Layer: Emotional Intelligence
            limbic_report = self.limbic.process_stimulus()
            if "FEAR" in limbic_report or "ANGER" in limbic_report:
                 await self.wal.append("limbic", {"event": "emotional_shift", "report": limbic_report})
                 self.wisdom.push_briefing("Limbic Shift", limbic_report, "MEDIUM")

            # 3. Mind Layer: Instinct Engine (Biological Drives)
            instinct_drives = self.instinct.evaluate_drives()
            for drive in instinct_drives:
                await self.wal.append("instinct", {"drive": drive})
                self.wisdom.push_briefing("Biological Instinct", drive, "MEDIUM")
            
            # 4. Performance & Rewards (Dopamine Loop)
            if tick_count % 30 == 0:
                bench = self.rewards.run_benchmark(iterations=3)
                if bench["rewarded"]:
                    self.wisdom.push_briefing("Biological Reward", f"Performance improved (+{bench['improvement_pct']:.1f}%). Dopamine released.", "LOW")

            # 5. Homeostatic Tick
            met_report = self.cardio.homeostatic_tick()
            if met_report.get("thermal_status") != "normal":
                 await self.wal.append("homeostasis", {"signal": "THERMAL_STRESS", "status": met_report["thermal_status"]})
                 self.wisdom.report_anomaly("Metabolism", f"Thermal stress detected: {met_report['thermal_status']}")
                 self.cardio.ventilate_context(100000)

            # 2. Vigilance Check (Attentional Gating)
            idle_msg = self.vigilance.check_idle(idle_threshold=300)
            if idle_msg:
                await self.wal.append("vigilance", {"event": "idle_recovery", "message": idle_msg})
                self.wisdom.push_briefing("Vigilance Recovery", idle_msg, "LOW")

            # 3. Cognitive Buffer Processing
            promoted = self.queue.process_buffer()
            for msg in promoted:
                await self.wal.append("cognition", {"event": "buffer_promotion", "message": msg})
                self.wisdom.push_briefing("Cognitive Buffer Promotion", msg, "MEDIUM")

            # 3. Proactive Intelligence Briefing
            if tick_count % 60 == 0:
                # Assuming ImmuneEngine has a get_status method as previously warned
                swarm_summary = self.thought.summarize_swarm([]) # Passing empty for now to avoid crash
                self.wisdom.push_briefing(
                    title="Swarm Intelligence Summary",
                    content=f"{swarm_summary}\n\n**Current Vibe:** {self.endocrine.get_state().get('vibe', 'Stable')}",
                    salience="LOW"
                )

            tick_count += 1
            await asyncio.sleep(5)

    async def pulse_loop(self):
        while self.running:
            self.metabolism.tick()
            await self.wal.append("pulse", {"tick": time.time()})
            await asyncio.sleep(1)

    async def orchestrator_loop(self):
        while self.running:
            self.endocrine.tick()
            await self.wal.append("orchestrator", {"status": "running"})
            await asyncio.sleep(3)

    async def senses_loop(self):
        while self.running:
            self.respiratory.tick()
            await self.wal.append("senses", {"status": "listening"})
            await asyncio.sleep(2)

    async def guardian_loop(self):
        while self.running:
            self.immune.tick()
            self.lymphatic.tick()
            await self.wal.append("guardian", {"status": "patrolling"})
            await asyncio.sleep(5)

    async def evolution_loop(self):
        """Periodically triggers evolution cycles for self-optimization."""
        while self.running:
            # Evolution is resource intensive, run less frequently (e.g., every 300 pulses)
            await asyncio.sleep(300)
            
            from layers.L04_Composition.evolution_engine import EvolutionEngine
            from layers.L04_Composition.policy_optimizer import PolicyOptimizer
            
            # Check energy status before evolving
            if self.metabolism.state.energy > 50:
                await self.wal.append("evolution", {"event": "generation_start"})
                
                # 1. Optimize Routing Policies
                optimizer = PolicyOptimizer(self.base_dir)
                opt_res = optimizer.optimize_routing()
                
                # 2. Evolve General Population
                evo = EvolutionEngine(self.base_dir, self) # Passing self as physiology proxy
                evo_res = evo.evolve_generation(population_size=10)
                
                await self.wal.append("evolution", {
                    "event": "generation_complete",
                    "routing": opt_res,
                    "general": evo_res
                })

    async def sleep_loop(self):
        """Autonomic sleep/wake cycle: checks idle, advances sleep stages, triggers memory consolidation."""
        while self.running:
            entered_sleep = self.sleep.force_sleep("auto")
            if entered_sleep:
                await self.wal.append("sleep", {"event": "entered_sleep", "stage": "nrem"})

            sleep_state = self.sleep.get_circadian_metrics() if hasattr(self.sleep, "get_circadian_metrics") else {}
            stage = sleep_state.get("stage") if isinstance(sleep_state, dict) else None
            if stage and stage.lower() != "awake":
                self.sleep.record_activity()
                await self.wal.append("sleep", {"event": "stage_change", "stage": stage})

            await asyncio.sleep(10)

    async def start(self):
        self.running = True
        await self.wal.append("runtime", {"status": "started"})
        
        # Start Proactive Sensory Nerves
        self.skin.start_proactive_monitoring()
        
        async with asyncio.TaskGroup() as tg:
            self.tasks = [
                tg.create_task(self.pulse_loop()),
                tg.create_task(self.orchestrator_loop()),
                tg.create_task(self.senses_loop()),
                tg.create_task(self.guardian_loop()),
                tg.create_task(self.sleep_loop()),
                tg.create_task(self.evolution_loop()),
                tg.create_task(self.homeostasis_loop()),
            ]

    async def stop(self):
        self.running = False
        self.skin.stop_proactive_monitoring()
        await self.wal.append("runtime", {"status": "stopped"})

if __name__ == "__main__":
    runtime = NexusRuntime(BASE_DIR)
    try:
        asyncio.run(runtime.start())
    except KeyboardInterrupt:
        print("Stopping runtime...")
        asyncio.run(runtime.stop())
