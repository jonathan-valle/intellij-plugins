// IntelliJ plugin built with JetBrains' official Gradle plugin
// (IntelliJ Platform Gradle Plugin 2.x): https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin.html
plugins {
    java
    id("org.jetbrains.intellij.platform") version "2.20.1"
}

group = "perso.jonathan"
version = "1.0.0"

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Compile against the installed IntelliJ (path set in gradle.properties)
        local(providers.gradleProperty("localIdePath"))
    }
}

// IntelliJ 2026.3 runs on Java 25, but targeting 21 keeps the bytecode broadly compatible.
tasks.withType<JavaCompile>().configureEach {
    options.release = 21
    options.encoding = "UTF-8"
}

intellijPlatform {
    pluginConfiguration {
        ideaVersion {
            sinceBuild = "263"      // IntelliJ 2026.3 or newer
            untilBuild = provider { null } // no upper bound
        }
    }
    buildSearchableOptions = false // no settings page: useless and slow
    instrumentCode = false         // no .form files or @NotNull annotations to instrument
}
