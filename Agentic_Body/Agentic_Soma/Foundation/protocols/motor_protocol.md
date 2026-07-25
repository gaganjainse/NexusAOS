# Document: Motor Agency Protocol
Version 1.0 (Golden Master)

## Overview
**Branch:** Core
**Level:** Protocol
**Superior:** Sesha Orchestrator Agent

## Purpose
To give **SeshaAOS** autonomous execution capability — the "Hand" that translates lattice directives into file writes, builds, and deployments without Sovereign hand-holding.

## Motor Actions
| Action | Description | Risk |
| :--- | :--- | :--- |
| `write_file` | Create or overwrite a file within the OS boundary | Medium |
| `append_file` | Append content to an existing file | Low |
| `run_command` | Execute a shell command from the allowlist | High |
| `complete_synapse` | Mark a lattice task complete with result | Low |

## Safety Boundaries
- All file paths must resolve inside the OS `base_dir`.
- Protected paths (`archives/dna_core/foundation`, Law I constitution) require Sovereign override.
- Commands matching destructive patterns are blocked at the motor layer.
- High-risk actions check `physiological_gate` before execution.

## Orchestrator Integration
1. Orchestrator fires synapse via `dispatch_task`.
2. Motor engine polls active lattice tasks every Pulse cycle.
3. Directives prefixed with `MOTOR:` are auto-executed.
4. Results are written back via `complete_task`.

## Approval Authority
| Area | Authority |
| :--- | :--- |
| **Command Allowlist** | Chief Systems Officer (CSO) |
| **Protected Path Overrides** | THE SOVEREIGN |

---

> [!CAUTION]
> Motor Agency does not bypass Law I. The Sovereign retains ultimate authority over constitutional DNA.

**Navigation:** [Global Dashboard](../foundation/aos_handbook.md) | [Lattice Protocol](./lattice_protocol.md)