package com.Sesha.shell

import com.sun.jna.Library
import com.sun.jna.Native

interface SomaLibrary : Library {
    fun get_cpu_thermal_vibe(): Float
    fun get_battery_status(): Int
    fun get_system_entropy_vibe(): Int
    fun get_memory_pressure(): Float
    fun execute_reflex_command(cmd: String, len: Int): Boolean
}

object SomaBridge {
    private val lib: SomaLibrary? by lazy {
        try {
            // Load the Sesha_soma library (mapped from Zig build)
            Native.load("Sesha_soma", SomaLibrary::class.java)
        } catch (e: UnsatisfiedLinkError) {
            println("Soma Bridge: Native library 'Sesha_soma' not found. Falling back to simulation.")
            null
        }
    }

    fun getThermal(): Float = lib?.get_cpu_thermal_vibe() ?: 45.0f
    fun getBatteryStatus(): Int = lib?.get_battery_status() ?: 1
    fun getVibe(): Int = lib?.get_system_entropy_vibe() ?: 0
    fun getMemoryPressure(): Float = lib?.get_memory_pressure() ?: 0.0f
    fun executeReflex(cmd: String): Boolean = lib?.execute_reflex_command(cmd, cmd.length) ?: true
}

