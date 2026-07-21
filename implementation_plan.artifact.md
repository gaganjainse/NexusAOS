# Phase 7: The Swarm Mind (Multi-Agent Orchestration)

This plan evolves the AOS from a single-node organism to a **Distributed Swarm Intelligence**. It implements the "Distributed Lattice" and "Collective Memory" required to move from an individual agent to a collaborative ecosystem.

## User Review Required

> [!IMPORTANT]
> This phase introduces **Distributed State**. By default, it will use a local file-based "Mesh Simulation" (simulating network nodes via subdirectories or ports). In a production environment, this would transition to real network sockets.

## Proposed Changes

### 1. Protocols: The Synaptic Mesh
Define the rules for inter-node communication.

#### [NEW] [mesh_protocol.md](file:///C:/Users/gagan/Downloads/nexus_corporate_os/archives/core/protocols/mesh_protocol.md)
- Define **"Node Discovery"**: Gossip-based discovery mechanism.
- Define **"Remote Synapses"**: How tasks are fired across different instances.
- Define **"Quorum Consensus"**: Rules for collective decision-making (Quorum = >50% nodes).

---

### 2. Lattice Evolution: The Synaptic Mesh Engine
Upgrade the Nervous System to handle remote handoffs.

#### [NEW] [nexus_mesh.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/tools/nexus_mesh.py)
- A tool for inter-node signaling.
- **Heartbeat Broadcast:** Announces presence to the mesh.
- **Signal Relay:** Forwards local signals to remote nodes.

#### [MODIFY] [nexus_lattice.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/tools/nexus_lattice.py)
- Update `fire_synapse` to check if `to_role` is available on a remote node.
- Integrate with `NexusMesh` for cross-node dispatch.

---

### 3. Memory Evolution: Collective Hippocampus
Ensure the swarm shares a unified knowledge graph.

#### [NEW] [collective_memory.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/tools/collective_memory.py)
- A wrapper around `MemoryReceptor`.
- **Sync Pulse:** Periodic sync of entities across the mesh.
- **Conflict Resolution:** Last-Writer-Wins (LWW) based on timestamps for entity properties.

---

### 4. Swarm Intelligence: Quorum Sensing
Implement collective intelligence in the executor.

#### [MODIFY] [swarm_executor.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/tools/swarm_executor.py)
- Add **"Role Affinity"** logic: Direct tasks to the node/swarm best suited for them (e.g., node with high energy + specific tools).
- Implement **"Quorum Check"**: Blocking tasks until a specified number of agents/nodes agree on the result.

---

### 5. Integration: MCP Registry
Expose the Swarm Mind to the Sovereign.

#### [MODIFY] [index.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/index.py)
- Add `@mcp.tool() get_mesh_status()`.
- Add `@mcp.tool() broadcast_directive()`.
- Add `@mcp.tool() trigger_quorum_vote()`.

---

## Verification Plan

### Automated Tests
- Spawn two simulated nodes and verify that a synapse fired on Node A is received and processed by a role on Node B.
- Verify that an entity stored in Node A's memory is visible to Node B after a Sync Pulse.

### Manual Verification
- Check the "Mesh" tab in the Neural Terminal (to be added) to see active nodes.
- Submit a "Broadcast Directive" and verify multiple agents across different "swarms" respond.
