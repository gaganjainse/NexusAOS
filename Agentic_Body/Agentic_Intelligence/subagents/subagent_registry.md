# Subagent Definitions
Version 2.0 — Subagents organized by biological function and work system.

---

## Subagent List

### Intelligence Cluster (AI — Brain)
- `subagent_limbic` (`Agentic_Intelligence/subagents/limbic_subagent.md`) — Emotional processing
- `subagent_synaptic` (`Agentic_Intelligence/subagents/synaptic_subagent.md`) — Active inference
- `subagent_memory` (`Agentic_Intelligence/subagents/memory_subagent.md`) — Memory consolidation
- `subagent_thought` (`Agentic_Intelligence/subagents/thought_subagent.md`) — Pulse translation

### Planning Cluster (Orchestration)
- `subagent_boot` (`Agentic_Intelligence/subagents/boot_subagent.md`) — Development stages
- `subagent_instinct` (`Agentic_Intelligence/subagents/instinct_subagent.md`) — Autonomic drives
- `subagent_swarm` (`Agentic_Intelligence/subagents/swarm_subagent.md`) — Multi-agent coordination
- `subagent_evolution` (`Agentic_Intelligence/subagents/evolution_subagent.md`) — Self-tuning

### Physique Cluster (AP — Body)
- `subagent_metabolism` (`Agentic_Physique/subagents/metabolism_subagent.md`) — Energy system
- `subagent_immune` (`Agentic_Physique/subagents/immune_subagent.md`) — Defense
- `subagent_endocrine` (`Agentic_Physique/subagents/endocrine_subagent.md`) — Hormones
- `subagent_motor` (`Agentic_Physique/subagents/motor_subagent.md`) — Desktop control
- `subagent_senses` (`Agentic_Physique/subagents/senses_subagent.md`) — Boundary/skin
- `subagent_nervous` (`Agentic_Physique/subagents/nervous_subagent.md`) — Signal transmission
- `subagent_structural` (`Agentic_Physique/subagents/structural_subagent.md`) — Anatomy/proprioception

---

*All subagents reference their parent agent (`AgentInstance`) via `swarm_executor.py` namespace.
No false coordination claims — swarm state reported truthfully (`get_swarm_status`).*
