package com.nexus.shell

import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import androidx.compose.ui.window.rememberWindowState
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.WindowPlacement
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.window.WindowStyle
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier

fun main() = application {
    val windowState = rememberWindowState(
        width = 1280.dp,
        height = 800.dp,
        placement = WindowPlacement.Floating
    )

    Window(
        onCloseRequest = ::exitApplication,
        state = windowState,
        title = "Nexus Sovereign Shell",
        undecorated = true, // For custom glass-morphism feel
        transparent = true
    ) {
        App()
    }
}
