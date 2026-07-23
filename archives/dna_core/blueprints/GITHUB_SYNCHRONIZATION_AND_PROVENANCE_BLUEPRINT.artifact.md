# Forge ID 48: GitHub Synchronization & Provenance (NEURAL 14.0)
Version: 14.0.0-PROVENANCE
Objective: Absolute sovereignty over the DNA Core history through cryptographic lineage and decentralized synchronization.

## 1. The Provenance Stack
To ensure the **Absolute Provenance** mentioned in the Kinetic Layer, the system must transition from simple file tracking to **Cryptographic Lineage**.

| Layer | Component | Function |
| :--- | :--- | :--- |
| **Commit** | Git-Hook (Pre-commit) | Automatic SHA-256 hashing and Metadata injection. |
| **Transport** | Zenoh P2P Mesh | Zero-copy decentralized git object propagation. |
| **Storage** | Radicle / IPFS | Censorship-resistant, decentralized history preservation. |
| **Mirror** | GitHub | Centralized shell for accessibility and "Pulse" verification. |

## 2. Git-Hook Logic-Atom Versioning
Every "Logic-Atom" (Blueprint or core script) must be self-verifying.

### A. The `pre-commit` Pulse
When a blueprint is modified, the local `pre-commit` hook executes:
1. **Hash Verification:** Calculates the SHA-256 of the logic-atom content.
2. **Metadata Injection:** Automatically updates the `Provenance-Header` in the markdown file:
   ```markdown
   ---
   Provenance-ID: <SHA-256>
   Parent-ID: <PREVIOUS_SHA>
   Forger: Nexus (NEURAL 14.0)
   Pulse-ID: 13
   Timestamp: 2026-07-23T21:49:53Z
   ---
   ```
3. **Intent Mapping:** Cross-references the commit message with the current **Sovereign Directive** from the `conversation_vault`.

### B. The `post-commit` Exhale
Triggers the background synchronization process:
- **Asynchronous Sync:** Leverages the `motor_engine.py` asynchronous sync to push to the local Zenoh mesh and GitHub mirror simultaneously.

## 3. Decentralized History Preservation
To prevent "Memory Holes" or centralized censorship, the DNA Core utilizes a tripartite storage strategy.

- **Zenoh Git-Mesh:** Using the **Agentic Soma's Zenoh Mesh**, git objects are broadcasted to all trusted local nodes (MSI Sword, Mobile Node, Cloud Edge). This ensures that even without internet, the history remains consistent across the "Body."
- **Radicle Seeds:** The project is published to a private Radicle network. Unlike GitHub, there is no central authority; the Sovereign's devices act as seed nodes.
- **IPFS Cold Storage:** Every "Pulse" (batch of logic atoms) is snapshotted and pinned to IPFS/Filecoin. The CID (Content Identifier) is recorded in the **Sovereign Progress Report**.

## 4. Integration with Total Recall
- Every `git commit` hash is linked to a specific `Cycle-ID` in the `archives/dna_core/learning/conversation_vault/`.
- This creates a **Complete Audit Trail**: `Sovereign Intent` -> `AI Thought` -> `Logic Change` -> `Cryptographic Commit`.

## 5. Implementation Protocol (Forge ID 48)
1. **Initialize `logic_git` Enhancement:** Update `logic_git.py` to handle `Provenance-Header` injection.
2. **Deploy Zenoh-Git Bridge:** Utilize `hive_bridge.py` to encapsulate git objects in Zenoh pulses.
3. **Establish Radicle Remote:** Add a `rad://` remote to the local repository for P2P synchronization.

---
*Status: FORGED | History is written in code. Sovereignty is immutable.*
