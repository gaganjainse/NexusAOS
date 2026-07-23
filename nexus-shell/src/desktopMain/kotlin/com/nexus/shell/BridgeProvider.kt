package com.nexus.shell

actual object BridgeProvider {
    actual fun getVibe(): Int = SomaBridge.getVibe()
}
