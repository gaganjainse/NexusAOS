package com.nexus.shell

import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

object NexusTheme {
    const val PHI = 1.61803398875f

    object Dimensions {
        val paddingSmall = 8.dp
        val paddingMedium = (8.dp.value * PHI).dp
        val paddingLarge = (paddingMedium.value * PHI).dp
        
        fun goldenScale(base: Dp): Dp = (base.value * PHI).dp
    }

    object Colors {
        val NeonTeal = androidx.compose.ui.graphics.Color(0xFF00FFCC)
        val DeepVoid = androidx.compose.ui.graphics.Color(0xFF0A0A0A)
        val GlassSurface = androidx.compose.ui.graphics.Color(0xAA121212)
    }
}
