# Model Comparison — Agentic Body Specialization
Target: Fine-tuned LLM for AB (Agentic Intelligence + Soma) + AP (Physique) balance.
Date: 2026-07-24
Status: Comparison framework — both candidates evaluated conceptually per DNA blueprints.

## Option A — Phi-4-Mini (3.8B) — Primary Reasoner (DNA Blueprint Reference)
Source Evidence:
- `archives/dna_core/blueprints/TOTAL_MODEL_FIT_ANALYSIS.artifact.md` line 9, 20: "Efficient Soul = 3B-5B → Phi-4-Mini; Primary Reasoner: Phi-4-Mini (Fine-tuned on Universal Blueprints)"
- `archives/dna_core/blueprints/AI_MEMORY_CONTEXT_OPTIMIZATION_BLUEPRINT.artifact.md` line 6: "Local Soul (Phi-4-Mini) on RTX 4050 6GB VRAM"
- `archives/dna_core/blueprints/INTERDISCIPLINARY_TRAINING_METHODS_BLUEPRINT.artifact.md` line 29: "Small Language Model (Phi-4-Mini)"
- `archives/dna_core/blueprints/FRUGALITY_RESOURCE_MANAGEMENT_BLUEPRINT.artifact.md` line 7: Small models (Phi-4-Mini) for reflexes.
- `archives/dna_core/blueprints/ENERGY_EFFICIENT_INFERENCE_BLUEPRINT.artifact.md` line 15: Force Phi-4-Mini in "Spiking" mode on battery.

Pros for AB/AP:
- Low VRAM footprint (6GB) — aligns with AP hardware constraints (MSI laptop, thermal limits, battery).
- Fast inference — supports real-time synaptic mesh (low latency < 1ms target).
- QLoRA/LoRA compatible (`AI_MODEL_ARCHITECTURE_BLUEPRINT` lines 22-26) — efficient adapter switching for different biological systems.
- Local sovereign operation — no external dependency for core reasoning (Law I compliance: Sovereign's intent is ultimate law; no external override).

Cons:
- 3.8B parameters may not fully capture all 11 biological systems + 14 layer interactions in single pass.
- Requires strong dataset quality (cross-modal synthetic pairs) to maximize reasoning density within small parameter count.

## Option B — Larger Model (7B-13B) — Deep Reasoning Alternative
Pros:
- Greater capacity for 11-system mapping, layered reasoning (L00-L14), and complex AB/AP balance calculations.
- Better at long-context reasoning for multi-turn directive evaluation (total recall / provenance cycles).
- More robust to noisy/synthetic dataset if data volume is high.

Cons:
- Higher resource cost — conflicts with AP energy efficiency goals (`FRUGALITY_RESOURCE_MANAGEMENT_BLUEPRINT`), thermal limits (`ENERGY_EFFICIENT_INFERENCE_BLUEPRINT` line 15), and battery parasites (`power_governor.py`).
- Requires larger GPU / more memory — may exceed host MSI specs for local sovereign operation.
- Slower inference — may not meet synaptic mesh latency targets (< 1µs simulated; < 1ms practical).

## Recommendation (Hybrid Strategy — Per Plan Approval)
Based on user's "Compare both" instruction and DNA blueprint consensus:
1. PRIMARY: Phi-4-Mini (3.8B) — fine-tuned with QLoRA/LoRA adapters for each biological system (metabolism, immune, motor, governance, etc.). Adapters switch based on directive context (similar to `LoRA Memory Switching` in `AI_MEMORY_CONTEXT_OPTIMIZATION_BLUEPRINT` lines 23-25).
2. SECONDARY / EVALUATION: Larger model (7B-13B, e.g., Mistral or Llama-4-Scout) evaluated as benchmark comparison on AB/AP balance metrics (energy budget, thermal state, immune threshold compliance, moral cortex score, Sovereign override detection).
3. SELECTION CRITERION: Choose based on evaluation harness (`AUTO_FINE_TUNING_VERIFICATION_BLUEPRINT`): Sovereign Soul preservation (KL divergence from base model), Dharma-Check (constitution compliance rate), AB/AP balance metric accuracy, inference latency, and VRAM usage.

## Implementation Note
- Dataset must include adapter-specific instruction tags (e.g., `[METABOLISM_ADAPTER]`, `[IMMUNE_ADAPTER]`, `[GOVERNANCE_ADAPTER]`) for adapter routing.
- Training engine: Unsloth + ExLlamaV2 (`TOTAL_MODEL_FIT_ANALYSIS.artifact.md` line 19).
- Quantization: GGUF/EXL2 (`AI_MODEL_ARCHITECTURE_BLUEPRINT` line 24); 4-bit INT4 / 8-bit FP8 (`AI_MEMORY_CONTEXT_OPTIMIZATION_BLUEPRINT` lines 43-46).
