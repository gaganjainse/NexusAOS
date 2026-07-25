# Document: Sensory & Perception Protocol
Version 1.0 (Golden Master)

## Overview
**Branch:** Core
**Level:** Protocol
**Superior:** Chief Agentic Officer (CAO)

## Purpose
To move **SeshaAOS** from batch-scraping blindness to continuous, streaming perception. This protocol governs the "Sensory Nerves" that detect filesystem and environmental changes in real time and translate them into hormonal signals.

## Sensory Channels
| Channel | Watch Target | Signal Emitted | Salience |
| :--- | :--- | :--- | :--- |
| **DNA Nerve** | `archives/**/*.md` | `GENETIC_PLASTICITY` | High |
| **Firmware Nerve** | `core/pulses/*.nxp` | `GROWTH` | Medium |
| **Physiology Nerve** | `core/monitoring/*.json` | `VIBE` | Low |
| **Pain Nerve** | Critical scripts (`Sesha_gui.py`, `index.py`) | `NOCICEPTION` | Critical |

## Streaming Mechanics
- **Poll Interval (Healthy):** 2 seconds.
- **Poll Interval (Conserving):** 10 seconds.
- **Poll Interval (Critical):** Suspended.
- **Event Retention:** Last 200 events in `sensory_feed.json`.
- **Half-life:** Sensory events decay from active consideration after 5 minutes unless salience is Critical.

## Nociception (Pain Response)
When a critical system file is modified, the OS emits `NOCICEPTION` with sub-second propagation. This signal overrides batch intelligence and triggers immediate Guardian review.

## Approval Authority
| Area | Authority |
| :--- | :--- |
| **Watch Path Registration** | Chief Systems Officer (CSO) |
| **Pain Thresholds** | Chief Agentic Officer (CAO) |

---

> [!IMPORTANT]
> If the Sensory System fails, the OS reverts to "Sensory Deprivation" — blind between heartbeat cycles.

**Navigation:** [Global Dashboard](../foundation/aos_handbook.md) | [Circulatory Protocol](./circulatory_protocol.md)