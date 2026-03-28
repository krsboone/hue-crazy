#!/usr/bin/env python3
"""
hue.py — Philips Hue light controller

Usage:
    python3 hue.py <color>              # set office light (6)
    python3 hue.py <color> <light_id>  # set specific light
    python3 hue.py list                 # show available colors

Examples:
    python3 hue.py lavender
    python3 hue.py blue 3
    python3 hue.py list
"""

import sys
import requests

# ── Bridge configuration ──────────────────────────────────────────────────────

BRIDGE   = "your-bridge-ip"
API_KEY  = "your-api-key"
DEFAULT_LIGHT = 6

# ── Color palette (CIE xy coordinates) ───────────────────────────────────────

COLORS: dict[str, list[float]] = {
    "red":      [0.675,  0.322 ],
    "orange":   [0.5567, 0.4091],
    "yellow":   [0.4325, 0.5007],
    "green":    [0.4091, 0.518 ],
    "teal":     [0.2857, 0.2744],
    "blue":     [0.167,  0.04  ],
    "purple":   [0.2485, 0.0917],
    "pink":     [0.5388, 0.2464],
    "white":    [0.3227, 0.3290],
    "lavender": [0.3085, 0.3071],
}


def set_color(light_id: int, color_name: str) -> bool:
    xy = COLORS.get(color_name.lower())
    if xy is None:
        print(f"Unknown color: '{color_name}'")
        print(f"Available: {', '.join(sorted(COLORS))}")
        return False
    url  = f"http://{BRIDGE}/api/{API_KEY}/lights/{light_id}/state"
    resp = requests.put(url, json={"xy": xy}, timeout=5)
    resp.raise_for_status()
    print(f"  Light {light_id} → {color_name}")
    return True


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] == "list":
        print("Colors:", ", ".join(sorted(COLORS)))
        return

    color    = args[0]
    light_id = int(args[1]) if len(args) > 1 else DEFAULT_LIGHT
    set_color(light_id, color)


if __name__ == "__main__":
    main()
