# IntelliJ plugins (personal)

Two IntelliJ IDEA 2026.3+ plugins, each a standalone Gradle project built with JetBrains'
official [IntelliJ Platform Gradle Plugin 2.x](https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin.html).

| Project | What it is | Code? |
|---|---|---|
| [`everforest-theme/`](everforest-theme/) | Everforest UI theme + editor/terminal colour scheme | Resources only (JSON + XML) |
| [`nowina-progress-bar/`](nowina-progress-bar/) | Progress bar with the Nowina "N" logo (like Mario Progress Bar) | Java (Swing) |

## Common commands (run inside a project folder)

```bash
export JAVA_HOME=~/.jdks/corretto-25.0.5   # any JDK 21+ works
./gradlew buildPlugin   # -> build/distributions/<name>-<version>.zip
./gradlew runIde        # starts a sandbox IntelliJ with the plugin loaded (safe for testing)
```

Install the zip via **Settings → Plugins → ⚙️ → Install Plugin from Disk…**

Both projects compile against the IntelliJ installed by Toolbox (`localIdePath` in
`gradle.properties`) instead of downloading the platform, so builds are fast and offline-friendly.
