# Document: Provenance Module
Version 2.0 — Implements the Sovereign Interaction Rule.
Every interaction is saved, committed to git, and truthfully reported.
No false claims per Law III.

## Protocol:
- Save: Append cycle to interaction_history.md
- Stage: git add
- Commit: git commit with truthful message
- Push: git push (reported truthfully, not claimed falsely)
- Report: Every step's success/failure is returned honestly
