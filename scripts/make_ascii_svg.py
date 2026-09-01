"""Convert the prepped plate into an ASCII portrait that types itself in.

Each row is wrapped in a clip that wipes left to right with a small block
cursor riding the edge, staggered top to bottom. It prints once and freezes:
no loop. The motion is SMIL inside the SVG, which is the one kind of animation
GitHub will still run in a README (it strips <script> and almost all inline
CSS, but it renders SVGs embedded with <img> and plays them).

    python scripts/make_ascii_svg.py            # writes profile/ascii-portrait.svg
    STATIC=1 python scripts/make_ascii_svg.py   # frozen frame, for previewing
"""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile_config as cfg  # noqa: E402

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense)
#       ^ the leading space clears the background to nothing

COLS, ROWS = 100, 51
CHAR_W = 6.0
LINE_H = 12.0
PAD = 18.0
BAR_H = 30.0
TOP = BAR_H + 14.0

DUR = 0.55        # seconds for one row's wipe
STAGGER = 0.045   # seconds between rows


def _blur(a, radius):
    """Small separable box blur, so the placeholder needs no extra dependency."""
    k = np.ones(radius * 2 + 1, np.float32) / (radius * 2 + 1)
    out = np.apply_along_axis(lambda m: np.convolve(m, k, "same"), 1, a)
    return np.apply_along_axis(lambda m: np.convolve(m, k, "same"), 0, out)


def sample(args):
    if cfg.PREPPED_PNG.exists():
        img = Image.open(cfg.PREPPED_PNG).convert("L")
        src = "prepped photo"
    else:
        print(f"{cfg.PREPPED_PNG.relative_to(cfg.ROOT)} not found - drawing the "
              f"placeholder bust. Run prep_photo.py to use a real photo.")
        lum = _placeholder_luma(COLS, ROWS)
        img = Image.fromarray(lum.astype(np.uint8), "L")
        src = "placeholder"
    grid = np.asarray(img.resize((COLS, ROWS), Image.LANCZOS), np.float32) / 255.0
    print(f"sampled {src} into a {COLS}x{ROWS} grid")

    grid = np.clip(grid, 0.0, 1.0) ** args.gamma
    if args.contrast != 1.0:
        grid = np.clip((grid - 0.5) * args.contrast + 0.5, 0.0, 1.0)
    return grid


def _placeholder_luma(cols, rows):
    """A lit bust drawn from scratch, so the README is never a broken image.

    Swap it for the real thing by running prep_photo.py on a photo.
    """
    # Build it in the display aspect: a monospace cell is twice as tall as it
    # is wide, so the grid's pixel canvas has to be cols*1 by rows*2.
    w, h = cols * 8, rows * 16
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = (x - w / 2) / (w / 2)
    ny = (y - h / 2) / (h / 2)

    head = ((nx / 0.36) ** 2 + ((ny + 0.42) / 0.44) ** 2) <= 1.0
    neck = (np.abs(nx) < 0.12) & (ny > -0.42) & (ny < 0.80)
    shoulders = ((nx / 0.88) ** 2 + ((ny - 0.80) / 0.58) ** 2) <= 1.0
    # Feather the silhouette so the ramp gets a mid-tone edge, not a step.
    body = np.clip(_blur((head | neck | shoulders).astype(np.float32), 7), 0, 1)

    key = np.clip(1.18 - np.hypot(nx + 0.5, ny + 0.72) * 0.80, 0.04, 1.0)
    rim = np.clip(1.0 - np.hypot(nx - 0.78, ny + 0.42) * 1.7, 0, 1) * 0.62
    subject = 30 + np.clip(key + rim, 0, 1) * 205
    return subject * body + 255.0 * (1 - body)


def to_chars(grid, cutoff):
    last = len(RAMP) - 1
    rows = []
    for line in grid:
        chars = []
        for t in line:
            chars.append(" " if t >= cutoff
                         else RAMP[int(round((1.0 - t) * last))])
        rows.append("".join(chars).rstrip())
    return rows


def build(rows, static):
    w, h = cfg.PORTRAIT_W, cfg.PORTRAIT_H
    body_w = COLS * CHAR_W
    font_size = CHAR_W / 0.6  # nominal monospace advance is 0.6 em

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="ASCII art portrait of {cfg.USERNAME}">',
        f'<title>{cfg.USERNAME} - ASCII portrait</title>',
        cfg.rounded_panel(w, h, title=f"{cfg.USERNAME}@github: ~/portrait",
                          bar_h=BAR_H),
        # xml:space has to be repeated on every <text>: it does not inherit
        # through a <g> in SVG2 text layout, and without it the leading spaces
        # collapse and every row lands at a different scale.
        f'<g font-family="{cfg.MONO}" font-size="{font_size:g}" '
        f'fill="{cfg.FG}">',
    ]

    for i, line in enumerate(rows):
        if not line:
            continue
        y = TOP + i * LINE_H + LINE_H * 0.78
        begin = i * STAGGER
        text_len = len(line) * CHAR_W
        clip = f"r{i}"

        if static:
            out.append(
                f'<text x="{PAD:g}" y="{y:g}" xml:space="preserve" '
                f'textLength="{text_len:g}" '
                f'lengthAdjust="spacingAndGlyphs">{cfg.esc(line)}</text>')
            continue

        out.append(
            f'<clipPath id="{clip}">'
            f'<rect x="{PAD:g}" y="{y - LINE_H:g}" height="{LINE_H + 4:g}" width="0">'
            f'<animate attributeName="width" from="0" to="{body_w:g}" '
            f'begin="{begin:.3f}s" dur="{DUR}s" fill="freeze"/>'
            f'</rect></clipPath>'
            f'<text x="{PAD:g}" y="{y:g}" xml:space="preserve" '
            f'textLength="{text_len:g}" lengthAdjust="spacingAndGlyphs" '
            f'clip-path="url(#{clip})">{cfg.esc(line)}</text>')

    if not static:
        # One cursor block per row, riding the wipe edge and blinking out when
        # its row is done.
        out.append(f'<g fill="{cfg.GREEN}">')
        for i, line in enumerate(rows):
            if not line:
                continue
            y = TOP + i * LINE_H
            begin = i * STAGGER
            out.append(
                f'<rect y="{y + 2:g}" width="{CHAR_W:g}" height="{LINE_H - 3:g}" '
                f'x="{PAD:g}" opacity="0">'
                f'<animate attributeName="x" from="{PAD:g}" '
                f'to="{PAD + body_w:g}" begin="{begin:.3f}s" dur="{DUR}s" '
                f'fill="freeze"/>'
                f'<set attributeName="opacity" to="0.9" begin="{begin:.3f}s"/>'
                f'<set attributeName="opacity" to="0" '
                f'begin="{begin + DUR:.3f}s" fill="freeze"/>'
                f'</rect>')
        out.append('</g>')

    out.append('</g></svg>')
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gamma", type=float, default=1.0,
                    help="<1 brightens the art, >1 darkens it")
    ap.add_argument("--contrast", type=float, default=1.0,
                    help="multiplier around mid-grey")
    ap.add_argument("--cutoff", type=float, default=0.965,
                    help="brightness at or above which a cell prints nothing")
    ap.add_argument("--static", action="store_true",
                    help="emit a frozen frame instead of the typing animation")
    args = ap.parse_args()

    static = args.static or os.environ.get("STATIC") == "1"
    rows = to_chars(sample(args), args.cutoff)
    ink = sum(len(r) for r in rows)
    print(f"{ink:,} glyphs across {sum(1 for r in rows if r)} printed rows")
    cfg.write(cfg.PORTRAIT_SVG, build(rows, static))


if __name__ == "__main__":
    main()
