plugins {
    kotlin("multiplatform") version "2.0.0"
    id("org.jetbrains.compose") version "1.6.11"
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.0"
}

kotlin {
    jvm("desktop")

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation(compose.runtime)
                implementation(compose.foundation)
                implementation(compose.material3)
                implementation(compose.ui)
                implementation(compose.components.resources)
                implementation(compose.components.uiToolingPreview)
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.1")
            }
        }

        val desktopMain by getting {
            dependencies {
                implementation(compose.desktop.currentOs)
                implementation("net.java.dev.jna:jna:5.14.0")
            }
        }
    }
}

compose.desktop {
    application {
        mainClass = "com.nexus.shell.MainKt"

        nativeDistributions {
            targetFormats(org.jetbrains.compose.desktop.application.dsl.TargetFormat.Exe)
            packageName = "NexusSovereignShell"
            packageVersion = "1.0.0"
        }
    }
}
