package com.nexus.shell

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.geometry.Offset
import kotlin.math.sin
import kotlin.math.cos

@Composable
fun SheshaNagaOverlay() {
    val infiniteTransition = rememberInfiniteTransition()
    val pulse by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(4000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        )
    )

    Canvas(modifier = Modifier.fillMaxSize()) {
        val centerX = size.width / 2
        val centerY = size.height / 2
        
        // Simulating the 7 hoods of Shesha Naga with golden geometry
        for (i in -3..3) {
            val angle = i * 20f
            val rad = Math.toRadians(angle.toDouble()).toFloat()
            
            val hoodPath = Path().apply {
                moveTo(centerX, centerY + 100f)
                quadraticBezierTo(
                    centerX + sin(rad) * 300f,
                    centerY - 400f + cos(rad) * 100f,
                    centerX + sin(rad) * 150f,
                    centerY - 600f * pulse
                )
            }
            
            drawPath(
                path = hoodPath,
                color = NexusTheme.Colors.NeonTeal.copy(alpha = 0.3f),
                style = Stroke(width = 2f)
            )
        }
    }
}
