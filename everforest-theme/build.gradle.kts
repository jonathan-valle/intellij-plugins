// Theme plugin: resources only (JSON + XML), no code.
// JetBrains' official Gradle plugin handles packaging and patching plugin.xml.
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
        local(providers.gradleProperty("localIdePath"))
    }
}

intellijPlatform {
    pluginConfiguration {
        ideaVersion {
            sinceBuild = "263"
            untilBuild = provider { null }
        }
    }
    buildSearchableOptions = false
    instrumentCode = false
}
