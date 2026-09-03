"""Page 24 -- Home Again.

The last page brings back the balloon, both pilots and the friends met along the
way, under a string of bunting. The busiest page in the book, saved for the end.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M
from p10 import hedgehog
from p07 import goat

TITLE = "Home Again"
SLUG = "home-again"


def bunting(pts, flags=7):
    string = curve(pts, t=0.9)
    tri = []
    for i in range(flags):
        f = (i + 0.5) / flags
        j = f * (len(pts) - 1)
        k = min(len(pts) - 2, int(j))
        t = j - k
        x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * t
        y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * t + 14 * (1 - abs(f - 0.5) * 2)
        tri.append(poly([(x - 26, y), (x + 26, y), (x, y + 66)]))
    return string, tri


def draw():
    poles = mid([capsule(150, 640, 150, 310, 12), capsule(716, 640, 716, 292, 12)])
    string, flags = bunting([(150, 316), (300, 386), (452, 404), (600, 372), (716, 300)])

    ground = mid([M.hill(112, 736, 982, 706, bumps=3)])

    balloon = at(452, 336, 0.42, M.wander(0.42))
    pilot = at(452, 400, 0.36, M.sorrel(0.36, pose="peek", goggles=True))
    mo = at(560, 452, 0.24, M.mo(0.24, flip=True))

    h, hl, he = hedgehog(238, 806, 0.58)
    g, gl, ge = goat(608, 754, 0.40, flip=True, wave=True)

    sorrel_ground = at(424, 704, 0.34, M.sorrel(0.34, pose="wave", goggles=False))

    blooms = mid(M.flower(172, 860, 28, stem=80) + M.flower(686, 848, 28, stem=74) +
                 M.tuft(330, 902, 66, 56) + M.tuft(486, 916, 60, 52) +
                 M.tuft(636, 890, 58, 50))

    return [poles, mid(flags), fine([string]), ground, balloon, pilot, mo,
            mid(h), fine(hl), ink(he), mid(g), fine(gl), ink(ge),
            sorrel_ground, blooms]
