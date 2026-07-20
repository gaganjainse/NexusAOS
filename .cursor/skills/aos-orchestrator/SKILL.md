---
name: aos-orchestrator
description: Submit directives and monitor the AOS Orchestrator closed loop. USE for autonomous task execution.
---

# AOS Orchestrator Skill

## Submit Directives
Use `submit_directive(text, priority)` where priority 1-10 (10 = urgent).

## Directive Keywords
- heal / repair / fix → self-healing
- intel / scrape / oracle → intelligence collection
- diagnose / status → system diagnostics
- clean / filtrate / liver → waste removal
- dream / consolidate / memory → dream cycle
- MOTOR:write:path:content → autonomous file write

## Monitor
- `get_orchestrator_status` — tick count, pending directives
- `get_lattice_state` — active synapses
- `get_motor_status` — motor action log
- `get_sensory_feed` — recent perception events
