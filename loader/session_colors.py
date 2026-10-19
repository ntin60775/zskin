#!/usr/bin/env python3
"""Per-session accent colors for the zskin sidebar (flat task list).

Port of oh-my-pi packages/tui/src/theme/session-color.ts (plus the OKLCH
plumbing pi-utils provides there): a session id is hashed to an OKLCH hue
on a theme-safe arc, and the theme accent's perceived weight (lightness /
chroma position relative to its own gamut cusp) is carried over to the new
hue. Guarantees: no yellow/chartreuse core on dark (mustard shift), cool
band on light, WCAG AA-large contrast on light surfaces, chroma floor when
the accent is near-gray.

stdlib-only, same bar as zskin.py. The gamut-cusp table is cached under
~/.cache/zskin/ (build-time math, keyed by format version).

This module is palette-coupled to themes/gruvbox.css on purpose: the
accent and collision hexes below mirror that theme's two schemes.
"""

import json
import math
import os
import sys

CACHE_PATH = os.path.join(
    os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
    "zskin", "oklch-cusp-v1.json")

# Bounds carried over from session-color.ts.
MIN_CHROMA = 0.05
MAX_CHROMA = 0.21
DARK_MIN_LIGHTNESS = 0.65
DARK_MAX_LIGHTNESS = 0.88
ACCENT_MIN_CONTRAST = 3
MIN_HUE_DISTANCE = 10
MIN_CHROMA_FOR_HUE = 0.03
FALLBACK_CUSP_CHROMA_FRACTION = 0.7

# gruvbox.css, dark scheme (html.theme-zai-dark / html.dark): accent plus
# every saturated semantic color, so session hues keep their distance.
DARK_INPUTS = {
    "accent": "#fe8019",
    "colors": ["#ebdbb2", "#fabd2f", "#b8bb26", "#8ec07c",
               "#83a598", "#d3869b", "#fb4934"],
    "surface_luminance": None,  # dark path
}

# gruvbox.css, light scheme (html.theme-zai-light): same rule; the surface
# is the sidebar background the row text sits on.
LIGHT_INPUTS = {
    "accent": "#d65d0e",
    "colors": ["#d65d0e", "#98971a", "#d79921", "#458588",
               "#8f3f71", "#cc241d", "#427b58", "#3c3836"],
    "surface_luminance": None,  # filled from LIGHT_SURFACE at import
}
LIGHT_SURFACE = "#ebdbb2"

# ----- OKLCH <-> sRGB (Ottosson OKLab matrices) -----

def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c):
    if c <= 0.0031308:
        return 12.92 * c
    return 1.055 * (c ** (1 / 2.4)) - 0.055


def _cbrt(x):
    return math.copysign(abs(x) ** (1.0 / 3.0), x)


def hex_to_rgb(hex_str):
    s = hex_str.strip().lstrip("#")
    return tuple(int(s[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(
        max(0, min(255, round(v * 255.0))) for v in rgb)


def hex_to_oklch(hex_str):
    r, g, b = (_srgb_to_linear(v) for v in hex_to_rgb(hex_str))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = _cbrt(l), _cbrt(m), _cbrt(s)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b2 = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    c = math.hypot(a, b2)
    h = math.degrees(math.atan2(b2, a)) % 360.0
    return {"l": L, "c": c, "h": h}


def _oklch_to_linear(L, c, h):
    hr = math.radians(h)
    a = c * math.cos(hr)
    b = c * math.sin(hr)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def _in_gamut(L, c, h):
    return all(-1e-6 <= v <= 1 + 1e-6 for v in _oklch_to_linear(L, c, h))


def oklch_to_hex(L, c, h):
    lin = (max(0.0, min(1.0, v)) for v in _oklch_to_linear(L, c, h))
    return rgb_to_hex(tuple(_linear_to_srgb(v) for v in lin))


def relative_luminance(hex_str):
    r, g, b = (_srgb_to_linear(v) for v in hex_to_rgb(hex_str))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _max_chroma(L, h):
    lo, hi = 0.0, 0.4
    if not _in_gamut(L, lo, h):
        return 0.0
    for _ in range(18):
        mid = (lo + hi) / 2
        if _in_gamut(L, mid, h):
            lo = mid
        else:
            hi = mid
    return lo


def _cusp(h):
    """Gamut-boundary vertex for hue h: {l, c} at the chroma maximum."""
    best_l, best_c = 0.5, 0.0
    for i in range(1, 99):
        L = i / 100.0
        c = _max_chroma(L, h)
        if c > best_c:
            best_l, best_c = L, c
    # refine around the winner
    span = 0.01
    for _ in range(2):
        for step in (-span, span):
            L = max(0.01, min(0.99, best_l + step))
            c = _max_chroma(L, h)
            if c > best_c:
                best_l, best_c = L, c
        span /= 2.0
    return {"l": best_l, "c": best_c}


def _load_cusp_table():
    """{hue: {l, c}} for all integer hues, cached on disk (build math)."""
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("v") == 1:
            return {int(k): v for k, v in data["cusps"].items()}
    except (OSError, ValueError, AttributeError):
        pass
    cusps = {h: _cusp(h) for h in range(360)}
    try:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        tmp = CACHE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"v": 1, "cusps": cusps}, f)
        os.replace(tmp, CACHE_PATH)
    except OSError:
        pass
    return cusps


CUSPS = _load_cusp_table()

# omp DARK_HUE_INTERVALS: hues whose vividness peak stays reachable under
# the dark lightness cap; recomputed from the cusp table.
def _intervals_where(predicate):
    out, start = [], -1
    for h in range(361):
        if h < 360 and predicate(h):
            if start < 0:
                start = h
        elif start >= 0:
            out.append((start, h - 1))
            start = -1
    return out


def _arc_length(intervals):
    return sum(b - a + 1 for a, b in intervals)


def _arc_to_hue(intervals, pos):
    p = pos
    for a, b in intervals:
        n = b - a + 1
        if p < n:
            return a + p
        p -= n
    return intervals[-1][1] if intervals else 0


def _hue_distance(a, b):
    d = abs(a - b)
    return min(d, 360 - d)


def _find_safe_hue(pos, occupied, intervals):
    total = _arc_length(intervals)
    target = _arc_to_hue(intervals, max(0, min(total - 1, pos)))
    if not occupied:
        return target
    if all(_hue_distance(target, h) >= MIN_HUE_DISTANCE for h in occupied):
        return target
    for d in range(1, total):
        for dir_step in (1, -1):
            candidate = _arc_to_hue(
                intervals, max(0, min(total - 1, pos + d * dir_step)))
            if all(_hue_distance(candidate, h) >= MIN_HUE_DISTANCE
                   for h in occupied):
                return candidate
    return target


def _name_to_hash(name):
    """djb2, 32-bit unsigned (verbatim from session-color.ts)."""
    hash_ = 5381
    for ch in name:
        hash_ = ((hash_ << 5) + hash_) ^ ord(ch)
        hash_ &= 0xFFFFFFFF
    return hash_


def _hex_hues(color_hexes):
    hues = []
    for hex_str in color_hexes:
        ok = hex_to_oklch(hex_str)
        if ok["c"] >= MIN_CHROMA_FOR_HUE:
            hues.append(ok["h"])
    return hues


def session_accent_hex(name, accent_hex, color_hexes, surface_luminance=None):
    """Stable accent hex for a session id; port of computeSessionAccentHex.

    surface_luminance=None selects the dark path (clamp to visible
    lightness); a value selects the light path (bisection to WCAG
    AA-large against that surface).
    """
    is_dark = surface_luminance is None
    intervals = (
        _intervals_where(lambda h: CUSPS[h]["l"] <= DARK_MAX_LIGHTNESS)
        if is_dark else [(195, 330)])

    pos = _name_to_hash(name) % _arc_length(intervals)
    target_hue = _find_safe_hue(pos, _hex_hues(color_hexes), intervals)

    accent = hex_to_oklch(accent_hex)
    usable = (accent["c"] >= MIN_CHROMA_FOR_HUE)
    target = CUSPS[int(target_hue) % 360]
    if usable:
        source = CUSPS[int(accent["h"]) % 360]
        if accent["l"] <= source["l"]:
            lightness = (accent["l"] / source["l"]) * target["l"]
        else:
            lightness = target["l"] + (
                (accent["l"] - source["l"]) / (1 - source["l"])) * (1 - target["l"])
        chroma_fraction = accent["c"] / source["c"]
    else:
        lightness = target["l"]
        chroma_fraction = FALLBACK_CUSP_CHROMA_FRACTION
    chroma = max(MIN_CHROMA, min(MAX_CHROMA, chroma_fraction * target["c"]))

    if is_dark:
        l = max(DARK_MIN_LIGHTNESS, min(DARK_MAX_LIGHTNESS, lightness))
        return oklch_to_hex(l, chroma, target_hue)

    cap = max(0.0, (surface_luminance + 0.05) / ACCENT_MIN_CONTRAST - 0.05)
    top = oklch_to_hex(lightness, chroma, target_hue)
    if relative_luminance(top) <= cap:
        return top
    lo, hi = 0.0, lightness
    for _ in range(20):
        mid = (lo + hi) / 2
        if relative_luminance(oklch_to_hex(mid, chroma, target_hue)) > cap:
            hi = mid
        else:
            lo = mid
    return oklch_to_hex(lo, chroma, target_hue)


def build_layer(session_ids):
    """CSS layer coloring flat sidebar rows; empty string without ids.

    Both theme schemes get their own ruleset (scoped like gruvbox.css),
    each computed with its own accent, collisions and surface.
    """
    if not session_ids:
        return ""
    dark_lum = LIGHT_INPUTS["surface_luminance"]
    assert dark_lum is not None, "LIGHT_INPUTS.surface_luminance not set"
    lines = [
        "",
        "/* ===== zskin session colors (generated at inject; flat sidebar) =====",
        " * hue = djb2(session id) on the omp session-color arc; gruvbox accents",
        " * and collision hexes mirror themes/gruvbox.css. Sessions created after",
        " * the last inject are uncolored until the next one. */",
    ]
    for scope, inputs in (
            ("html.theme-zai-dark, html.dark", DARK_INPUTS),
            ("html.theme-zai-light", LIGHT_INPUTS)):
        lines.append("")
        for sid in session_ids:
            hex_color = session_accent_hex(
                sid, inputs["accent"], inputs["colors"],
                inputs["surface_luminance"])
            lines.append(
                '%s li[data-testid="task-item-%s"] '
                '{ box-shadow: inset 3px 0 0 %s; }' % (scope, sid, hex_color))
    return "\n".join(lines) + "\n"


LIGHT_INPUTS["surface_luminance"] = relative_luminance(LIGHT_SURFACE)


# ----- self-test: the property checks of omp's session-color.test.ts -----

def _selftest():
    names = ["analyze-debian-trixie-%d" % i for i in range(600)]
    dark_accent, light_accent = "#e5c07b", "#7287fd"
    tol = 2.0
    failures = []

    def check(label, ok):
        print(("PASS " if ok else "FAIL ") + label)
        if not ok:
            failures.append(label)

    def hues_of(accent, light=None):
        return [
            hex_to_oklch(session_accent_hex(
                n, accent, [], light))["h"] for n in names]

    check("deterministic",
          session_accent_hex("x", dark_accent, [])
          == session_accent_hex("x", dark_accent, []))

    dark_default = hues_of(dark_accent)
    check("dark: cusp lightness reachable (<=0.89)",
          all(CUSPS[int(h) % 360]["l"] <= 0.88 + 0.01 for h in dark_default))
    warm = sum(1 for h in dark_default if h < 94 or h > 350)
    check("dark: warm share < 0.5 (%.2f)" % (warm / len(names)),
          warm / len(names) < 0.5)

    yellow_ok = True
    for accent in (dark_accent, "#ed4abf", "#7aa2f7"):
        for h in hues_of(accent):
            if not (h < 94 + tol or h > 138 - tol):
                yellow_ok = False
    check("dark: never in yellow core 94-138", yellow_ok)

    pastel_ok = True
    for n in names[:50]:
        vivid = hex_to_oklch(session_accent_hex(n, "#ed4abf", []))["c"]
        pastel = hex_to_oklch(session_accent_hex(n, "#bb9af7", []))["c"]
        if not (pastel <= vivid + 0.01 and pastel >= 0.04):
            pastel_ok = False
    check("dark: pastel <= vivid chroma, floor 0.04", pastel_ok)

    gray_ok = all(
        hex_to_oklch(session_accent_hex(n, "#8a8a8e", []))["c"] >= 0.04
        for n in names[:50])
    check("dark: near-gray accent keeps chroma floor", gray_ok)

    dark_ok = all(
        hex_to_oklch(session_accent_hex(n, "#5a3d1e", []))["l"] >= 0.63
        for n in names[:50])
    check("dark: very dark accent raised to visible lightness", dark_ok)

    check("dark: max luminance > 0.5",
          max(relative_luminance(
              session_accent_hex(n, dark_accent, [])) for n in names) > 0.5)

    for label, surface in (("crust #dce0e8", "#dce0e8"),
                           ("poimandres #7390aa", "#7390aa")):
        bg = relative_luminance(surface)
        light_hues, contrast_ok = [], True
        for n in names:
            hx = session_accent_hex(n, light_accent, [], bg)
            light_hues.append(hex_to_oklch(hx)["h"])
            la, lb = relative_luminance(hx), bg
            contrast = ((max(la, lb) + 0.05) / (min(la, lb) + 0.05))
            if contrast < 2.99:
                contrast_ok = False
        check("light %s: WCAG >= 2.99" % label, contrast_ok)
        check("light %s: cool band 195-330" % label,
              all(195 - tol <= h <= 330 + tol for h in light_hues))

    near_white = relative_luminance("#dce0e8")
    order_ok = all(
        relative_luminance(session_accent_hex(
            n, dark_accent, [], near_white))
        <= relative_luminance(session_accent_hex(n, dark_accent, [])) + 1e-9
        for n in names)
    check("light accent never lighter than dark twin", order_ok)

    if failures:
        print("FAILED: %d" % len(failures))
        return 1
    print("all properties hold")
    return 0


if __name__ == "__main__":
    sys.exit(_selftest())
