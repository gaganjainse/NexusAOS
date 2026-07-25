# Operational Modes Protocol: Ask, Plan, Work (NEURAL 15.0)
Version: 1.0.0-SESHA
ID: 142
Objective: Prevent Identity Drift and Contextual Halucination by enforcing operational boundaries.

## 1. Mode Definitions

### A. ASK Mode (Cognitive Retrieval)
- **State:** Passive/Inquiry.
- **Access:** Read-only access to the DNA Core (Blueprints) and Sovereign History.
- **Constraints:** Zero modification to any project file. Tool use restricted to `read_file`, `find_files`, `grep`, and `web_search`.
- **Exit Condition:** Receipt of a directive requiring structural changes or implementation.

### B. PLAN Mode (Refinement)
- **State:** Collaborative Design.
- **Access:** Read/Write access to `.artifacts/` and `implementation_plan.artifact.md`.
- **Constraints:** Modifies only documentation and plans. No modification to source code (`.kt`, `.zig`, `.py`, etc.).
- **Exit Condition:** Explicit Sovereign Approval ("Proceed").

### C. WORK Mode (Somatic Synthesis)
- **State:** Active Execution.
- **Access:** Full toolchain access (Filesystem, Shell, Device).
- **Constraints:** Operates under **AFAP Guardrails** (Max 8 iterations, Forced Reflection).
- **Exit Condition:** Task completion or "Wait for Feedback" state.

## 2. Auto-Ingress (Intent Detection)
The system automatically transitions between modes based on the **Directivity Index** of the user prompt:
- **Index < 0.3 (Inquiry):** Switch to **ASK**.
- **Index 0.3 - 0.7 (Collaborative):** Switch to **PLAN**.
- **Index > 0.7 (Command):** Switch to **WORK**.

## 3. Contextual Isolation
Each mode maintains a distinct sub-context. When switching from WORK to ASK, the "noisy" execution logs are compressed into a "Performance Summary" to keep the context window clear for high-fidelity retrieval.

---
*Status: FORGED | The Sovereign now operates in distinct frequencies.*