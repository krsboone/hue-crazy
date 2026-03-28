#!/usr/bin/env python3
"""
cycle.py — Slowly cycle a Hue light through a sequence of colors.

Usage:
    python3 cycle.py                        # cycle through all colors, 5s each
    python3 cycle.py --secs 10              # 10 seconds per color
    python3 cycle.py --light 3              # use a different light
    python3 cycle.py --colors blue purple lavender white
    python3 cycle.py --once                 # run through once, then stop
"""

import argparse
import time
import requests

from hue import BRIDGE, API_KEY, COLORS, DEFAULT_LIGHT

DEFAULT_SECS = 5

DEFAULT_SEQUENCE = [
    "blue", "purple", "lavender", "white",
    "teal", "green", "yellow", "orange",
    "pink", "red",
]


def set_xy(light_id: int, xy: list[float]) -> None:
    url = f"http://{BRIDGE}/api/{API_KEY}/lights/{light_id}/state"
    requests.put(url, json={"xy": xy, "transitiontime": 10}, timeout=5)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--light",  type=int,   default=DEFAULT_LIGHT)
    parser.add_argument("--secs",   type=float, default=DEFAULT_SECS)
    parser.add_argument("--colors", nargs="+",  default=DEFAULT_SEQUENCE)
    parser.add_argument("--once",   action="store_true")
    args = parser.parse_args()

    sequence = [c for c in args.colors if c in COLORS]
    if not sequence:
        print("No valid colors in sequence.")
        return

    print(f"  Cycling light {args.light} through: {', '.join(sequence)}")
    print(f"  {args.secs}s per color  —  Ctrl+C to stop\n")

    try:
        while True:
            for color in sequence:
                print(f"  → {color}")
                set_xy(args.light, COLORS[color])
                time.sleep(args.secs)
            if args.once:
                break
    except KeyboardInterrupt:
        print("\n  Stopped.")


if __name__ == "__main__":
    main()
