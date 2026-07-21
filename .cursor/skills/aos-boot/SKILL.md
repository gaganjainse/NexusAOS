---
name: aos-boot
description: Boot and verify the AOS biological runtime. USE when starting the system, checking service health, or diagnosing failures.
---

# AOS Boot Skill

## Boot Sequence
1. Call MCP tool `boot_nexusaos` — starts Supervisor (pulse, guardian, senses, orchestrator)
2. Call `get_service_heartbeats` — verify all services alive
3. Call `diagnose_os` — full system check
4. Call `get_orchestrator_status` — confirm CPU loop running

## If Services Stale
- `start_circulatory_system` — pulse
- `start_guardian_service` — immune
- `start_sensory_system` — nerves
- `start_orchestrator` — CPU

## Physiology Check
- `get_energy_status`
- `get_global_vibe`
- `get_immune_status`
- `get_physiological_dampening`
