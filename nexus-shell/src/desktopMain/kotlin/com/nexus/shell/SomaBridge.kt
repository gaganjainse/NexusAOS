package com.nexus.shell

import com.sun.jna.Library
import com.sun.jna.Native

interface SomaLibrary : Library {
    fun get_system_vibe(): Int
    fun shred_process(pid: Int): Boolean
    fun get_memory_pressure(): Float
    fun execute_reflex_command(cmd: String, len: Int): Boolean
}

object SomaBridge {
    private val lib: SomaLibrary? by lazy {
        try {
            Native.load("nexus_soma", SomaLibrary::class.java)
        } catch (e: UnsatisfiedLinkError) {
            println("Soma Bridge: Native library not found. Falling back to simulation.")
            null
        }
    }

    fun getVibe(): Int = lib?.get_system_vibe() ?: 0
    fun shred(pid: Int): Boolean = lib?.shred_process(pid) ?: false
    fun getMemoryPressure(): Float = lib?.get_memory_pressure() ?: 0.0f
    fun executeReflex(cmd: String): Boolean = lib?.execute_reflex_command(cmd, cmd.length) ?: true
}
