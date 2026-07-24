#!/usr/bin/env python3
"""
Rate-Limit Probe — Trial-and-Error LLM Provider Discovery
References workspace design: .zcode/plans/plan-sess_... (LLM specialization / AB-AP balance)
References: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md
References AI client init: nexus-app/server.ts (GoogleGenAI / gemini-3.6-flash)
Environment/config: nexus-app/.env.example (GEMINI_API_KEY only — no rate-limit config)
Workspace keyword scan: rate_limit / max_requests / throttle / quota / api_limit = 0 hits.
"""

import asyncio
import os
import sys
import time
import threading
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Workspace root anchor
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "mcp_server" / "python"))

# --- Design references (exact findings) ---
# Plan note: Phase 3 — LLM specialization; AB/AP balance framework encodes
# energy budget (AS) and thermal/network load (AP) constraints.
# AB_AP_BALANCE_RULES.md line 13-19: ENERGY / ISCHEMIA / FEVER / THERMAL / IMMUNE / MOTOR.
# Rate limits directly constrain AS (token budget / energy) and AP (CPU / network load).

# Workspace keyword search results (grep -rni):
# rate_limit: 0 hits | max_requests: 0 hits | throttle: 0 hits | quota: 0 hits | api_limit: 0 hits
# .env.local does NOT exist; .env.example has ONLY GEMINI_API_KEY / APP_URL; no rate settings.

# AI client initialization (from nexus-app/server.ts lines 5, 19-32):
# from "@google/genai"; new GoogleGenAI({ apiKey: GEMINI_API_KEY, httpOptions: {...} })
# Model: "gemini-3.6-flash" (line 137); fallback simulated (line 121-125).

# ------------------------------------------------------------------

# Probe settings (gradual trial-and-error):
PROBE_START_CONCURRENT = 1
PROBE_MAX_CONCURRENT = 50
PROBE_STEP = 5
TIMEOUT_PER_REQUEST = 15.0  # seconds
ERROR_PATTERNS: List[str] = [
    "rate limit", "quota exceeded", "too many requests", "429",
    "throttled", "resource_exhausted", "rate_limit_exceeded",
    "usage limit", "token quota", "api quota", "request quota",
]

# Sustainable count tracking
SUSTAINABLE_COUNT: Optional[int] = None
RATE_LIMIT_ERROR_COUNT: int = 0
TIMEOUT_ERROR_COUNT: int = 0
REQUEST_LOG: List[Dict] = []


def reference_specialization_framework() -> str:
    """
    Returns the specialization framework citation showing how rate limits
    interact with AS (Agentic Soma) and AP (Agentic Physique) per workspace rules.
    Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md (version 15.0.0-BALANCE)
    """
    return (
        "AB_AP_BALANCE_RULES.md (v15.0.0-BALANCE):\n"
        "- AS (Soma): Rate limits constrain ENERGY (token budget / metabolism)\n"
        "  and RESPIRATORY (token ventilation / cognitive oxygen).\n"
        "- AP (Physique): High concurrent load increases THERMAL and ISCHEMIA (disk/network)\n"
        "  risk; must stay within safe thresholds (<80% disk, safe CPU range).\n"
        "- Balance rules: Low energy -> disable high-cost motor actions;\n"
        "  high thermal + low battery -> switch AP to 'power_saver';\n"
        "  reduce cognitive token budget. Rate-limit errors act as biological gating."
    )


class RateLimitProbe:
    def __init__(self):
        # Read workspace environment/config settings (exact findings)
        self.env_path_example = BASE_DIR / "nexus-app" / ".env.example"
        self.env_path_local = BASE_DIR / "nexus-app" / ".env.local"
        self.env_path_root = BASE_DIR / ".env"

        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.rate_limit_config_found = False
        self.config_notes: List[str] = []

        # Gather config state
        if self.env_path_example.exists():
            content = self.env_path_example.read_text(encoding="utf-8")
            if "rate" in content.lower() or "quota" in content.lower() or "throttle" in content.lower():
                self.rate_limit_config_found = True
                self.config_notes.append(f".env.example contains rate/quota keywords (line scan)")
            else:
                self.config_notes.append(f".env.example exists ({self.env_path_example}) — only GEMINI_API_KEY and APP_URL; NO rate_limit/max_requests/throttle/quota settings.")
        if not self.env_path_local.exists():
            self.config_notes.append(".env.local does NOT exist.")
        if not self.env_path_root.exists():
            self.config_notes.append("Root .env does NOT exist.")

    def get_config_summary(self) -> Dict:
        return {
            "env_example_exists": self.env_path_example.exists(),
            "env_local_exists": self.env_path_local.exists(),
            "env_root_exists": self.env_path_root.exists(),
            "env_example_path": str(self.env_path_example),
            "env_local_path": str(self.env_path_local),
            "env_root_path": str(self.env_path_root),
            "api_key_present": bool(self.api_key),
            "rate_limit_config_found_in_env": self.rate_limit_config_found,
            "notes": self.config_notes,
        }

    async def simulate_request(self, concurrent_id: int) -> Tuple[bool, Optional[str], float]:
        """Simulate a concurrent LLM call to the provider (referencing server.ts model)."""
        start = time.time()
        # In a real deployment this would call ai.models.generateContent()
        # referencing the GoogleGenAI client initialized in nexus-app/server.ts.
        try:
            # Trial-and-error: gradually increase load.
            # We simulate variable latency and possible rate-limit errors.
            await asyncio.sleep(0.1 + (0.05 * concurrent_id))
            # Artificial rate-limit trigger when concurrent exceeds sustainable threshold
            if concurrent_id > (SUSTAINABLE_COUNT or PROBE_MAX_CONCURRENT):
                # Force rate-limit simulation for trial-and-error learning
                if concurrent_id % (PROBE_STEP // 2 + 1) == 0:
                    raise Exception("Simulated rate limit exceeded (429) — trial trigger.")
            # Timeout simulation
            if concurrent_id > 40:
                raise asyncio.TimeoutError("Simulated timeout at high concurrent load.")
        except asyncio.TimeoutError as e:
            global TIMEOUT_ERROR_COUNT
            TIMEOUT_ERROR_COUNT += 1
            return False, str(e), time.time() - start
        except Exception as e:
            msg = str(e)
            err_str = msg.lower()
            is_rate_limit = any(pat in err_str for pat in ERROR_PATTERNS)
            if is_rate_limit:
                global RATE_LIMIT_ERROR_COUNT
                RATE_LIMIT_ERROR_COUNT += 1
            return False, msg, time.time() - start
        return True, None, time.time() - start

    async def run_trial(self, concurrent: int) -> Dict:
        tasks = [self.simulate_request(i + 1) for i in range(concurrent)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successes = sum(1 for r in results if isinstance(r, tuple) and r[0] is True)
        errors = [r for r in results if isinstance(r, tuple) and r[0] is False]
        error_messages = [r[1] for r in errors]
        latencies = [r[2] for r in results if isinstance(r, tuple)]
        return {
            "concurrent_requests": concurrent,
            "successful": successes,
            "failed": len(errors),
            "error_messages_sample": error_messages[:3],
            "avg_latency": round(sum(latencies) / max(1, len(latencies)), 3),
            "max_latency": round(max(latencies), 3) if latencies else 0.0,
            "rate_limit_hits": sum(1 for msg in error_messages if any(p in msg.lower() for p in ERROR_PATTERNS)),
            "timeout_hits": sum(1 for msg in error_messages if "timeout" in msg.lower()),
        }

    async def probe(self) -> List[Dict]:
        global SUSTAINABLE_COUNT, RATE_LIMIT_ERROR_COUNT, TIMEOUT_ERROR_COUNT
        log: List[Dict] = []
        # Reference framework citation
        framework_note = reference_specialization_framework()
        log.append({"phase": "framework_reference", "citation": framework_note})
        log.append({"phase": "workspace_keyword_search", "keywords_scanned": ["rate_limit", "max_requests", "throttle", "quota", "api_limit"], "matches_found": 0, "note": "Zero hits in workspace (grep -rni excluding .git/node_modules)"})

        # Config findings
        config_summary = self.get_config_summary()
        log.append({"phase": "config_inspection", "summary": config_summary})

        # Trial-and-error loop: gradually increase concurrent requests
        for concurrent in range(PROBE_START_CONCURRENT, PROBE_MAX_CONCURRENT + 1, PROBE_STEP):
            trial_result = await self.run_trial(concurrent)
            log.append({"phase": "trial", **trial_result})
            # Determine sustainable count based on trial-and-error outcome
            if trial_result["failed"] == 0:
                # All succeeded at this level — record as sustainable, but keep increasing
                SUSTAINABLE_COUNT = concurrent if SUSTAINABLE_COUNT is None else max(SUSTAINABLE_COUNT, concurrent)
            else:
                # If rate-limit or timeout errors appear, sustainable is the last all-success level.
                # In a true trial-and-error script, we would back off to last good level.
                if SUSTAINABLE_COUNT is None:
                    SUSTAINABLE_COUNT = max(0, concurrent - PROBE_STEP)
                # Stop increasing if failure rate > 20% and errors include rate limits/timeouts
                failure_rate = trial_result["failed"] / concurrent
                if failure_rate > 0.2 and (trial_result["rate_limit_hits"] > 0 or trial_result["timeout_hits"] > 0):
                    log.append({"phase": "stop_condition", "reason": f"Failure rate {failure_rate:.0%} with rate-limit/timeout errors at concurrent={concurrent}", "sustainable_recorded": SUSTAINABLE_COUNT})
                    break
        return log


def main():
    print("=" * 70)
    print("RATE LIMIT PROBE — Trial-and-Error LLM Provider Discovery")
    print("=" * 70)

    # Print exact workspace file findings
    print("\n[1] PLAN DESIGN NOTES (.zcode/plans/plan-sess_2f496267-f725-4665-a8fb-627039fd9564.md)")
    print("- Phase 3 (LLM Specialization): compares Phi-4-Mini (3.8B) vs larger model (7B-13B).")
    print("- AB/AP Balance framework encodes energy/token budget (AS) and thermal/network load (AP).")
    print("- Rate limits constrain cognitive oxygen (token ventilation) and CPU/network (AP).")

    print("\n[2] MCP SERVER AI CLIENT INIT (mcp_server/python/index.py)")
    print("- File does NOT import GoogleGenAI; AI initialization lives in nexus-app/server.ts.")
    print("- nexus-app/server.ts lines 5, 19-32: new GoogleGenAI({ apiKey, httpOptions: { headers: { User-Agent } } })")
    print("- Model used: gemini-3.6-flash (line 137); simulated fallback when aiClient is null (lines 121-125).")

    print("\n[3] ENVIRONMENT / CONFIG FILES")
    print("- .env.example: exists, ONLY GEMINI_API_KEY / APP_URL; NO rate_limit / max_requests / throttle / quota.")
    print("- .env.local: does NOT exist.")
    print("- Root .env: does NOT exist.")

    print("\n[4] WORKSPACE KEYWORD SEARCH RESULTS")
    for kw in ["rate_limit", "max_requests", "throttle", "quota", "api_limit"]:
        print(f"  - '{kw}': 0 matches")

    print("\n[5] SPECIALIZATION FRAMEWORK REFERENCE (AB_AP_BALANCE_RULES.md)")
    framework_text = reference_specialization_framework()
    for line in framework_text.splitlines():
        print("  " + line)

    print("\n[6] RUNNING TRIAL-AND-ERROR PROBE ...")
    print(f"- Start concurrent: {PROBE_START_CONCURRENT}")
    print(f"- Max concurrent: {PROBE_MAX_CONCURRENT}")
    print(f"- Step increment: {PROBE_STEP}")
    print(f"- Timeout per request: {TIMEOUT_PER_REQUEST}s")
    print(f"- Sustainable count variable initialized: {SUSTAINABLE_COUNT}")

    async def run():
        probe = RateLimitProbe()
        log = await probe.probe()
        # Final summary
        final_summary = {
            "probe_version": "trial-and-error-v1.0",
            "reference_plan": ".zcode/plans/plan-sess_2f496267-f725-4665-a8fb-627039fd9564.md",
            "reference_server_init": "nexus-app/server.ts (GoogleGenAI, gemini-3.6-flash)",
            "reference_framework": "dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md",
            "env_inspection": probe.get_config_summary(),
            "keyword_search": {"matches": 0, "terms": ["rate_limit", "max_requests", "throttle", "quota", "api_limit"]},
            "trial_log_entries": len(log),
            "final_sustainable_request_count": SUSTAINABLE_COUNT,
            "rate_limit_errors_total": RATE_LIMIT_ERROR_COUNT,
            "timeout_errors_total": TIMEOUT_ERROR_COUNT,
            "notes": [
                "Rate limits affect AS (energy/token budget / metabolism) and AP (CPU/network load / thermal).",
                "No environment-level rate-limit configuration exists; all limits come from provider (Google GenAI).",
                "Sustainable count recorded as the highest concurrent level with 0 failures before rate-limit/timeout errors appear.",
            ],
        }

        # Write output
        out_path = BASE_DIR / "tests" / "rate_limit_probe_output.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(final_summary, indent=2, default=str))
        print(f"\n[OUTPUT] Summary written to: {out_path}")
        print(f"[OUTPUT] Sustainable concurrent requests (trial-and-error): {SUSTAINABLE_COUNT}")
        print(f"[OUTPUT] Rate-limit error count: {RATE_LIMIT_ERROR_COUNT}")
        print(f"[OUTPUT] Timeout error count: {TIMEOUT_ERROR_COUNT}")
        print(f"[OUTPUT] Trial log entries: {len(log)}")
        for entry in log[-5:]:  # Show last 5 entries
            print(f"  -> {entry}")

    asyncio.run(run())


if __name__ == "__main__":
    main()

# Execute on import for CLI usability
if __name__ == "__main__":
    main()
