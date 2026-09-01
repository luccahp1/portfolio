"""Hand-authored neofetch-style card that prints itself line by line.

The contribution graph already carries the numbers, so this panel is for the
story the numbers do not tell: what I am building, what I built it on, and
where it runs. Edit LINES below and re-run; nothing here is scraped.

    python scripts/make_info_card.py            # writes profile/info-card.svg
    STATIC=1 python scripts/make_info_card.py   # frozen frame, for previewing
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile_config as cfg  # noqa: E402

C = cfg  # shorthand for the palette below

# (key, value, key colour). A key of None prints the value full width; an
# empty tuple is a blank spacer line.
LINES = [
    ("Now", "IT Solution Delivery Co-op @ WSIB - Java, Spring Boot", C.GREEN),
    ("", "health-check automation, JWT/cookie request handling,", None),
    ("", "an iText upgrade through a legacy Java codebase", None),
    (),
    ("Building", "Atrio - an AI phone receptionist, live 24/7 on a real", C.BLUE),
    ("", "number. Custom Node bridge streams G.711 straight", None),
    ("", "between SignalWire and Inworld: ~640-820 ms to first", None),
    ("", "audio. Self-hosted, watchdogged every 10 minutes.", None),
    ("", "Outpace - speed-to-lead replies in the owner's voice,", None),
    ("", "in minutes. Next.js, Claude API, libSQL, 40 unit tests.", None),
    (),
    ("Prev", "Co-op Developer @ DevLift - 2023", C.PURPLE),
    ("School", "Fanshawe, Computer Programming & Analysis", C.PURPLE),
    ("", "WSIB Scholars Award (full scholarship)", None),
    (),
    ("Stack", "Java · Spring Boot · Python · TypeScript · Next.js · SQL", C.ORANGE),
    ("Ops", "Ubuntu · nginx · systemd · Tailscale · UFW · Git", C.ORANGE),
    ("AI", "Claude API · realtime speech-to-speech · agent design", C.ORANGE),
    (),
    ("Host", "luccaserver - a closet in London, Ontario", C.DIM),
    ("Site", "luccahp1.github.io/portfolio", C.DIM),
]

PAD = 24.0
BAR_H = 30.0
LINE_H = 21.5
KEY_W = 78.0
FONT = 12.5
STAGGER = 0.055
DUR = 0.42

# The neofetch colour strip, minus the ANSI.
SWATCHES = [C.RED, C.ORANGE, C.GREEN, "#2ea043", C.BLUE, C.PURPLE, C.FG, C.DIM]


def build(static):
    w, h = cfg.CARD_W, cfg.CARD_H
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="Terminal info card for {cfg.USERNAME}">',
        f'<title>{cfg.USERNAME} - whoami</title>',
        cfg.rounded_panel(w, h, title=f"{cfg.USERNAME}@github: ~", bar_h=BAR_H),
        f'<g font-family="{cfg.MONO}" font-size="{FONT}">',
    ]

    y = BAR_H + PAD + 12
    step = 0

    def row(fragment, delay_index):
        """Wrap a line so it fades and slides up into place, once."""
        if static:
            return f'<g>{fragment}</g>'
        begin = delay_index * STAGGER
        return (f'<g opacity="0" transform="translate(0 6)">{fragment}'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{begin:.3f}s" dur="{DUR}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" '
                f'from="0 6" to="0 0" begin="{begin:.3f}s" dur="{DUR}s" '
                f'fill="freeze"/></g>')

    # Header: the neofetch "user@host" line and its underline.
    head = (f'<text x="{PAD}" y="{y}" fill="{cfg.GREEN}" font-weight="600">'
            f'{cfg.USERNAME}</text>'
            f'<text x="{PAD + len(cfg.USERNAME) * FONT * 0.6:.1f}" y="{y}" '
            f'fill="{cfg.FG}">@</text>'
            f'<text x="{PAD + (len(cfg.USERNAME) + 1) * FONT * 0.6:.1f}" y="{y}" '
            f'fill="{cfg.BLUE}" font-weight="600">london.on</text>')
    out.append(row(head, step))
    step += 1
    y += LINE_H * 0.75
    rule = ("-" * 30)
    out.append(row(f'<text x="{PAD}" y="{y}" fill="{cfg.DIM}">{rule}</text>', step))
    step += 1
    y += LINE_H * 1.15

    for line in LINES:
        if not line:
            y += LINE_H * 0.5
            continue
        key, value, colour = line
        parts = []
        if key:
            parts.append(f'<text x="{PAD}" y="{y}" fill="{colour}" '
                         f'font-weight="600">{cfg.esc(key)}</text>')
        parts.append(f'<text x="{PAD + KEY_W}" y="{y}" '
                     f'fill="{cfg.FG if key else cfg.DIM}">'
                     f'{cfg.esc(value)}</text>')
        out.append(row("".join(parts), step))
        step += 1
        y += LINE_H

    # Colour strip, bottom left, the way neofetch signs off.
    sw_y = h - PAD - 14
    sw = "".join(
        f'<rect x="{PAD + i * 22:.0f}" y="{sw_y}" width="18" height="12" rx="2" '
        f'fill="{colour}"/>' for i, colour in enumerate(SWATCHES))
    out.append(row(sw, step))

    out.append('</g></svg>')
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--static", action="store_true",
                    help="emit a frozen frame instead of the fade-in")
    args = ap.parse_args()
    static = args.static or os.environ.get("STATIC") == "1"
    cfg.write(cfg.INFO_CARD_SVG, build(static))


if __name__ == "__main__":
    main()
