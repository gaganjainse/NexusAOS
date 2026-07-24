# Document: Orchestrator Runtime Protocol
Version 1.0 (Golden Master)

## Overview
**Branch:** HQ / NCC
**Level:** Protocol
**Superior:** THE SOVEREIGN

## Purpose
To provide an **always-on CPU loop** that closes the perception-action cycle without requiring external LLM or manual MCP invocation. The Orchestrator is the autonomous executive that routes signals, directives, and maintenance.

## The Closed Loop
```
Senses (poll) -> Signals (TTL) -> Orchestrator (decide) -> Lattice (handoff) -> Motor (execute) -> Memory (consolidate)
```

## Tick Cycle (Healthy: 3s)
1. **Perceive:** Read new sensory events since last tick.
2. **Interpret:** Match active hormonal signals to routing table.
3. **Direct:** Process sovereign directive inbox (priority queue).
4. **Act:** Execute routed actions (heal, reforge, intel, motor, filtrate, dream).
5. **Maintain:** Auto-filtration, fever response, motor drain, vibe synthesis.

## Sovereign Directive Inbox
- **Path:** `core/monitoring/directive_inbox.json`
- **Submission:** GUI terminal, MCP `submit_directive`, or external agent.
- **Parsing:** Keyword-based routing (repair, intel, diagnose, clean, dream, motor).

## Routing Weights (Learning)
- **Path:** `core/monitoring/routing_weights.json`
- Success/failure counts per signal type inform future routing confidence.

## Service Supervision
- **Supervisor:** `Sesha_supervisor.py` boots and restarts: Pulse, Guardian, Senses, Orchestrator.
- **Heartbeats:** `core/monitoring/heartbeats/*.json`
- **Boot command:** MCP `boot_Sesha_aos()`

## Approval Authority
| Area | Authority |
| :--- | :--- |
| **Routing table changes** | Chief Agentic Officer (CAO) |
| **Supervisor overrides** | THE SOVEREIGN |

---

> [!IMPORTANT]
> Without the Orchestrator running, SeshaAOS reverts to passive documentation. The Supervisor must be running for true AGOI runtime.

**Navigation:** [Global Dashboard](../foundation/corporate_os_handbook.md) | [Sensory Protocol](./sensory_protocol.md)
