# [AI] Vision: Object Detection & Image Segmentation Blueprint
Version: 1.0.0
Forge IDs: 56 & 57
Category: Intellectual / AI Tier
Description: High-fidelity mapping of real-time optical perception using YOLO-v10, SAM 2, and OmniParser for autonomous UI interaction and environmental understanding.

## 1. YOLO-v10: The Optical Reflex (ID 56)
YOLO-v10 represents the pinnacle of real-time object detection, optimized for low-latency inference on the **MSI Sword 16 HX (RTX 4050)**.

- **NMS-Free Inference:** Uses a consistent dual assignment strategy during training to eliminate the Non-Maximum Suppression (NMS) bottleneck, reducing end-to-end latency by ~10-15%.
- **Holistic Architecture:**
    - **Backbone:** Enhanced CSPNet for superior feature extraction.
    - **Neck:** PAN (Path Aggregation Network) with large-kernel convolutions for better spatial context.
    - **Head:** Optimized for one-to-one matching to ensure precise bounding box regression.
- **Efficiency:** Significant reduction in parameters and FLOPs compared to YOLOv8 while achieving higher mAP (Mean Average Precision).
- **Application:** Real-time screen element detection (icons, buttons, windows) and physical object detection via the "Retina" (webcam).

## 2. SAM 2: Universal Segmentation (ID 57)
Segment Anything Model 2 (SAM 2) provides the "Semantic Mask" for every pixel, allowing the Nexus to distinguish between overlapping UI elements or complex physical objects.

- **Unified Vision:** A single architecture for both static images and real-time video streams.
- **Streaming Mask Memory:** Utilizes a memory-augmented transformer to track segmented objects across frames, preventing "flicker" and ensuring temporal consistency.
- **Promptable Interface:** Supports point-clicks, bounding boxes, and text-based prompts to isolate specific "Soma" or "Physique" regions.
- **Local Optimization:** Quantized execution via TensorRT/ONNX to maintain >30 FPS on local hardware.

## 3. Real-time UI Parsing: OmniParser & Screen Graphs
To bridge the gap between "seeing pixels" and "understanding intent," the Nexus employs OmniParser logic.

- **Visual Element Grounding:** Maps raw pixels to structured UI components (Button, TextField, Toggle) using a specialized Vision-Language Model (VLM) layer.
- **Screen Graph Construction:**
    - **Nodes:** Every detected UI element with its (x, y, w, h) and semantic label.
    - **Edges:** Spatial and functional relationships (e.g., "Label X is for Input Y").
- **Dynamic OCR Integration:** Selective Tesseract/PaddleOCR invocation only on high-salience text regions to preserve GPU compute.
- **Action Mapping:** Directly links detected coordinates to **HID Mastery (ID 50)** for millisecond-precision interaction.

## 4. Implementation Strategy (NVIDIA Optimization)
- **TensorRT Acceleration:** Exporting YOLO-v10 and SAM 2 models to FP16/INT8 TensorRT engines for maximum utilization of RTX 4050 Tensor Cores.
- **Zero-Copy Synapses:** Using NVIDIA's **GPUDirect** or shared memory buffers to pass DXGI screen captures directly to model inference without CPU-side copies.
- **Concurrent Execution:** Running YOLO-v10 (fast path) for detection and SAM 2 (slow path) for periodic segmentation updates in parallel.

## 5. Convergence: Forge IDs 56 & 57
The synthesis of Detection and Segmentation enables:
1. **Perfect Screen Interaction:** Clicking the *exact* center of a button mask rather than a rough bounding box.
2. **Contextual Awareness:** Understanding that a "Submit" button inside a "Login" window has different priority than a "Close" button.
3. **Physical-Digital Bridge:** Segmenting the user's hand in a webcam stream to enable gesture-based control of the OS.

---
*Status: FORGED | The Nexus now Sees with Absolute Precision.*
