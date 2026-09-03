"""Page 16 -- Down to the Reef.

Underwater, so the page fills corner to corner for the first time. Every shape
is still a closed one a crayon can sit inside.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M

TITLE = "Down to the Reef"
SLUG = "down-to-the-reef"


def fish(cx, cy, s=1.0, flip=False, scales=True):
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    body = blob([P(-96, 0), P(-30, -62), P(60, -46), P(104, 0), P(60, 48),
                 P(-30, 62)], t=0.9)
    tail = blob([P(-88, 0), P(-166, -56), P(-150, 0), P(-166, 56)],
                t=0.6, sharp=(1, 2, 3))
    fin_top = blob([P(-6, -56), P(30, -104), P(58, -50)], t=0.8, sharp=(1,))
    fin_low = blob([P(-2, 54), P(18, 92), P(48, 46)], t=0.8, sharp=(1,))
    gill = curve([P(38, -40), P(22, 0), P(38, 42)], t=0.9)
    eye = [circle(*P(62, -14), 11 * s)]
    detail = [gill]
    if scales:
        for k in range(3):
            x = -20 + k * 34
            detail.append(curve([P(x, -30), P(x + 18, 0), P(x, 30)], t=0.9))
    return [tail, fin_top, fin_low, body], detail, eye


def coral_fan(cx, base, w, h):
    stem = capsule(cx, base, cx, base - h * 0.34, 14)
    fan = M.puff(cx, base - h * 0.62, w, h * 0.68, bumps=3, seed=1)
    ribs = [curve([(cx, base - h * 0.32), (cx - w * 0.22, base - h * 0.62),
                   (cx - w * 0.26, base - h * 0.86)]),
            curve([(cx, base - h * 0.32), (cx, base - h * 0.92)]),
            curve([(cx, base - h * 0.32), (cx + w * 0.22, base - h * 0.62),
                   (cx + w * 0.26, base - h * 0.86)])]
    return [stem, fan], ribs


def weed(cx, base, h, lean=1):
    """A closed, tapering ribbon of seaweed -- colorable, not just a squiggle."""
    return blob([(cx - 22, base), (cx + lean * 34, base - h * 0.34),
                 (cx - lean * 40, base - h * 0.66), (cx + lean * 18, base - h),
                 (cx + lean * 40, base - h * 0.62), (cx - lean * 14, base - h * 0.32),
                 (cx + 22, base)], t=0.85)


def draw():
    floor = mid([M.hill(112, 738, 984, 848, bumps=3)])

    c1, r1 = coral_fan(268, 874, 200, 290)
    c2, r2 = coral_fan(612, 892, 180, 250)

    star = mid([M.star(424, 892, 92, inner=0.52)])
    star_dots = fine([circle(424, 892, 22), circle(424, 838, 11), circle(378, 918, 11),
                      circle(470, 918, 11)])

    f1, d1, e1 = fish(300, 320, 1.0)
    f2, d2, e2 = fish(612, 486, 0.78, flip=True)
    f3, d3, e3 = fish(388, 636, 0.62)

    bubbles = mid([circle(508, 236, 26), circle(566, 300, 18), circle(482, 176, 16),
                   circle(206, 520, 22), circle(166, 452, 15), circle(700, 300, 20)])

    weeds = mid([weed(156, 906, 226, 1), weed(700, 908, 210, -1)])

    return [weeds, mid(c1 + c2), fine(r1 + r2), floor, star, star_dots,
            mid(f1), fine(d1), ink(e1),
            mid(f2), fine(d2), ink(e2),
            mid(f3), fine(d3), ink(e3), bubbles]
