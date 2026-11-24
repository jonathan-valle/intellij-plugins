# Everforest (perso) — IntelliJ theme

The **Islands Dark** UI recoloured with the [Everforest](https://github.com/sainnhe/everforest)
*dark medium* palette, plus an editor colour scheme whose console/terminal ANSI colours match
the Everforest palette of the Ptyxis terminal. Background `#2D353B` instead of Islands Dark's `#191A1C`.

## How an IntelliJ theme plugin works

```
src/main/resources/
├── META-INF/plugin.xml            # declares <themeProvider path="/themes/everforest.theme.json"/>
└── themes/
    ├── everforest.theme.json      # UI theme (Swing component colours)
    └── everforest.xml             # editor colour scheme (.icls format), referenced by "editorScheme"
```

**`everforest.theme.json`**
- `"parentTheme": "ExperimentalDark"` — inherits everything from the New UI dark theme.
- `"colors"` — *named* colours (`gray-10`, `blue-80`, `editor-text`, …). This is the palette;
  the `ui` section only references these names, so **recolouring = editing `colors`**.
  The greys were remapped to the Everforest background ramp and JetBrains' blue accent to Everforest green.
- `"ui"` — per-component keys (`"*"` is the wildcard default; `"Islands": 1` enables the island layout).
  Copied as-is from Islands Dark.
- `"editorScheme": "/themes/everforest.xml"` — the editor scheme applied with the theme.

**`everforest.xml`** (editor scheme)
- `<colors>` — editor chrome: caret row, gutter, selection, indent guides, VCS markers…
- `<attributes>` — syntax highlighting keys (`DEFAULT_KEYWORD`, `DEFAULT_STRING`, …) and the
  console ANSI colours (`CONSOLE_RED_OUTPUT`, …). `FONT_TYPE` 1 = bold, 2 = italic;
  `EFFECT_TYPE` 1 = underline, 2 = wave underline, 3 = strikeout.
- `parent_scheme="Darcula"` — any key not listed falls back to Darcula.

Tip: in IntelliJ, **Settings → Editor → Color Scheme** shows the key behind any colour —
tweak it there, then copy the value back into `everforest.xml`.

## `tools/build_everforest.py`

The one-off generator that produced the two theme files from Islands Dark. Only re-run it to rebase
on a newer Islands Dark (it overwrites the files); for small tweaks, edit the files directly.

## Build / test

```bash
./gradlew buildPlugin   # build/distributions/everforest-theme-1.0.0.zip
./gradlew runIde        # sandbox IDE, then pick Settings → Appearance → Theme → Everforest
```
If **Sync with OS** is ticked in Appearance, IntelliJ forces its own dark theme — untick it.
