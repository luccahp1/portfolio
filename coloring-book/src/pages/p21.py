"""Page 21 -- Star Nets.

Night flight. The balloon returns full size with a lantern hung off the basket,
and the sky fills with two sizes of star so the page has a rhythm to it.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M

TITLE = "Star Nets"
SLUG = "star-nets"


def moon(cx, cy, r):
    """Crescent: one disc with a bite taken out, drawn as a single closed path."""
    import math
    a0, a1 = math.radians(-62), math.radians(62)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return __import__("inkstyle").path(
        "M%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f Z"
        % (x0, y0, r, r, x1, y1, r * 1.15, r * 1.15, x0, y0))


def lantern(cx, cy, w, h):
    body = blob([(cx - w / 2.0, cy - h * 0.32), (cx, cy - h * 0.5),
                 (cx + w / 2.0, cy - h * 0.32), (cx + w * 0.42, cy + h * 0.34),
                 (cx, cy + h * 0.5), (cx - w * 0.42, cy + h * 0.34)], t=0.9)
    cap = blob([(cx - w * 0.30, cy - h * 0.44), (cx + w * 0.30, cy - h * 0.44),
                (cx + w * 0.24, cy - h * 0.66), (cx - w * 0.24, cy - h * 0.66)],
               t=0.25, sharp=(0, 1, 2, 3))
    ribs = [line(cx - w * 0.20, cy - h * 0.36, cx - w * 0.26, cy + h * 0.34),
            line(cx + w * 0.20, cy - h * 0.36, cx + w * 0.26, cy + h * 0.34)]
    return [cap, body], ribs


def draw():
    sky_stars = mid([M.star(180, 236, 34), M.star(300, 172, 24), M.star(676, 214, 32),
                     M.star(560, 148, 22), M.star(150, 470, 26), M.star(716, 452, 24),
                     M.star(196, 764, 30), M.star(690, 780, 26), M.star(392, 894, 24),
                     M.star(586, 936, 20)])
    sparkles = fine([line(268, 380, 268, 440), line(238, 410, 298, 410),
                     line(628, 620, 628, 676), line(600, 648, 656, 648),
                     line(324, 940, 324, 986), line(302, 964, 348, 964)])

    m = mid([moon(618, 336, 92)])

    balloon = at(424, 496, 0.60, M.wander(0.60))
    pilot = at(424, 604, 0.52, M.sorrel(0.52, pose="peek", goggles=True))

    lb, lr = lantern(300, 848, 96, 122)
    hang = mid([capsule(340, 782, 302, 792, 7)])

    return [sky_stars, sparkles, m, balloon, pilot, hang, mid(lb), fine(lr)]
