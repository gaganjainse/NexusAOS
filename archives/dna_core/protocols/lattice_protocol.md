# Document: Lattice Protocol
Version 1.0 (Golden Master)

## Overview
**Branch:** Core
**Level:** Protocol
**Superior:** Chief Agentic Officer (CAO)

## Purpose
To define the **"Nervous System"** of the SeshaAOS, enabling complex inter-agent coordination, context-aware handoffs, and system-wide proprioception.

## Synaptic Handoffs
A handoff occurs when one role (the **Firing Node**) transfers authority and context to another role (the **Target Node**).
- **Synchronous:** The Firing Node waits for a response (blocking).
- **Asynchronous:** The Firing Node continues while the Target Node processes in the background.
- **Context Injection:** Every handoff MUST include the `Sovereign_Directive_ID` and the `Current_System_State`.

## Node States
| State | Description |
| :--- | :--- |
| **Resting** | The node is inactive and frozen in the registry. |
| **Firing** | The node is actively processing a directive. |
| **Blocked** | The node is waiting for a synapse response from a downstream role. |
| **Refractory** | The node has completed a task and is undergoing "Memory Consolidation" (logging). |

## Axon Routing
Directives follow the hierarchy defined in the **Job Matrix**. 
- **Ascending:** Escalation to a Superior.
- **Descending:** Delegation to a Subordinate.
- **Lateral:** Coordination with a Peer in the same Branch.

## Approval Authority
| Area | Authority |
| :--- | :--- |
| **Synapse Prioritization** | Sesha Orchestrator Agent |
| **Hierarchy Resolution** | Chief Knowledge Officer (CKO) |

---

> [!IMPORTANT]
> A node may only "Fire" if it has sufficient **Metabolic Energy** (>10%). If energy is Critical, the Nervous System enters a forced stasis.

**Navigation:** [Global Dashboard](../foundation/aos_handbook.md) | [Circulatory Protocol](./circulatory_protocol.md)
