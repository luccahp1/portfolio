"""Page 23 -- The Lantern Boats.

Folded paper boats, each carrying a lantern, each with a different pattern on
the hull. Reflections are drawn as outlines only -- no gray, nothing to shade.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M

TITLE = "The Lantern Boats"
SLUG = "the-lantern-boats"


def boat(cx, cy, w, h, pattern="stripes"):
    hull = blob([(cx - w * 0.5, cy), (cx + w * 0.5, cy), (cx + w * 0.30, cy + h),
                 (cx - w * 0.30, cy + h)], t=0.2, sharp=(0, 1, 2, 3))
    sail = blob([(cx, cy - h * 1.5), (cx + w * 0.44, cy - h * 0.06),
                 (cx - w * 0.44, cy - h * 0.06)], t=0.2, sharp=(0, 1, 2))
    fold = [line(cx, cy - h * 1.42, cx, cy - h * 0.08)]
    marks = []
    if pattern == "stripes":
        for f in (-0.22, 0.0, 0.22):
            marks.append(line(cx + w * f, cy + h * 0.18, cx + w * f, cy + h * 0.82))
    elif pattern == "dots":
        for f in (-0.24, 0.0, 0.24):
            marks.append(circle(cx + w * f, cy + h * 0.5, h * 0.22))
    else:
        marks.append(curve([(cx - w * 0.32, cy + h * 0.5), (cx - w * 0.12, cy + h * 0.24),
                            (cx + w * 0.10, cy + h * 0.62), (cx + w * 0.32, cy + h * 0.32)],
                           t=0.9))
    return [sail, hull], fold + marks


def lantern(cx, cy, r):
    body = blob([(cx, cy - r), (cx + r * 0.92, cy), (cx, cy + r), (cx - r * 0.92, cy)],
                t=0.95)
    cap = blob([(cx - r * 0.42, cy - r * 0.86), (cx + r * 0.42, cy - r * 0.86),
                (cx + r * 0.30, cy - r * 1.24), (cx - r * 0.30, cy - r * 1.24)],
               t=0.25, sharp=(0, 1, 2, 3))
    ribs = [curve([(cx - r * 0.34, cy - r * 0.80), (cx - r * 0.50, cy),
                   (cx - r * 0.34, cy + r * 0.80)]),
            curve([(cx + r * 0.34, cy - r * 0.80), (cx + r * 0.50, cy),
                   (cx + r * 0.34, cy + r * 0.80)])]
    return [cap, body], ribs


def draw():
    stars = mid([M.star(180, 218, 26), M.star(660, 196, 22), M.star(420, 158, 20),
                 M.star(716, 340, 18)])

    out = []
    for cx, cy, w, h, r, pat in ((256, 486, 244, 108, 42, "stripes"),
                                 (600, 578, 200, 92, 38, "dots"),
                                 (330, 742, 226, 102, 40, "wave"),
                                 (622, 872, 184, 86, 34, "stripes")):
        b, d = boat(cx, cy, w, h, pat)
        mast = capsule(cx + w * 0.34, cy + h * 0.1, cx + w * 0.34, cy - h * 0.5, 7)
        lb, lr = lantern(cx + w * 0.34, cy - h * 0.5 - r * 0.9, r)
        b = b + [mast]
        out += [mid(b), fine(d), mid(lb), fine(lr)]

    water = fine([M.wave_line(126, 726, 630, 14, 4), M.wave_line(126, 726, 824, 14, 4),
                  M.wave_line(126, 726, 950, 14, 4)])
    rings = fine([ellipse(256, 612, 88, 20), ellipse(600, 696, 72, 18),
                  ellipse(330, 864, 80, 18)])

    return [stars] + out + [water, rings]
