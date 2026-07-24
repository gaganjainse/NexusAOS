package com.Sesha.shell

actual object BridgeProvider {
    actual fun getVibe(): Int = SomaBridge.getVibe()
}

