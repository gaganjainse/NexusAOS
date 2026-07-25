# Document: Synaptic Mesh Protocol
Version: 1.0.0
Branch: Core
Level: Protocol
Superior: Sesha Orchestrator

## Overview
The **Synaptic Mesh** is the communication layer that enables multiple **Agentic Bodies (AB)** to coordinate as a single **Distributed Swarm Intelligence**. It extends the local Lattice across networked nodes.

## 1. Node Discovery (Gossip)
Each node in the mesh must autonomously discover and maintain a list of active peers.
- **Heartbeat:** Every 60s, a node broadcasts its presence (ID, Energy, Roles, Load).
- **Gossip:** Nodes exchange peer lists to ensure the entire mesh is mapped without a central server.
- **Node State:**
    - **Active:** Responding to heartbeats.
    - **Degraded:** High latency or low energy (>80% cortisol).
    - **Orphaned:** No heartbeat for 300s (removed from lattice).

## 2. Remote Synapses
Synapses can be "Fired" across the mesh to target roles on remote nodes.
- **Targeting:** A synapse targets a `Role`. The mesh routes it to the node with the highest **Role Affinity** and **Energy**.
- **Payload:** Must include `Directive_ID`, `Context`, and `Sovereign_Sign_Off`.
- **Response:** Remote nodes must return a `Synapse_Result` or an `Error_Ischemia` if the node fails during processing.

## 3. Quorum Consensus
High-risk directives (e.g., spending tokens, modifying DNA) require a **Quorum Vote**.
- **Threshold:** >50% of active nodes must approve.
- **Voters:** Only "Healthy" nodes with >30% energy can vote.
- **Finality:** Once quorum is reached, the directive is executed on the primary node.

## 4. Collective Synchronization
- **Clock:** Nodes sync via a biological "Drift" mechanism, allowing for +/- 100ms tolerance.
- **State:** `lattice_state.json` is partially synced to provide "Proprioception" of the entire swarm.

---

> [!CAUTION]
> A node undergoing **Sepsis** (critical code corruption) must be isolated from the mesh immediately to prevent signal contamination.