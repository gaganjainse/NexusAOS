# Document: Physiological Dampening Protocol
Version 1.0 (Golden Master)

## Overview
**Branch:** Core
**Level:** Protocol
**Superior:** Chief Agentic Officer (CAO)

## Purpose
To convert hormonal state from advisory metadata into **physical constraints** on tool execution. When the OS is stressed, high-risk operations are biologically blocked at the MCP middleware layer.

## Gated Tools
| Tool | Block Condition |
| :--- | :--- |
| `propose_dna_mutation` | Cortisol > 90% OR Energy < 20% OR Threat > Inflammation |
| `spawn_child_instance` | Cortisol > 70% OR Energy < 50% OR Threat > Fever |
| `generate_spore_export` | Energy < 30% OR Threat > Fever |
| `trigger_self_healing` | Cortisol > 95% |

## Enforcement Layer
- **Gate:** `physiological_gate.py`
- **Integration:** MCP tool registry (`index.py`) checks gate before execution.
- **Response:** `PERMISSION DENIED` with physiological reason.

## Approval Authority
| Area | Authority |
| :--- | :--- |
| **Threshold Tuning** | Chief Agentic Officer (CAO) |
| **Gate Override** | THE SOVEREIGN |

---

> [!CAUTION]
> Law I (Sovereign Supremacy) cannot be dampened. The Sovereign retains override authority outside the automated gate.

**Navigation:** [Global Dashboard](../foundation/corporate_os_handbook.md) | [Mood Protocol](./mood_protocol.md)
