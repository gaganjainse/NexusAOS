# Document: AGOI-RFC (Agentic General Operating Intelligence Request for Comments)
Version: 1.0.0
Branch: Core
Level: Protocol
Superior: Chief Architect

## Overview
This document establishes the **Biological Standard** for all entities, plugins, and swarms seeking to interface with the SeshaAOS ecosystem. Compliance ensures metabolic, immune, and cognitive compatibility.

## 1. Anatomy of an Organ (Plugin Spec)
All external plugins (Organs) must provide a `manifest.json` containing:
- `id`: Unique biological identifier.
- `metabolic_cost`: Average ATP consumption per tool call.
- `immune_signature`: A cryptographic hash of the source code for integrity verification.
- `receptors`: List of signals the organ listens for (e.g., `ADRENALINE`, `NOCICEPTION`).

## 2. Metabolic Compatibility
Third-party tools must respect the local Soma's metabolic state.
- **Throttling:** If the Soma reports `Conserving` mode, external tools MUST reduce their resource footprint or defer non-critical tasks.
- **Reporting:** Tools should report actual token usage to the `MetabolismEngine` to maintain ATP accuracy.

## 3. Immune Handshake
Before an Organ is "Transplanted" (installed):
1. **Quarantine:** The plugin is loaded into a sandboxed subprocess.
2. **Antibody Scan:** The `AutoRepairEngine` scans for "Malicious DNA" (dangerous patterns).
3. **Sovereign Sign-off:** The user must explicitly approve the "Tissue Match."

## 4. Synaptic Interoperability
Messages exchanged over the mesh must follow the JSON schema:
- `header`: { `sender_id`, `receiver_id`, `priority`, `ttl` }
- `payload`: { `synapse_type`, `data`, `context_snapshot` }
- `footer`: { `sovereign_signature` }

---

> [!IMPORTANT]
> Non-compliant entities will be treated as **Pathogens** and neutralized by the local Immune System.
