#!/usr/bin/env python3
"""Generates the Everforest theme files in src/main/resources/themes/.

One-off tool: it starts from the Islands Dark theme shipped with IntelliJ and swaps its palette.
Only re-run it to rebase on a newer Islands Dark; for small tweaks, edit the files in
src/main/resources/themes/ directly (careful: re-running overwrites them).

Usage (from the project root):
  unzip -p <IDE>/lib/intellij.platform.resources.jar themes/islands/ManyIslandsDark.theme.json > /tmp/islands.json
  python3 tools/build_everforest.py /tmp/islands.json
"""
import json, pathlib, sys

src = sys.argv[1]
OUT = pathlib.Path(__file__).resolve().parent.parent / "src/main/resources/themes"
t = json.load(open(src))

# --- Everforest Dark Medium palette (same as Ptyxis) -------------------------
BG0, BG1, BG2, BG3, BG4, BG5 = "#2D353B", "#343F44", "#3D484D", "#475258", "#4F585E", "#56635F"
BG_DIM, BG_VISUAL, BG_RED, BG_GREEN, BG_BLUE, BG_YELLOW = "#232A2E", "#4C3743", "#514045", "#425047", "#3A515D", "#4D4C43"
FG, GREY0, GREY1, GREY2 = "#D3C6AA", "#7A8478", "#859289", "#9DA9A0"
RED, ORANGE, YELLOW, GREEN, AQUA, BLUE, PURPLE = "#E67E80", "#E69875", "#DBBC7F", "#A7C080", "#83C092", "#7FBBB3", "#D699B6"

c = t["colors"]
# Greys -> Everforest ramp (10 = island background, 30 = window frame)
c.update({
    "gray-10": BG0, "gray-20": "#313A40", "gray-30": BG1, "gray-40": BG2, "gray-50": BG3,
    "gray-60": BG4, "gray-70": BG5, "gray-80": GREY0, "gray-90": GREY1, "gray-100": GREY2,
    "gray-110": "#B4B39F", "gray-120": "#C4BDA5", "gray-130": FG, "gray-140": "#DDD3B8",
    "gray-150": "#E6DEC6", "gray-160": "#F2EFDF",
})
# JetBrains "blue" accent -> Everforest green (selections, buttons, active tabs)
c.update({
    "blue-10": "#262E2A", "blue-20": "#2A332D", "blue-30": "#303A32", "blue-40": "#384539",
    "blue-50": BG_GREEN, "blue-60": "#4E5E48", "blue-70": "#5E7350", "blue-80": "#6F8A55",
    "blue-90": "#8AA36A", "blue-100": GREEN, "blue-110": "#B5CB93", "blue-120": "#C3D5A6",
    "blue-130": "#D0DEB9", "blue-140": "#DDE7CC", "blue-150": "#EAF0DF", "blue-160": "#F5F8EF",
})
c.update({
    "red-100": RED, "red-80": "#C8686A", "red-40": BG_RED,
    "yellow-100": YELLOW, "yellow-80": "#B89A5E", "yellow-40": BG_YELLOW,
    "orange-100": ORANGE, "purple-100": PURPLE, "teal-100": AQUA,
    "green-100": AQUA, "green-90": "#6FA67E", "green-80": "#5A8C69", "green-40": BG_GREEN,
    "text-link": BLUE, "editor-text": FG, "search-match-bg": "#B39A62",
    "transparent": BG0 + "00", "tab-file-color-mask-bg": BG0 + "80",
    "popup-completion-match-text": GREEN, "icon-green-stroke": GREEN,
})

t["name"] = "Everforest"
t["author"] = "Jonathan (perso)"
t["editorScheme"] = "/themes/everforest.xml"

# --- Editor colour scheme ----------------------------------------------------
def h(x): return x.lstrip("#")

colors = {
    "CARET_COLOR": FG, "CARET_ROW_COLOR": "#333C42", "CONSOLE_BACKGROUND_KEY": BG0,
    "GUTTER_BACKGROUND": BG0, "LINE_NUMBERS_COLOR": BG5, "LINE_NUMBER_ON_CARET_ROW_COLOR": GREY1,
    "SELECTION_BACKGROUND": BG_GREEN, "INDENT_GUIDE": BG2, "SELECTED_INDENT_GUIDE": BG4,
    "SOFT_WRAP_SIGN_COLOR": BG4, "WHITESPACES": BG3, "RIGHT_MARGIN_COLOR": BG2,
    "TEARLINE_COLOR": BG2, "SELECTED_TEARLINE_COLOR": BG4, "METHOD_SEPARATORS_COLOR": BG2,
    "DOCUMENTATION_COLOR": BG1, "LOOKUP_COLOR": BG1, "INFORMATION_HINT": BG1,
    "ADDED_LINES_COLOR": "#899C40", "MODIFIED_LINES_COLOR": "#5F8E87", "DELETED_LINES_COLOR": "#B85F61",
    "WHITESPACES_MODIFIED_LINES_COLOR": "#5F8E87", "IGNORED_ADDED_LINES_BORDER_COLOR": "#899C40",
    "FILESTATUS_ADDED": GREEN, "FILESTATUS_MODIFIED": BLUE, "FILESTATUS_DELETED": RED,
    "FILESTATUS_UNKNOWN": ORANGE, "FILESTATUS_IGNORED": GREY0,
    "VISUAL_INDENT_GUIDE": BG2, "TOOLTIP": BG1, "NOTIFICATION_BACKGROUND": BG1,
    "ScrollBar.Mac.thumbColor": BG4 + "80", "ScrollBar.thumbColor": BG4 + "80",
}

# key -> (fg, bg, font_type, effect_color, effect_type)   font: 1 bold, 2 italic
# effect_type: 1 underline, 2 wave underline, 3 strikeout
A = {
    "TEXT": (FG, BG0), "DEFAULT_IDENTIFIER": (FG,), "IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, BG2),
    "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": (None, BG_BLUE),
    "DEFAULT_KEYWORD": (RED,), "DEFAULT_STRING": (AQUA,), "DEFAULT_VALID_STRING_ESCAPE": (ORANGE,),
    "DEFAULT_INVALID_STRING_ESCAPE": (RED, None, 0, RED, 2),
    "DEFAULT_NUMBER": (PURPLE,), "DEFAULT_CONSTANT": (PURPLE,), "DEFAULT_PREDEFINED_SYMBOL": (PURPLE,),
    "DEFAULT_LINE_COMMENT": (GREY1, None, 2), "DEFAULT_BLOCK_COMMENT": (GREY1, None, 2),
    "DEFAULT_DOC_COMMENT": (GREY1, None, 2), "DEFAULT_DOC_COMMENT_TAG": (AQUA, None, 2),
    "DEFAULT_DOC_COMMENT_TAG_VALUE": (BLUE, None, 2), "DEFAULT_DOC_MARKUP": (GREY2,),
    "DEFAULT_FUNCTION_DECLARATION": (GREEN,), "DEFAULT_FUNCTION_CALL": (GREEN,),
    "DEFAULT_INSTANCE_METHOD": (GREEN,), "DEFAULT_STATIC_METHOD": (GREEN, None, 2),
    "DEFAULT_CLASS_NAME": (YELLOW,), "DEFAULT_CLASS_REFERENCE": (YELLOW,), "DEFAULT_INTERFACE_NAME": (YELLOW,),
    "DEFAULT_INSTANCE_FIELD": (BLUE,), "DEFAULT_STATIC_FIELD": (BLUE, None, 2),
    "DEFAULT_LOCAL_VARIABLE": (FG,), "DEFAULT_REASSIGNED_LOCAL_VARIABLE": (FG, None, 0, GREY0, 1),
    "DEFAULT_PARAMETER": (FG,), "DEFAULT_REASSIGNED_PARAMETER": (FG, None, 0, GREY0, 1),
    "DEFAULT_GLOBAL_VARIABLE": (BLUE,),
    "DEFAULT_METADATA": (PURPLE,), "ANNOTATION_NAME_ATTRIBUTES": (PURPLE,), "ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": (AQUA,),
    "ENUM_CONST": (PURPLE,), "TYPE_PARAMETER_NAME_ATTRIBUTES": (ORANGE,),
    "DEFAULT_OPERATION_SIGN": (ORANGE,), "DEFAULT_BRACES": (GREY2,), "DEFAULT_BRACKETS": (GREY2,),
    "DEFAULT_PARENTHS": (GREY2,), "DEFAULT_COMMA": (GREY2,), "DEFAULT_SEMICOLON": (GREY2,), "DEFAULT_DOT": (GREY2,),
    "DEFAULT_LABEL": (ORANGE,), "DEFAULT_TAG": (ORANGE,), "DEFAULT_ATTRIBUTE": (YELLOW,),
    "DEFAULT_ENTITY": (PURPLE,), "DEFAULT_TEMPLATE_LANGUAGE_COLOR": (FG, BG1),
    "JAVA_KEYWORD": (RED,), "JAVA_STRING": (AQUA,), "JAVA_NUMBER": (PURPLE,),
    "KOTLIN_KEYWORD": (RED,), "KOTLIN_STRING": (AQUA,),
    "XML_TAG_NAME": (ORANGE,), "XML_ATTRIBUTE_NAME": (YELLOW,), "XML_ATTRIBUTE_VALUE": (AQUA,),
    "JSON.PROPERTY_KEY": (BLUE,), "YAML_SCALAR_KEY": (BLUE,), "PROPERTIES.KEY": (BLUE,),
    "MATCHED_BRACE_ATTRIBUTES": (None, BG4, 1), "UNMATCHED_BRACE_ATTRIBUTES": (None, BG_RED),
    "SEARCH_RESULT_ATTRIBUTES": (None, BG_YELLOW), "WRITE_SEARCH_RESULT_ATTRIBUTES": (None, "#5A4E3B"),
    "TEXT_SEARCH_RESULT_ATTRIBUTES": (None, BG_YELLOW),
    "ERRORS_ATTRIBUTES": (None, None, 0, RED, 2), "WRONG_REFERENCES_ATTRIBUTES": (RED,),
    "WARNING_ATTRIBUTES": (None, None, 0, YELLOW, 2), "WEAK_WARNING_ATTRIBUTES": (None, None, 0, GREY1, 2),
    "INFO_ATTRIBUTES": (None, None, 0, BLUE, 2),
    "NOT_USED_ELEMENT_ATTRIBUTES": (GREY0,), "DEPRECATED_ATTRIBUTES": (None, None, 0, FG, 3),
    "MARKED_FOR_REMOVAL_ATTRIBUTES": (None, None, 0, RED, 3),
    "TODO_DEFAULT_ATTRIBUTES": (YELLOW, None, 3), "HYPERLINK_ATTRIBUTES": (BLUE, None, 0, BLUE, 1),
    "FOLLOWED_HYPERLINK_ATTRIBUTES": (PURPLE, None, 0, PURPLE, 1),
    "INLAY_DEFAULT": (GREY1, BG1), "INLINE_PARAMETER_HINT": (GREY1, BG1), "INLINE_PARAMETER_HINT_HIGHLIGHTED": (FG, BG2),
    "BREAKPOINT_ATTRIBUTES": (None, BG_RED), "EXECUTIONPOINT_ATTRIBUTES": (None, BG_BLUE),
    "FOLDED_TEXT_ATTRIBUTES": (GREY1, BG1),
    "DIFF_INSERTED": (None, BG_GREEN), "DIFF_MODIFIED": (None, BG_BLUE),
    "DIFF_DELETED": (None, BG_RED), "DIFF_CONFLICT": (None, BG_VISUAL),
    # Console + built-in terminal: ANSI palette from Ptyxis Everforest
    "CONSOLE_NORMAL_OUTPUT": (FG,), "CONSOLE_ERROR_OUTPUT": (RED,), "CONSOLE_SYSTEM_OUTPUT": (GREY1,),
    "CONSOLE_USER_INPUT": (GREEN, None, 2), "LOG_ERROR_OUTPUT": (RED,), "LOG_WARNING_OUTPUT": (YELLOW,),
    "CONSOLE_BLACK_OUTPUT": ("#4B565C",), "CONSOLE_RED_OUTPUT": (RED,), "CONSOLE_GREEN_OUTPUT": (GREEN,),
    "CONSOLE_YELLOW_OUTPUT": (YELLOW,), "CONSOLE_BLUE_OUTPUT": (BLUE,), "CONSOLE_MAGENTA_OUTPUT": (PURPLE,),
    "CONSOLE_CYAN_OUTPUT": (AQUA,), "CONSOLE_GRAY_OUTPUT": (FG,), "CONSOLE_DARKGRAY_OUTPUT": ("#5C6A72",),
    "CONSOLE_RED_BRIGHT_OUTPUT": ("#F85552",), "CONSOLE_GREEN_BRIGHT_OUTPUT": ("#8DA101",),
    "CONSOLE_YELLOW_BRIGHT_OUTPUT": ("#DFA000",), "CONSOLE_BLUE_BRIGHT_OUTPUT": ("#3A94C5",),
    "CONSOLE_MAGENTA_BRIGHT_OUTPUT": ("#DF69BA",), "CONSOLE_CYAN_BRIGHT_OUTPUT": ("#35A77C",),
    "CONSOLE_WHITE_OUTPUT": ("#DFDDC8",),
}

lines = ['<scheme name="Everforest" version="142" parent_scheme="Darcula">', "  <colors>"]
lines += [f'    <option name="{k}" value="{h(v)}" />' for k, v in colors.items()]
lines += ["  </colors>", "  <attributes>"]
for name, spec in A.items():
    fg, bg, font, ec, et = (list(spec) + [None, None, 0, None, None])[:5]
    lines.append(f'    <option name="{name}">')
    lines.append("      <value>")
    if fg: lines.append(f'        <option name="FOREGROUND" value="{h(fg)}" />')
    if bg: lines.append(f'        <option name="BACKGROUND" value="{h(bg)}" />')
    if font: lines.append(f'        <option name="FONT_TYPE" value="{font}" />')
    if ec: lines.append(f'        <option name="EFFECT_COLOR" value="{h(ec)}" />')
    if et: lines.append(f'        <option name="EFFECT_TYPE" value="{et}" />')
    lines.append("      </value>")
    lines.append("    </option>")
lines += ["  </attributes>", "</scheme>", ""]
scheme = "\n".join(lines)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "everforest.theme.json").write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
(OUT / "everforest.xml").write_text(scheme)
print("ok ->", OUT)
