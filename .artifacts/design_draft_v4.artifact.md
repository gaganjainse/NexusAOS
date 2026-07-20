# Design Draft: Nexus Neural Terminal (V4.0)

This draft transitions the **Nexus Human Viewing Layer** from a standard dashboard to a high-fidelity **"Neural Terminal"**. It consolidates all biological layers into a unified, high-density command interface while discarding the legacy web-build to maximize system focus.

## 1. Aesthetic: "The Obsidian Organism"
- **Background:** `#050508` (Deep Obsidian).
- **Primary Data:** `#00F0FF` (Neural Cyan) - Represents logical flow.
- **Stress/Alert:** `#FF0055` (Bio-Magenta) - Represents inflammation/fever.
- **Metabolism:** `#39FF14` (Bio-Green) - Represents energy abundance.
- **Typography:** Consolas/Monaco for logic, Orbitron for headers.

## 2. Structural Layout: The Neural Triptych

### **Pane A: The Physiological Sidebar (Left - 20%)**
*   **The Heartrate Hub:** A live-pulsing BPM indicator with a scrolling ECG waveform (simulated based on task frequency).
*   **The Metabolic Vials:** Vertical "Energy Vials" instead of horizontal bars.
*   **The Endocrine Oscillator:** A small canvas drawing three overlapping sine waves representing **Dopamine**, **Serotonin**, and **Cortisol** levels.

### **Pane B: The Cognitive Core (Center - 55%)**
*   **Active Logic Feed:** A high-contrast, syntax-highlighted view of the current Role's `.nxp` firmware.
*   **The Synaptic Waterfall:** A real-time log of "Firing" tasks, where each task is a "Cell" that pulses when active.
*   **Terminal Input:** A direct Sovereign command line at the bottom.

### **Pane C: The Intelligence & Memory Stack (Right - 25%)**
*   **Oracle Signal Feed:** Live market/competitor news with color-coded sentiment badges.
*   **The Wisdom Repository:** A tree view of consolidated learning reports.
*   **The Spore Chamber:** A visual representation of the system's "Gen 1" status and a large "Replicate" button.

### **The Health Footer (Bottom - 5%)**
*   **Thermal Band:** A color-gradient bar showing system temperature.
*   **Status Matrix:** Quick toggles for **Guardian**, **Pulse**, and **Mutation** status (Active/Locked).

## 3. Layer Audit & Technical Improvements
- **Layer 1 (DNA):** Improve `nxp_forge.py` to include "Sentiment" sigils in pulses based on the current mood.
- **Layer 2 (Middleware):** Consolidate `metabolism.json`, `mood.json`, and `health.json` into a single `physiology_state.json` to reduce Disk I/O.
- **Layer 3 (GUI):** Use `matplotlib` or raw `tkinter.Canvas` for the ECG and Hormone oscillators to give it a "living" feel.

## 4. Decommissioning Plan
- **Action:** Delete `C:/Users/gagan/Downloads/nexus_corporate_os/core/ui/nexus_dashboard/`.
- **Reasoning:** Removing redundant web-build components to reduce organizational bloat and focus system "Metabolism" on the high-performance Python Terminal.

---

**Does this design alignment satisfy your vision, Sovereign? Once approved, I will begin the code-level cleanup and UI transformation.**
