package com.Sesha.shell

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

import androidx.compose.ui.tooling.preview.Preview

@Composable
@Preview
fun AppPreview() {
    App()
}

@Composable
fun App() {
    val infiniteTransition = rememberInfiniteTransition()
    val drift by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1000f,
        animationSpec = infiniteRepeatable(
            animation = tween(20000, easing = LinearEasing)
        )
    )

    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = SeshaTheme.Colors.NeonTeal,
            background = Color.Transparent,
            surface = SeshaTheme.Colors.GlassSurface
        )
    ) {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = Color.Black.copy(alpha = 0.4f)
        ) {
            // Phase 3: Shesha Naga & Kinetic Fluidity
            SheshaNagaOverlay()

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(SeshaTheme.Dimensions.paddingLarge),
                contentAlignment = Alignment.Center
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(SeshaTheme.Dimensions.paddingMedium)
                ) {
                    Text(
                        text = "Sesha SOVEREIGN",
                        style = MaterialTheme.typography.headlineLarge.copy(
                            letterSpacing = 10.sp,
                            color = SeshaTheme.Colors.NeonTeal,
                            shadow = androidx.compose.ui.graphics.Shadow(
                                color = SeshaTheme.Colors.NeonTeal,
                                blurRadius = 20f
                            )
                        )
                    )
                    
                    Text(
                        text = "STATE: CONVERGED | VIBE: ${BridgeProvider.getVibe()}",
                        style = MaterialTheme.typography.bodyMedium.copy(
                            color = Color.White.copy(alpha = 0.7f),
                            letterSpacing = 5.sp
                        )
                    )
                }
            }
        }
    }
}

