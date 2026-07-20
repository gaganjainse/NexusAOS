# NexusOS: The Liver & Filtration (AGOI Phase 10)

This plan implements the **Filtration System** (The Liver), preventing organizational bloat and data toxicity. It moves the OS from "Cumulative Growth" to **"Metabolic Balance,"** solving the "Waste & Excretion" gap identified in the audit.

## Proposed Changes

### 1. DNA: Filtration Protocol
Define the rules for identifying and "excreting" system waste.

#### [NEW] [filtration_protocol.md](file:///C:/Users/gagan/Downloads/nexus_corporate_os/archives/core/protocols/filtration_protocol.md)
- Define **"Toxins"**: Redundant debug logs, stale consolidation reports (>30 days), and orphan logic nodes.
- Define **"The Excretion Cycle"**: Moving non-critical data to the `archives/excreta/` folder (The Bladder) before permanent deletion.
- Define **"Data Longevity"**: Retention periods for different classes of system artifacts.

### 2. Autonomic Layer: The Nexus Liver
Implement the Python logic for system-wide data filtration.

#### [NEW] [nexus_liver.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/tools/nexus_liver.py)
- A tool to scan the OS filesystem for "Toxic" buildup.
- **Log Rotation:** Automatically truncates `.log` files exceeding 5MB.
- **Archive Pruning:** Moves old `consolidation_*.md` files to an `archives/vault/` (compressed) or deletes them if deemed low-value by the Memory Synth.
- **History Compaction:** Truncates `lattice_state.json` and `mutation_history.json` based on the system's "Salience" (Keeping only what matters for current Vibe).

### 3. Circulatory Integration: Filtration Pulse
Connect waste management to the Heartbeat.

#### [MODIFY] [nexus_pulse.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/nexus_pulse.py)
- Add a **"Filtration Cycle"** (every 100 cycles).
- Trigger `nexus_liver.py` to "clean the blood" (data streams).

### 4. Proprioception: Toxic Load Monitoring
Update diagnostics to reflect system "Cleanliness."

#### [MODIFY] [system_diagnostics.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/tools/system_diagnostics.py)
- Add a "Toxicity" section.
- Report on **"Toxic Load"** (Total log size / unnecessary file count).

### 5. Integration: MCP & Dashboard
Visualize the system's "Liver Function."

#### [MODIFY] [index.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/index.py)
- Add `@mcp.tool() trigger_system_filtration()`.
- Add `@mcp.tool() get_toxicity_report()`.

#### [MODIFY] [nexus_gui.py](file:///C:/Users/gagan/Downloads/nexus_corporate_os/mcp_server/python/nexus_gui.py)
- Add a "Toxicity Meter" to the Health tab.
- Add a visual "Cleanse" button to manually trigger the Liver.

## Verification Plan

### Automated Tests
- Create 10 dummy log files and verify that `nexus_liver.py` identifies and prunes them.
- Verify that the total disk footprint of the `archives/` directory decreases after a filtration cycle.

### Manual Verification
- View the Toxicity Meter in the GUI and verify it drops after a "Cleanse" event.
