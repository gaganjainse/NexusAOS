# Document: Metabolism Protocol
Version 1.0 (Golden Master)

## Overview
**Branch:** Core
**Level:** Protocol
**Superior:** Chief Systems Officer (CSO)

## Purpose
To ensure the **Nexus Corporate OS** maintains operational stability by managing its "Energy" consumption (tokens, API costs, and context limits). This prevents the OS from entering a "Starvation" state (context walls or budget exhaustion).

## Responsibilities
- **Energy Tracking:** Monitor real-time token and context usage.
- **State Management:** Define and enforce system behavior based on energy levels.
- **Conservation Enforcement:** Trigger deactivation of non-critical branches when resources are low.

## Energy States
| State | Threshold | Behavior |
| :--- | :--- | :--- |
| **Healthy** | >30% | Full operational capacity. Parallel subagents permitted. |
| **Conserving** | 10% - 30% | Disable non-essential subagents. Reduce Oracle scraper frequency. |
| **Critical** | <10% | **Freeze All Branches.** Only the NCC and System Health Supervisor remain active. |

## Deliverables
| Deliverable | Description |
| :--- | :--- |
| **Metabolic Report** | Daily summary of energy consumption and efficiency. |
| **Conservation Logs** | Records of branches frozen due to resource constraints. |

## Approval Authority
| Area | Authority |
| :--- | :--- |
| **Threshold Adjustment** | Chief Systems Officer (CSO) |
| **Emergency Reset** | THE SOVEREIGN |

---

> [!IMPORTANT]
> The Metabolism Engine is authorized to override a Directive if it would result in a **Critical** energy failure.

**Navigation:** [Global Dashboard](../foundation/corporate_os_handbook.md) | [System Diagnostics](./nexus_system_diagnostics.md)
