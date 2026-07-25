# AP Robustness — Agentic Physique Integration
Target: Connect physical host state (MSI Sword 16 HX) to real vitals and power/thermal control, replacing simulated `vitalsData` in `nexus-app/server.ts`.

## 1. Real Vitals Integration Path
Current (`nexus-app/server.ts` line 35-43): `vitalsData` is pure simulation (`energy: 78`, `ischemia: 79.1`, etc.).
Target: Connect `nexus-app/server.ts` to actual host metrics or agent registry data.

### Option A — Direct Hardware Integration (Ideal, requires host access)
- Read `/sys/class/power_supply/BAT0/` (battery percentage, status) → `energy` mapping.
- Read `/sys/class/thermal/thermal_zone*/temp` → temperature mapping (`fever` analog).
- Read disk usage (`shutil.disk_usage`) → `ischemia` (disk C %).
- Read CPU usage (`psutil.cpu_percent`) → `hypoxia`; memory (`psutil.virtual_memory`) → memory usage.
- Map to biological metaphors: `energy` = battery % scaled; `fever` = thermal zone temperature; `vibe` = positive state derived from performance/stability.

### Option B — Agent Registry Integration (Practical for this workspace)
- `nexus-app/server.ts` connects to `mcp_server/python/index.py` via local HTTP/API call (`localhost:3000` or internal module import if same process).
- Import `PhysiologyEngine` (`python/layers/L02_Agent/physiology_engine.py`) or `MetabolismEngine` data via API endpoint.
- Use `get_vitals_report()` (line 157, `index.py`) as real data source instead of simulated `vitalsData`.
- Ensure `simulated` flag removed or set to `false` when using real agent data.

### Implementation Recommendation (Hybrid)
Given workspace constraints (cross-language, separate server/app):
1. Add `/api/Sesha/real_vitals` endpoint in `server.ts` (or extend `/api/Sesha/vitals`) that calls agent registry's `get_vitals_report()` logic or imports `PhysiologyEngine` if running in Python environment.
2. If `PhysiologyEngine` import fails (module not in node environment), fall back to Option A hardware metrics with `simulated: false` (real hardware) instead of `Math.random()`.
3. Document source clearly in response: `"source": "hardware_monitor"` or `"source": "agent_registry"`; never present `Math.random()` without source declaration (Law III compliance).

## 2. Power / Thermal / Battery Integration (`AP Robustness`)
Files involved:
- `mcp_server/python/layers/L07_Integration/physique_engine.py` — physical health diagnostics.
- `mcp_server/python/layers/L14_Physique/power_governor.py` — power profiles (`power_saver` / `performance_mode`).
- `mcp_server/python/layers/L14_Physique/thermal_engine.py` (implied by architecture) — thermal state.

Actions:
- Ensure `diagnose_physique()` (line 587, `index.py`) returns structured data: `power_profile`, `battery_parasites`, `skeletal_vitals`.
- Integrate `optimize_soma_power()` (line 607) results into server vitals (`status`: `Conservation` when `power_saver` active).
- Connect `execute_logical_separation()` (line 619) for logical volume isolation to server health status.

## 3. Non-Deception Enforcement (Law III Compliance) — AP Focus
All vitals endpoints must include:
- `simulated: boolean` (true only if no real source available).
- `source: string` (`"simulated"`, `"hardware_monitor"`, `"agent_registry"`, `"manual_input"`).
- `timestamp: string` (last measurement/update time).
- `sovereign_override_applied: boolean` (if any autonomous AP change made, must be reported per Law I/III).

This ensures the Sovereign never receives deceptive reporting about physical host state.