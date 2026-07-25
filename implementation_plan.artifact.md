# [Goal Description]
Configure the Mojo SDK in Android Studio using WSL UNC paths and migrate core Python engine logic to Mojo 1.0 (2026 Beta) for peak hardware performance.

## User Review Required
> [!IMPORTANT]
> The Mojo SDK configuration uses **UNC paths** (`\\wsl.localhost\Ubuntu\...`) to bridge the Windows-WSL gap. This ensures Android Studio can index the standard library while the code executes in the high-performance Linux layer.
> [!WARNING]
> Python logic in Ring 1 (Metabolism, Synaptic Mesh) is being replaced by Mojo kernels. Python will remain for high-level "Skin" orchestration (Layer 0-1) but math-heavy "Muscle" (Ring 1) will be native Mojo.

## Proposed Changes

### Android Studio Configuration
Update project metadata to recognize the WSL Mojo SDK.

#### [MODIFY] [.idea/modules/sesha_agentic_body.iml](file:///C:/Users/gagan/Downloads/sesha_agentic_body/.idea/modules/sesha_agentic_body.iml)
- Point `Mojo SDK` to `\\wsl.localhost\Ubuntu\home\gaganjainse\mojo_core\.pixi\envs\default`.
- Point `Debugger` to `\\wsl.localhost\Ubuntu\home\gaganjainse\mojo_core\.pixi\envs\default\bin\mojo-lldb`.

#### [MODIFY] [.idea/misc.xml](file:///C:/Users/gagan/Downloads/sesha_agentic_body/.idea/misc.xml)
- Ensure project SDK is set to `Mojo SDK`.

---

### Core Kernels (Mojo 1.0)
Implement the "Muscle" layer using MLIR-native Mojo.

#### [MODIFY] [mcp_server/kernels/mojo/inference_engine.mojo](file:///C:/Users/gagan/Downloads/sesha_agentic_body/mcp_server/kernels/mojo/inference_engine.mojo)
- Finalize vectorized KL-divergence logic with 1.0 syntax.

#### [MODIFY] [mcp_server/kernels/mojo/photonic_vfe.mojo](file:///C:/Users/gagan/Downloads/sesha_agentic_body/mcp_server/kernels/mojo/photonic_vfe.mojo)
- Finalize SIMD energy complexity pulses.

#### [MODIFY] [mcp_server/kernels/mojo/metabolism_engine.mojo](file:///C:/Users/gagan/Downloads/sesha_agentic_body/mcp_server/kernels/mojo/metabolism_engine.mojo)
- Implement cellular respiration and ATP distribution logic.

#### [MODIFY] [mcp_server/kernels/mojo/synaptic_mesh.mojo](file:///C:/Users/gagan/Downloads/sesha_agentic_body/mcp_server/kernels/mojo/synaptic_mesh.mojo)
- Implement intent detection and signal firing.

## Verification Plan

### Automated Tests
- Run `mojo run <file>.mojo` for each kernel in WSL.
- Verify "SESHA_AI_KERNEL_HEARTBEAT" and VFE metrics.

### Manual Verification
- Check Android Studio bottom bar for "Mojo 1.0.0b2" status.
- Verify that "Mojo SDK" is no longer missing in Project Structure.