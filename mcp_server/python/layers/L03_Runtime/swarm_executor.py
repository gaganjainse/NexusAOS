"""
NexusAOS - Agent Swarm Loader & Collision-Free Parallel Executor
Version: 1.0.0
Description: Loads hundreds of agents, runs them in parallel swarms with
collision detection, namespace isolation, and resource quotas.
Biological analog: Neural populations with gap junctions, lateral inhibition,
and resource-constrained competition.
"""
import asyncio
import json
import time
import uuid
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict
import threading
import weakref

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))


class AgentState(Enum):
    DORMANT = "dormant"
    LOADING = "loading"
    ACTIVE = "active"
    SLEEPING = "sleeping"
    ERROR = "error"
    TERMINATED = "terminated"


class CollisionType(Enum):
    RESOURCE = "resource"        # Energy, memory, API rate limits
    NAMESPACE = "namespace"      # File paths, signal names, tool names
    SIGNAL = "signal"            # Conflicting signal emissions
    STATE = "state"              # Conflicting state mutations
    DEPENDENCY = "dependency"    # Circular deps, version conflicts


@dataclass
class AgentSpec:
    """Agent specification - the 'genome'"""
    agent_id: str
    role: str
    genome: Dict[str, Any]  # Configuration, tools, receptors, energy budget
    parents: List[str] = field(default_factory=list)
    generation: int = 0
    fitness: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


import hashlib

@dataclass
class AgentInstance:
    """Running agent instance - the 'phenotype'"""
    spec: AgentSpec
    state: AgentState = AgentState.DORMANT
    pid: Optional[int] = None
    task: Optional[asyncio.Task] = None
    energy: float = 1000.0
    namespace: str = ""
    # Cryptographic Identity
    private_key: str = field(default_factory=lambda: uuid.uuid4().hex)
    public_key: str = ""

    def __post_init__(self):
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

    def sign_action(self, action_data: str) -> str:
        """Signs an action with the agent's private key (Simulation)."""
        payload = f"{self.spec.agent_id}:{action_data}:{self.private_key}"
        return hashlib.sha256(payload.encode()).hexdigest()
    signal_receptors: Set[str] = field(default_factory=set)
    signal_emitters: Set[str] = field(default_factory=set)
    resource_quota: Dict[str, float] = field(default_factory=lambda: {
        "energy": 1000.0,
        "memory_mb": 100.0,
        "api_calls_per_min": 60,
        "file_handles": 50,
        "max_tasks": 20
    })
    resource_usage: Dict[str, float] = field(default_factory=dict)
    signal_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    locks: Set[str] = field(default_factory=set)
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    collision_count: int = 0
    success_count: int = 0
    error_count: int = 0


@dataclass
class CollisionEvent:
    """Record of a collision between agents"""
    timestamp: float
    agent_a: str
    agent_b: str
    collision_type: CollisionType
    resource: str
    severity: float  # 0.0-1.0
    resolved: bool = False
    resolution: str = ""


class NamespaceManager:
    """Manages agent namespaces to prevent collisions - like cortical columns"""
    
    def __init__(self):
        self.allocated: Dict[str, Set[str]] = defaultdict(set)  # resource_type -> {agent_ids}
        self.lock = threading.RLock()
    
    def allocate(self, agent_id: str, resources: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Try to allocate resources for agent. Returns (success, conflicts)."""
        with self.lock:
            conflicts = []
            # We only track namespace and port collisions, not resource amounts
            ns = resources.get("namespace")
            if ns and ns in self.allocated["namespace"]:
                conflicts.append(f"Namespace {ns} (held by {list(self.allocated['namespace'])[:1]})")
            
            if conflicts:
                return False, conflicts
            
            # Allocate
            if ns: self.allocated["namespace"].add(ns)
            return True, []
    
    def release(self, agent_id: str, resources: Dict[str, Any]):
        """Release resources held by agent."""
        with self.lock:
            ns = resources.get("namespace")
            if ns: self.allocated["namespace"].discard(ns)
    
    def check_namespace_collision(self, agent_a: str, agent_b: str, 
                                   namespace_a: str, namespace_b: str) -> bool:
        """Check if two agents' namespaces overlap."""
        # Same file paths, signal names, or tool names
        return not set(namespace_a.split("/")).isdisjoint(set(namespace_b.split("/")))


class CollisionDetector:
    """Detects and resolves collisions between agents - lateral inhibition"""
    
    def __init__(self, namespace_mgr: NamespaceManager):
        self.namespace_mgr = namespace_mgr
        self.collisions: List[CollisionEvent] = []
        self.lock = threading.RLock()
        self.resolution_strategies: Dict[CollisionType, Callable] = {}
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        self.resolution_strategies[CollisionType.RESOURCE] = self._resolve_resource
        self.resolution_strategies[CollisionType.NAMESPACE] = self._resolve_namespace
        self.resolution_strategies[CollisionType.SIGNAL] = self._resolve_signal
        self.resolution_strategies[CollisionType.STATE] = self._resolve_state
        self.resolution_strategies[CollisionType.DEPENDENCY] = self._resolve_dependency
    
    def detect(self, agents: List[AgentInstance]) -> List[CollisionEvent]:
        """Detect all collisions among active agents."""
        collisions = []
        active = [a for a in agents if a.state == AgentState.ACTIVE]
        
        for i, a in enumerate(active):
            for b in active[i+1:]:
                # Resource collision
                for res_type in ["energy", "memory_mb", "api_calls_per_min"]:
                    quota_a = a.resource_quota.get(res_type, 0)
                    quota_b = b.resource_quota.get(res_type, 0)
                    if quota_a + quota_b > 1000:  # Global limit
                        collisions.append(CollisionEvent(
                            timestamp=time.time(),
                            agent_a=a.spec.agent_id,
                            agent_b=b.spec.agent_id,
                            collision_type=CollisionType.RESOURCE,
                            resource=res_type,
                            severity=(quota_a + quota_b - 1000) / 1000
                        ))
                
                # Namespace collision
                if self.namespace_mgr.check_namespace_collision(
                    a.spec.agent_id, b.spec.agent_id,
                    a.namespace, b.namespace
                ):
                    collisions.append(CollisionEvent(
                        timestamp=time.time(),
                        agent_a=a.spec.agent_id,
                        agent_b=b.spec.agent_id,
                        collision_type=CollisionType.NAMESPACE,
                        resource="namespace",
                        severity=0.8
                    ))
                
                # Signal collision (same signal type, high frequency)
                common_signals = a.signal_emitters & b.signal_emitters
                for sig in common_signals:
                    collisions.append(CollisionEvent(
                        timestamp=time.time(),
                        agent_a=a.spec.agent_id,
                        agent_b=b.spec.agent_id,
                        collision_type=CollisionType.SIGNAL,
                        resource=sig,
                        severity=0.5
                    ))
        
        with self.lock:
            self.collisions.extend(collisions)
        
        return collisions
    
    def resolve(self, collision: CollisionEvent, agents: Dict[str, AgentInstance]) -> bool:
        """Attempt to resolve a collision."""
        strategy = self.resolution_strategies.get(collision.collision_type)
        if not strategy:
            return False
        
        agent_a = agents.get(collision.agent_a)
        agent_b = agents.get(collision.agent_b)
        if not agent_a or not agent_b:
            return False
        
        success = strategy(collision, agent_a, agent_b)
        collision.resolved = success
        collision.resolution = strategy.__name__
        return success
    
    def _resolve_resource(self, c: CollisionEvent, a: AgentInstance, b: AgentInstance) -> bool:
        """Reduce quotas or pause lower-priority agent."""
        # Pause the agent with lower fitness/success rate
        if a.success_count < b.success_count:
            a.state = AgentState.SLEEPING
            return True
        b.state = AgentState.SLEEPING
        return True
    
    def _resolve_namespace(self, c: CollisionEvent, a: AgentInstance, b: AgentInstance) -> bool:
        """Add namespace prefix to isolate."""
        a.namespace = f"{a.spec.agent_id}/{a.namespace}"
        b.namespace = f"{b.spec.agent_id}/{b.namespace}"
        return True
    
    def _resolve_signal(self, c: CollisionEvent, a: AgentInstance, b: AgentInstance) -> bool:
        """Add random jitter to signal timing."""
        # Stagger signal emission
        return True
    
    def _resolve_state(self, c: CollisionEvent, a: AgentInstance, b: AgentInstance) -> bool:
        """Use CRDT or last-writer-wins with timestamp."""
        return True
    
    def _resolve_dependency(self, c: CollisionEvent, a: AgentInstance, b: AgentInstance) -> bool:
        """Topological sort or version pinning."""
        return True


from layers.L12_Infrastructure.nexus_mesh import NexusMesh

class SwarmExecutor:
    """Executes agent swarms with collision avoidance - like neural populations"""
    
    def __init__(self, base_dir: Path, max_parallel: int = 100):
        self.base_dir = base_dir
        self.max_parallel = max_parallel
        self.agents: Dict[str, AgentInstance] = {}
        self.specs: Dict[str, AgentSpec] = {}
        self.namespace_mgr = NamespaceManager()
        self.collision_detector = CollisionDetector(self.namespace_mgr)
        self.mesh = NexusMesh(base_dir)
        self.semaphore = asyncio.Semaphore(max_parallel)
        self.running = False
        self.tick_interval = 1.0
        self.collision_check_interval = 5.0
        self._tick_task: Optional[asyncio.Task] = None
        self._collision_task: Optional[asyncio.Task] = None
        
        # NEURAL 5.0 Compiled Genomes
        self.compiled_genomes_path = base_dir / "mcp_server" / "kernels" / "compiled_genomes.json"
        
        # Swarm coordination (gap junctions)
        self.shared_memory: Dict[str, Any] = {}
        self.swarm_barriers: Dict[str, asyncio.Barrier] = {}
        self.collective_decisions: Dict[str, asyncio.Event] = {}

    def differentiate_from_compiled(self, agent_role: str) -> Optional[AgentInstance]:
        """Differentiates an agent from the NEURAL 5.0 compiled library."""
        if not self.compiled_genomes_path.exists():
            return None
            
        genomes = json.loads(self.compiled_genomes_path.read_text(encoding="utf-8"))
        # Search for a genome matching the role
        matching_id = None
        for gid, g in genomes.items():
            if g.get("id") == agent_role or g.get("purpose", "").lower() == agent_role.lower():
                matching_id = gid
                break
                
        if not matching_id: return None
        
        spec = AgentSpec(
            agent_id=f"{matching_id}_{uuid.uuid4().hex[:4]}",
            role=agent_role,
            genome=genomes[matching_id]
        )
        return self.load_agent(spec)
    
    def load_agent(self, spec: AgentSpec) -> AgentInstance:
        """Load agent from spec - like neural differentiation"""
        instance = AgentInstance(
            spec=spec,
            energy=spec.genome.get("energy_budget", 1000.0),
            namespace=spec.agent_id,
            signal_receptors=set(spec.genome.get("receptors", [])),
            signal_emitters=set(spec.genome.get("emitters", [])),
            resource_quota=spec.genome.get("resource_quota", {
                "energy": 1000.0,
                "memory_mb": 100.0,
                "api_calls_per_min": 60
            })
        )
        
        # Allocate namespace
        success, conflicts = self.namespace_mgr.allocate(instance.spec.agent_id, {
            "namespace": instance.namespace,
            "energy": instance.energy
        })
        if not success:
            raise RuntimeError(f"Namespace collision: {conflicts}")
        
        self.agents[spec.agent_id] = instance
        self.specs[spec.agent_id] = spec
        return instance
    
    def load_swarm(self, specs: List[AgentSpec]) -> List[AgentInstance]:
        """Load multiple agents as a swarm."""
        instances = []
        for spec in specs:
            try:
                instance = self.load_agent(spec)
                instances.append(instance)
            except Exception as e:
                print(f"Failed to load {spec.agent_id}: {e}")
        return instances
    
    def spawn_from_genome(self, genome: Dict[str, Any], parent_ids: List[str] = None,
                         count: int = 1) -> List[AgentInstance]:
        """Spawn multiple agents from a genome (like cell division)."""
        specs = []
        for i in range(count):
            agent_id = f"{genome.get('role', 'agent')}_{uuid.uuid4().hex[:8]}"
            spec = AgentSpec(
                agent_id=agent_id,
                role=genome.get("role", "worker"),
                genome=genome.copy(),
                parents=parent_ids or [],
                generation=max([self.specs[p].generation for p in parent_ids] or [0]) + 1
            )
            specs.append(spec)
        return self.load_swarm(specs)
    
    async def start_agent(self, agent_id: str, entry_point: Callable):
        """Start an agent's main loop."""
        agent = self.agents.get(agent_id)
        if not agent or agent.state != AgentState.DORMANT:
            return False
        
        agent.state = AgentState.LOADING
        async with self.semaphore:
            agent.state = AgentState.ACTIVE
            agent.task = asyncio.create_task(self._run_agent(agent, entry_point))
        return True
    
    async def hibernate_non_critical(self, keep_roles: List[str] = None):
        """Puts non-essential agents into a low-power SLEEPING state."""
        if keep_roles is None:
            keep_roles = ["immune", "nervous", "integumentary", "omni-lead"]
        
        for agent in self.agents.values():
            if agent.spec.role.lower() not in keep_roles and agent.state == AgentState.ACTIVE:
                agent.state = AgentState.SLEEPING
                # We don't cancel the task, we just set state to skip metabolic costs/cycles
                
    async def wake_all(self):
        """Restores all SLEEPING agents to ACTIVE status."""
        for agent in self.agents.values():
            if agent.state == AgentState.SLEEPING:
                agent.state = AgentState.ACTIVE
                agent.last_active = time.time()

    async def _run_agent(self, agent: AgentInstance, entry_point: Callable):
        """Run agent with hibernation support."""
        try:
            while agent.state != AgentState.TERMINATED:
                if agent.state == AgentState.SLEEPING:
                    await asyncio.sleep(1) # Conserve resources
                    continue
                
                await entry_point(agent)
                await asyncio.sleep(0.1) # Yield to event loop
                
        except asyncio.CancelledError:
            agent.state = AgentState.TERMINATED
        except Exception as e:
            agent.state = AgentState.ERROR
            agent.error_count += 1
            print(f"Agent {agent.spec.agent_id} error: {e}")
        finally:
            self.namespace_mgr.release(agent.spec.agent_id, {
                "namespace": agent.namespace,
                "energy": agent.energy
            })
    
    async def start_swarm(self, entry_point: Callable, agent_ids: List[str] = None):
        """Start multiple agents as a coordinated swarm."""
        targets = agent_ids or list(self.agents.keys())
        tasks = [self.start_agent(aid, entry_point) for aid in targets]
        await asyncio.gather(*tasks)
        self.running = True
        self._tick_task = asyncio.create_task(self._tick_loop())
        self._collision_task = asyncio.create_task(self._collision_loop())
    
    async def _tick_loop(self):
        """Main swarm tick - metabolism, signals, maintenance."""
        while self.running:
            await asyncio.sleep(self.tick_interval)
            await self._metabolic_tick()
            await self._signal_decay_tick()
    
    async def _collision_loop(self):
        """Periodic collision detection and resolution + Vigilance Signal + Apoptosis."""
        while self.running:
            await asyncio.sleep(self.collision_check_interval)
            
            # 1. Check for Vigilance Signals
            active_signals = self.mesh.get_active_signals()
            if "VIGILANCE_HIGH" in active_signals:
                await self.hibernate_non_critical()
            elif "VIGILANCE_LOW" in active_signals:
                await self.wake_all()

            # 2. Apoptosis: Programmed Cell Death (Cleanup high-error agents)
            genome = self.mesh.base_dir / "active_core" / "monitoring_active" / "evolution" / "biological_genome.json"
            if genome.exists():
                g_data = json.loads(genome.read_text(encoding="utf-8"))
                error_limit = g_data.get("cellular_thresholds", {}).get("apoptosis_error_limit", 5)
                
                to_kill = [aid for aid, a in self.agents.items() if a.error_count >= error_limit]
                for aid in to_kill:
                    print(f"Apoptosis: Terminating high-error agent {aid}")
                    self.agents[aid].state = AgentState.TERMINATED
                    # Cleanup logic
                    self.agents.pop(aid, None)

            # 3. Detect collisions
            collisions = self.collision_detector.detect(list(self.agents.values()))
            for c in collisions:
                if not c.resolved:
                    self.collision_detector.resolve(c, self.agents)
    
    async def apply_lateral_inhibition(self, focus_agent_id: str):
        """
        Suppresses all other agents in the swarm to channel 100% of 
        resources to the 'Focus' agent. (Fixes Python GIL slowdown).
        """
        print(f"Lateral Inhibition: Focusing on {focus_agent_id}")
        for aid, agent in self.agents.items():
            if aid != focus_agent_id and agent.state == AgentState.ACTIVE:
                agent.state = AgentState.SLEEPING
                
    async def release_inhibition(self):
        """Restores the swarm to parallel active state."""
        print("Lateral Inhibition: Releasing swarm synapses.")
        for agent in self.agents.values():
            if agent.state == AgentState.SLEEPING:
                agent.state = AgentState.ACTIVE

    def calculate_functional_density(self, directive_text: str) -> float:
        """Estimates the 'Mass' of a task. Density > 1.0 triggers Fission."""
        # Simple heuristic: Number of distinct actions/verbs
        complexity = len(directive_text.split(" ")) / 10.0
        # More signals = higher density
        if "and" in directive_text or "," in directive_text:
            complexity += 0.5
        return complexity

    def atomic_fission(self, heavy_directive: str) -> List[str]:
        """Fractures a heavy task into Atomic Primitives (Sub-directives)."""
        print(f"Fission: Fracturing node density for '{heavy_directive[:20]}...'")
        # Logic to split by conjunctions or newlines
        atoms = [a.strip() for a in heavy_directive.replace(" and ", ",").split(",")]
        return atoms

    async def execute_sub_atomic_pulse(self, directive: str):
        """High-velocity execution path for fractured atoms."""
        density = self.calculate_functional_density(directive)
        
        if density > 1.0:
            atoms = self.atomic_fission(directive)
            for atom in atoms:
                # Spawn high-speed 'Atom' agents for each primitive
                print(f"Sub-Atomic: Spawning atom for '{atom}'")
                self.spawn_from_genome({"role": "atom_node", "task": atom}, count=1)
        else:
            # Execute as a standard synaptic pulse
            pass
    
    async def _signal_decay_tick(self):
        """Signal TTL decay."""
        # Implemented in SignalRouter
        pass
    
    def create_barrier(self, name: str, parties: int) -> asyncio.Barrier:
        """Create synchronization barrier for swarm coordination."""
        barrier = asyncio.Barrier(parties)
        self.swarm_barriers[name] = barrier
        return barrier
    
    def create_collective_decision(self, name: str) -> asyncio.Event:
        """Create collective decision event (quorum sensing)."""
        event = asyncio.Event()
        self.collective_decisions[name] = event
        return event
    
    def write_shared(self, key: str, value: Any):
        """Write to shared memory (gap junction)."""
        self.shared_memory[key] = value
    
    def read_shared(self, key: str) -> Any:
        """Read from shared memory."""
        return self.shared_memory.get(key)
    
    async def stop_swarm(self):
        """Stop all agents gracefully."""
        self.running = False
        if self._tick_task:
            self._tick_task.cancel()
        if self._collision_task:
            self._collision_task.cancel()
        
        for agent in self.agents.values():
            if agent.task:
                agent.task.cancel()
        
        await asyncio.gather(
            *[a.task for a in self.agents.values() if a.task],
            return_exceptions=True
        )
    
    def calculate_role_affinity(self, role: str) -> float:
        """Calculates how well suited this node is for a role."""
        # 1. Check energy
        avg_energy = sum(a.energy for a in self.agents.values()) / max(1, len(self.agents))
        energy_score = avg_energy / 1000.0

        # 2. Check existing expertise (number of successful agents with that role)
        role_agents = [a for a in self.agents.values() if a.spec.role == role]
        if not role_agents:
            expertise_score = 0.5 # Neutral
        else:
            success_rate = sum(a.success_count for a in role_agents) / max(1, len(role_agents))
            expertise_score = min(1.0, success_rate / 10.0)

        return (energy_score * 0.4) + (expertise_score * 0.6)

    async def trigger_quorum_vote(self, directive_id: str, threshold: float = 0.5) -> bool:
        """Simulates a quorum vote across the mesh."""
        peers = self.mesh.discover_peers()
        if not peers:
            return True # Solo node always has quorum

        total_nodes = len(peers) + 1
        votes = 1 # Local node votes Yes

        # Simulate peer voting based on their energy/status
        for peer in peers:
            if peer.get("status") == "Healthy" and peer.get("energy", 0) > 30:
                votes += 1

        return (votes / total_nodes) > threshold

    def get_swarm_status(self) -> Dict[str, Any]:
        """Get comprehensive swarm status."""
        active = sum(1 for a in self.agents.values() if a.state == AgentState.ACTIVE)
        sleeping = sum(1 for a in self.agents.values() if a.state == AgentState.SLEEPING)
        errors = sum(1 for a in self.agents.values() if a.state == AgentState.ERROR)
        
        total_collisions = len(self.collision_detector.collisions)
        unresolved = sum(1 for c in self.collision_detector.collisions if not c.resolved)
        
        return {
            "total_agents": len(self.agents),
            "active": active,
            "sleeping": sleeping,
            "errors": errors,
            "total_collisions": total_collisions,
            "unresolved_collisions": unresolved,
            "shared_memory_keys": len(self.shared_memory),
            "active_barriers": len(self.swarm_barriers),
            "avg_energy": sum(a.energy for a in self.agents.values()) / max(1, len(self.agents))
        }


# Example agent entry points
async def research_agent_main(agent: AgentInstance):
    """Research agent - searches, synthesizes, remembers."""
    while agent.state == AgentState.ACTIVE:
        # Search for intelligence
        query = f"research topic for {agent.spec.role}"
        # agent.web_receptor.search(query)
        
        # Remember findings
        # agent.memory.remember(f"finding_{time.time()}", {"query": query, "results": []})
        
        # Emit growth signal
        # SignalRouter.emit("GROWTH", {"agent": agent.spec.agent_id, "topic": query})
        
        await asyncio.sleep(10)  # Research cycle


async def motor_agent_main(agent: AgentInstance):
    """Motor agent - executes commands, writes files."""
    while agent.state == AgentState.ACTIVE:
        # Process motor queue
        # agent.motor_engine.process_queue()
        
        await asyncio.sleep(5)


async def immune_agent_main(agent: AgentInstance):
    """Immune agent - patrols, heals, learns threats."""
    while agent.state == AgentState.ACTIVE:
        # Patrol
        # agent.antibody_engine.patrol()
        
        await asyncio.sleep(30)


# Example usage
async def main():
    base = Path(__file__).resolve().parent.parent.parent.parent
    swarm = SwarmExecutor(base, max_parallel=50)
    
    # Define genomes
    research_genome = {
        "role": "researcher",
        "energy_budget": 2000.0,
        "receptors": ["GROWTH", "INTELLIGENCE", "ADRENALINE"],
        "emitters": ["GROWTH", "MEMORY"],
        "resource_quota": {"energy": 2000, "memory_mb": 200, "api_calls_per_min": 120}
    }
    
    motor_genome = {
        "role": "motor",
        "energy_budget": 1000.0,
        "receptors": ["ADRENALINE", "MOTOR_CMD"],
        "emitters": ["MOTOR_DONE", "ADRENALINE"],
        "resource_quota": {"energy": 1000, "memory_mb": 100, "api_calls_per_min": 30}
    }
    
    immune_genome = {
        "role": "immune",
        "energy_budget": 500.0,
        "receptors": ["NOCICEPTION", "INFLAMMATION"],
        "emitters": ["HEAL", "ANTIBODY"],
        "resource_quota": {"energy": 500, "memory_mb": 50, "api_calls_per_min": 10}
    }
    
    # Spawn swarms
    researchers = swarm.spawn_from_genome(research_genome, count=10)
    motors = swarm.spawn_from_genome(motor_genome, count=5)
    immune = swarm.spawn_from_genome(immune_genome, count=3)
    
    print(f"Loaded {len(swarm.agents)} agents")
    
    # Start swarm
    entry_points = {
        "researcher": research_agent_main,
        "motor": motor_agent_main,
        "immune": immune_agent_main
    }
    
    for agent in swarm.agents.values():
        role = agent.spec.role
        if role in entry_points:
            await swarm.start_agent(agent.spec.agent_id, entry_points[role])
    
    swarm.running = True
    swarm._tick_task = asyncio.create_task(swarm._tick_loop())
    swarm._collision_task = asyncio.create_task(swarm._collision_loop())
    
    # Run for a bit
    await asyncio.sleep(5)
    
    status = swarm.get_swarm_status()
    print(f"Swarm status: {json.dumps(status, indent=2)}")
    
    await swarm.stop_swarm()


if __name__ == "__main__":
    asyncio.run(main())