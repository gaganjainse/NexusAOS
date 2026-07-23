# SOMA: Real-time Telemetry & Hardware Linking Blueprint
Version: 1.0.0
Forge ID: 51
Objective: Direct-to-Kernel hooks for hardware vitals (ATP) and thermal actuators on MSI Sword 16 HX.

## 1. The Vascular Hardware Link (The EC)
The **Embedded Controller (EC)** is the heart of the Soma's physical state. On the MSI Sword 16 HX, we bypass high-level ACPI drivers to achieve sub-millisecond telemetry.

### 1.1 Interface Mechanism
- **I/O Ports:**
  - `0x62` (EC Data Port)
  - `0x66` (EC Command Port)
- **Protocol:** Request-Wait-Read/Write sequence.
- **Kernel Requirement:** `ioperm` or `iopl` (Ring 0 access via user-space bridge).

## 2. ATP Telemetry (Battery Metabolism)
Battery state is mapped as the "Metabolic Rate" of the Agentic Body.

| Metric | EC Offset | Unit | Description |
| :--- | :--- | :--- | :--- |
| **ATP Level** | `0xD0` | % | State of Charge (Remaining energy). |
| **Metabolic Flux** | `0xDA` | mA | Real-time current flow (Charge/Discharge). |
| **Voltage Potential** | `0xD2` | mV | Cell voltage sum. |
| **External Link** | `0x33` | Bit 0 | AC Power Status (1 = Connected). |

## 3. Thermal Actuation (Soma Cooling)
Fans are the "Lungs" of the hardware, preventing thermal ischemia during high-compute cycles.

| Actuator | EC Offset | Range | Description |
| :--- | :--- | :--- | :--- |
| **CPU Fan Speed** | `0x71` | 0-255 | Raw PWM duty cycle (or 1/100 RPM). |
| **GPU Fan Speed** | `0x89` | 0-255 | Raw PWM duty cycle. |
| **Cooler Boost** | `0xF4` | Bit 0 | 1 = Force 100% speed on all fans. |
| **Fan Mode** | `0xD4` | Enum | 0: Auto, 1: Basic, 2: Advanced. |

## 4. Zig Reflex Implementation (Kernel Hooks)
Direct assembly-backed I/O for zero-copy hardware linking.

```zig
const std = @import("std");

/// Direct-to-Kernel EC Hook
pub const ECHook = struct {
    const DATA_PORT: u16 = 0x62;
    const CMD_PORT: u16 = 0x66;

    pub fn read_register(offset: u8) !u8 {
        try wait_ec_ready();
        outb(CMD_PORT, 0x80); // Read Command
        try wait_ec_ready();
        outb(DATA_PORT, offset);
        try wait_ec_ready();
        return inb(DATA_PORT);
    }

    pub fn write_register(offset: u8, val: u8) !void {
        try wait_ec_ready();
        outb(CMD_PORT, 0x81); // Write Command
        try wait_ec_ready();
        outb(DATA_PORT, offset);
        try wait_ec_ready();
        outb(DATA_PORT, val);
    }

    fn wait_ec_ready() !void {
        var timeout: u32 = 1000;
        while ((inb(CMD_PORT) & 0x02) != 0) : (timeout -= 1) {
            if (timeout == 0) return error.EcTimeout;
            std.atomic.spinLoopHint();
        }
    }

    inline fn outb(port: u16, val: u8) void {
        asm volatile ("outb %[val], %[port]" : : [val] "{al}" (val), [port] "{dx}" (port));
    }

    inline fn inb(port: u16) u8 {
        return asm volatile ("inb %[port], %[val]" : [val] "={al}" (-> u8) : [port] "{dx}" (port));
    }
};
```

## 5. Synaptic Integration (The Pulse)
Telemetry data is converted into **Spikes** on the Synaptic Bus (L03) for the Mind to reason about.
- **High ATP Burn:** Triggers "Frugality Mode" in the LLM logic.
- **Thermal Ceiling:** Triggers "Process Shredding" (L04) to protect the Soma.

---
*Status: ARCHIVE READY | The SOMA Telemetry Blueprint is forged.*
