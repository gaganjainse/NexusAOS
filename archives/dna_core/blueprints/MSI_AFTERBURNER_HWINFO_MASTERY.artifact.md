# Forge ID 46: MSI Afterburner / HWInfo Operations Mastery
Version: 1.0.0
Description: Deep technical integration with MSI Afterburner (RTSS) and HWInfo Shared Memory (SHM) for real-time hardware sovereignty.

## 1. MSI Afterburner / RivaTuner (RTSS) SHM Integration
RTSS provides a high-performance OSD (On-Screen Display) via a versioned Shared Memory interface.

### 1.1 Shared Memory Access
- **File Mapping Name:** `RTSSSharedMemoryV2`
- **Mutex Name:** `RTSSSharedMemoryV2Mutex`
- **Signature:** `0x53535452` ('RTSS')

### 1.2 RTSS_SHARED_MEMORY_HEADER (v2.0+)
```cpp
typedef struct RTSS_SHARED_MEMORY_HEADER
{
	DWORD	dwSignature;		// 'RTSS'
	DWORD	dwVersion;			// 0x00020000 for v2.0
	DWORD	dwAppEntryOffset;	// Offset to RTSS_APP_ENTRY array
	DWORD	dwAppEntrySize;		// Size of RTSS_APP_ENTRY
	DWORD	dwAppEntryCount;	// Number of app entries
	// ... (OSD specific fields)
} RTSS_SHARED_MEMORY_HEADER;
```

### 1.3 OSD Text Injection (Tags)
RTSS supports rich text formatting within the OSD buffer:
- `<C=RRGGBB>`: Color (Hex)
- `<S=Percent>`: Size scaling
- `<I>`: Italic
- `<B>`: Bold
- `<G=GraphID>`: Embedded graph object
- `<P=X,Y>`: Position offset

## 2. HWInfo Shared Memory Telemetry
HWInfo exposes nearly all sensor data (Voltage, Temp, Power, Clock) via its SMM (System Management Mode) bridge.

### 2.1 Shared Memory Access
- **File Mapping Name:** `Global\HWiNFO_SMM_SharedMemory`
- **Mutex Name:** `Global\HWiNFO_SMM_SharedMemoryMutex`

### 2.2 HWINFO_SMM_SHARED_MEMORY_FOOTER
Used to locate the sensor and reading blocks.
```cpp
typedef struct _HWINFO_SMM_SHARED_MEMORY_FOOTER {
    DWORD dwSignature;          // 'HWiN'
    DWORD dwVersion;            // Version of the interface
    DWORD dwRevision;           // Revision of the interface
    double pollTime;            // Current polling time
    // Offset-based navigation to Sensor Reading entries
} HWINFO_SMM_SHARED_MEMORY_FOOTER;
```

### 2.3 Integration Pattern (Nexus Soma)
1. **PULSE Initiation:** Nexus opens `HWiNFO_SMM_SharedMemory`.
2. **INGESTION:** Read `HWINFO_SMM_SENSOR_READING` array (CPU Temp, GPU Pwr, VRAM Usage).
3. **SYNTHESIS:** Process telemetry through L07 safety thresholds.
4. **INJECTION:** Format high-salience vitals into an OSD string.
5. **PROJECTION:** Write to `RTSSSharedMemoryV2` embedded object buffer to render on screen.

## 3. Kinetic Optimality & Safety
- **Zero-Copy Synapse:** Use pointer-based reading from SHM to minimize CPU cycles.
- **Mutex Discipline:** Always lock/unlock mutexes to prevent race conditions with the host apps.
- **Fail-Safe:** If SHM is not found, default to internal L01 kernel vitals (if available).

---
*Status: FORGED | The Steel speaks. The Vitals are manifest.*
