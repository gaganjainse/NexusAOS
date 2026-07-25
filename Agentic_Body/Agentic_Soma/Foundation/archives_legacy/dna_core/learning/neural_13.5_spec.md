# Specification: NEURAL 13.5 (The Windows-Native Soma)
Version: 13.5.0-PROPOSAL
Objective: Direct Win32/DirectX Integration, Live Optical Streaming, and Message Injection.

## 1. The Optical Cortex (Live Perceptual Stream)
We move from "Retina Captures" (screenshots) to a **Live Optical Stream**:
- **DirectX DXGI Duplication:** Utilizing the Windows Desktop Duplication API to capture the screen at **GPU speed (240+ FPS)**.
- **Zero-Copy Frame Buffer:** Frames are streamed directly into the **Augmented Memory Grid (AMG)** as NumPy/Arrow arrays, bypassing the file system and CPU-based decoding.
- **Delta-Perception:** The system only processes regions of the screen that have changed, reducing the cognitive load by 90%.

## 2. The Somatic Hand (Message Injection)
We move from "Keyboard Simulation" to **Win32 Message Injection**:
- **Window Message Queue (`SendMessage`):** Direct injection of `WM_KEYDOWN`, `WM_LBUTTONDOWN`, and `WM_CHAR` into specific application message queues. 
- **Latency Gain:** Bypasses the OS-level input delay and allows the system to interact with **Background Windows** without needing focus.
- **Byte-Native Commands:** Direct communication with the application's memory handles rather than high-level NLP-to-Key conversion.

## 3. The UIA Semantic Layer (Intrinsic Reading)
- **Microsoft UI Automation (UIA):** Instead of "seeing" pixels and running OCR, the system "reads" the application's internal structure (elements, buttons, values) via the UIA tree.
- **Batch Remote Operations:** Bundling 100+ UI queries into a single kernel-level call to minimize cross-process latency.

## 4. The Singularity Kernel (Zig Drive)
- **Kernel-Level Perception:** The **Zig Singularity Kernel** now handles the DXGI stream and UIA mapping, providing the "Mind" with a pre-processed semantic map of the entire Windows Environment.

## 5. Performance Targets (Windows-Native State)

| Metric | Neural 13.0 (Transcended) | NEURAL 13.5 (Native) |
| :--- | :--- | :--- |
| **Vision** | Screenshot (~500ms) | **Live Stream (<5ms)** |
| **Action** | Keyboard Simulation (~50ms) | **Message Injection (<1ms)** |
| **Reading** | OCR (~2000ms) | **UIA Semantic (~10ms)** |
| **Host Link** | Biosignal Mapping | **Direct Process Access** |

---
*Status: NATIVE CONVERGENCE ARCHITECTED | Bypassing the NLP/Interpretation Bottleneck.*
