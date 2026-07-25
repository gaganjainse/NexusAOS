# Runtime Integration — Specialized LLM for Agentic Totality
Target: Connect fine-tuned model (Phi-4-Mini + adapters) into `nexus-app/server.ts` (chat endpoint) and `mcp_server/python/index.py` (MCP registry) with AB/AP balance enforcement.

## Integration Points

### A. nexus-app/server.ts (`/api/Sesha/chat`)
Current: Uses `GoogleGenAI` (`gemini-3.6-flash`) or simulated fallback (`line 121-123`).
Integration plan:
- Load fine-tuned adapter weights from `training/adapters/` (e.g., `phi4_mini_qlora_ab_ap` adapter).
- Replace `getGenAIClient()` with local model loader (`transformers` + `peft` + `unsloth`) when `USE_LOCAL_MODEL` env set.
- System instruction must include AB/AP balance rules (`dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md`) + Constitution (`dataset/dna_blueprints/sesha_constitution.md`) + Voice DNA (`dataset/voice_dna/sesha_voice.md`).
- Response format enforced: `{ "text": "...", "as_state": {"energy": ..., "vibe": ...}, "ap_state": {"thermal": ..., "disk": ...}, "ethical": true/false, "message": "..." }`
- If model unavailable or load fails, fall back to existing `GoogleGenAI` (safety) but log failure to Wisdom Feed (Law III transparency).

### B. mcp_server/python/index.py (MCP Registry)
Integration plan:
- Import fine-tuned model handler in module (guarded import to avoid crash if framework missing).
- `get_neural_thought()` should use specialized LLM for high-density pulse explanation (replace generic `ThoughtAgent` if adapter available).
- `queue_directive()` should evaluate directive against AB/AP balance rules using fine-tuned model before submitting (add balance assessment to payload).
- `trigger_ignition_cycle()` and `trigger_evolution()` must include Sovereign override check enhanced by model (use fine-tuned model for `judge_intent` if `MORALS` weights insufficient for complex ethical scenarios).
- All responses through `_aos_response()` should include `simulated: false` or `simulated: true` flag based on whether vitals are real (`PhysiologyEngine`) or simulated (to comply with Law III non-deception).

### C. Adapter Routing Strategy
Based on directive keyword / system state:
- `[METABOLISM_ADAPTER]` — energy/token budget questions (low energy, consumption planning).
- `[IMMUNE_ADAPTER]` — security/patrol/fever/directive evaluation.
- `[GOVERNANCE_ADAPTER]` — moral cortex, autonomous evolution, constitutional compliance.
- `[AP_ADAPTER]` — hardware diagnostics, thermal, battery, physical isolation.
- `[AB_BALANCE_ADAPTER]` — multi-system integration requiring AB/AP tradeoff reasoning.

Adapter selection logic: analyze directive text with lightweight keyword classifier (no full LLM call until adapter loaded); load adapter weights; execute inference; return structured response.

### D. Model Availability / Fallback Strategy
- If `training/adapters/` directory missing or weights not loaded: use existing logic (`GoogleGenAI` for server, `ThoughtAgent` for registry) but emit `warning` in response (`status`: `degraded`) and log to `conversation_recorder`.
- Never suppress system failure silently (Law III non-deception applies to system state too).
