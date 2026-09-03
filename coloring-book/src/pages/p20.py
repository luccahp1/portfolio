"""Page 20 -- Lantern Bugs at Dusk.

Dusk, so the page turns vertical: tall grass at the bottom, little lantern
bodies floating above it.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M

TITLE = "Lantern Bugs at Dusk"
SLUG = "lantern-bugs-at-dusk"


def lantern_bug(cx, cy, s=1.0, flip=False):
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    wings = [blob([P(-14, -34), P(-96, -84), P(-124, -30), P(-46, 6)], t=0.9),
             blob([P(-6, -30), P(48, -92), P(96, -56), P(38, 4)], t=0.9)]
    lamp = blob([P(-60, 6), P(60, 6), P(70, 74), P(0, 112), P(-70, 74)], t=0.85)
    cap = blob([P(-40, -14), P(40, -14), P(44, 12), P(-44, 12)], t=0.3, sharp=(0, 1, 2, 3))
    ring = circle(*P(0, -30), 15 * s)
    head = circle(*P(0, -46), 26 * s)
    ant = [curve([P(-14, -66), P(-40, -104), P(-64, -110)]),
           curve([P(14, -66), P(40, -104), P(64, -110)])]
    tips = [circle(*P(-70, -116), 10 * s), circle(*P(70, -116), 10 * s)]
    glow = [line(*P(-64, 46), *P(-104, 40)), line(*P(64, 46), *P(104, 40)),
            line(*P(-48, 96), *P(-78, 122)), line(*P(48, 96), *P(78, 122)),
            line(*P(0, 120), *P(0, 154))]
    eyes = [circle(*P(-10, -50), 8 * s), circle(*P(10, -50), 8 * s)]
    return wings + [ring, head, cap, lamp] + tips, ant + glow, eyes


def draw():
    grass = []
    for i in range(8):
        x = 158 + i * 76
        grass += M.tuft(x, 940, 76 + (i % 3) * 14, 150 + (i % 4) * 44, blades=3)
    ground = mid([M.hill(112, 738, 984, 918, bumps=3)])

    out = []
    for cx, cy, s, flip in ((286, 340, 1.0, False), (582, 452, 0.86, True),
                            (352, 616, 0.76, True), (620, 726, 0.66, False)):
        b, l, e = lantern_bug(cx, cy, s, flip)
        out += [mid(b), fine(l), ink(e)]

    sparks = mid([M.star(180, 262, 26), M.star(668, 268, 20), M.star(452, 210, 22),
                  M.star(206, 560, 18), M.star(716, 566, 16)])

    return [ground, mid(grass)] + out + [sparks]
