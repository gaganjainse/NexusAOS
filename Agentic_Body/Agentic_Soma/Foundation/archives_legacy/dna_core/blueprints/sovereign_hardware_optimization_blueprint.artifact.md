# Sovereign Hardware Optimization Blueprint: MSI Sword 16 HX (B14VEKG)
Version: 1.0.0
Description: Technical parameters and optimization strategies for the MSI Sword 16 HX substrate.

## 1. Substrate Specifications
- **CPU:** Intel Core i7-14700HX (8 P-cores, 12 E-cores | 28 Threads).
- **GPU:** NVIDIA GeForce RTX 4050 Laptop GPU (6GB GDDR6 | 105W TGP).
- **RAM:** DDR5-5600 MHz support.
- **Display:** 16-inch, 1600p, 165Hz.

## 2. Optimization Strategies (Physique Tier)
- **CPU Undervolting:** Utilizing offset voltage adjustments (if supported by BIOS/ThrottleStop) to reduce thermal throttling on the 14th Gen HX silicon.
- **Power Profiles:**
  - **Sovereign Mode:** PL1/PL2 limits maximized for short-burst reasoning tasks; GPU allocated priority for inference.
  - **Dharmic/Eco Mode:** Aggressive E-core utilization and PL1 capping for background processes and battery longevity.
- **GPU Calibration:** Curve optimization in MSI Afterburner to maintain stable clock speeds while minimizing voltage spikes during VRAM-intensive AI tasks.

## 3. Monitoring & Safety (L07 Integration)
- **Thermal Thresholds:**
  - CPU: < 95°C (Tjunction is 100°C).
  - GPU: < 85°C.
- **Telemetry Hooks:** Integration with HWInfo64 shared memory and **Direct-to-Kernel SOMA hooks** (see [SOMA_TELEMETRY_HARDWARE_LINKING](file:///C:/Users/gagan/Downloads/Sesha_corporate_os/archives/dna_core/blueprints/SOMA_TELEMETRY_HARDWARE_LINKING.artifact.md)) for real-time vitals and actuator control.

---
*Status: ARCHITECTED | Stability is the foundation of Power.*