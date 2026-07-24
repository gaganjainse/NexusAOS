package com.Sesha.shell

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
    val thermalVibe = SomaBridge.getThermal()
    val pulseDuration = (10000 / (thermalVibe / 20)).toInt().coerceIn(2000, 8000)

    val infiniteTransition = rememberInfiniteTransition()
    val pulse by infiniteTransition.animateFloat(
        initialValue = 0.8f,
        targetValue = 1.2f,
        animationSpec = infiniteRepeatable(
            animation = tween(pulseDuration, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
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
                moveTo(centerX, centerY + 200f)
                quadraticBezierTo(
                    centerX + sin(rad) * 400f * pulse,
                    centerY - 300f + cos(rad) * 100f,
                    centerX + sin(rad) * 200f,
                    centerY - 500f * pulse
                )
            }
            
            drawPath(
                path = hoodPath,
                color = SeshaTheme.Colors.NeonTeal.copy(alpha = 0.2f * pulse),
                style = Stroke(width = 3f)
            )
        }
    }
}

