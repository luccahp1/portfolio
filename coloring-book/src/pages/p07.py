"""Page 7 -- Ledge of the Mountain Goats.

First page with new animals. They use the same face module as Sorrel and Mo, so
they read as part of the same book rather than clip art dropped in.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, capsule, ink)
import motifs as M

TITLE = "Ledge of the Mountain Goats"
SLUG = "ledge-of-the-mountain-goats"


def rock(cx, cy, w, h, seed=0):
    j = (0.06 * ((seed % 3) - 1), 0.08 * ((seed % 2) - 0.5))
    return blob([(cx - w * 0.5, cy + h * 0.5), (cx - w * (0.42 + j[0]), cy - h * 0.30),
                 (cx - w * 0.16, cy - h * 0.5), (cx + w * (0.24 + j[1]), cy - h * 0.44),
                 (cx + w * 0.5, cy + h * 0.1), (cx + w * 0.38, cy + h * 0.5)],
                t=0.55, sharp=(0, 5))


def goat(cx, cy, s=1.0, flip=False, wave=False):
    """Round mountain goat: oval body, capsule legs, two swept horns, and the
    same two-dot-and-a-smile face as everyone else in the book."""
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    def B(pts, **kw):
        return blob([P(x, y) for x, y in pts], **kw)

    body = B([(0, -72), (96, -50), (112, 20), (72, 74), (-40, 78), (-104, 44),
              (-112, -30), (-60, -70)], t=0.9)
    legs = [capsule(*P(74, 40), *P(86, 150), 21 * s),
            capsule(*P(34, 56), *P(30, 150), 21 * s),
            capsule(*P(-78, 42), *P(-88, 150), 21 * s),
            capsule(*P(-38, 56), *P(-34, 150), 21 * s)]
    hooves = [ellipse(*P(88, 162), 26 * s, 18 * s), ellipse(*P(30, 162), 26 * s, 18 * s),
              ellipse(*P(-90, 162), 26 * s, 18 * s), ellipse(*P(-34, 162), 26 * s, 18 * s)]
    if wave:
        legs[0] = capsule(*P(78, 10), *P(158, -50), 21 * s)
        hooves[0] = ellipse(*P(168, -58), 26 * s, 20 * s, rot=-30 * d)
    neck = capsule(*P(70, -30), *P(140, -118), 36 * s)
    head = B([(112, -190), (180, -200), (236, -168), (244, -118), (194, -88),
              (136, -102), (106, -148)], t=0.9)
    horns = [B([(150, -196), (112, -244), (52, -252), (78, -216), (128, -178)],
               t=0.7, sharp=(2,)),
             B([(178, -200), (140, -252), (80, -262), (106, -224), (156, -182)],
               t=0.7, sharp=(2,))]
    ear = B([(134, -140), (78, -128), (74, -96), (128, -104)], t=0.8)
    beard = B([(186, -88), (206, -34), (168, -60), (152, -92)], t=0.8, sharp=(1,))
    tail = B([(-100, -56), (-140, -110), (-118, -46), (-96, -22)], t=0.8, sharp=(1,))
    eyes = [circle(*P(172, -158), 11 * s), circle(*P(214, -152), 11 * s)]
    smile = curve([P(196, -122), P(212, -110), P(228, -122)])
    nose = curve([P(232, -140), P(238, -134), P(232, -128)])
    return ([tail, ear] + horns + legs + hooves + [neck, body, head, beard],
            [smile, nose], eyes)


def draw():
    sky = mid([M.cloud(226, 210, 196, 90, bumps=3),
               M.cloud(186, 452, 150, 70, bumps=3, seed=2)] + M.bird(392, 342, 54))

    balloon = at(628, 288, 0.24, M.wander(0.24))

    ledges = mid([rock(300, 878, 372, 200, 1), rock(608, 818, 268, 196, 2),
                  rock(196, 716, 150, 124, 0)])

    g1, g1l, g1e = goat(298, 692, 0.62, flip=False, wave=True)
    g2, g2l, g2e = goat(614, 612, 0.55, flip=True)

    return [sky, balloon, ledges,
            mid(g1), fine(g1l), ink(g1e),
            mid(g2), fine(g2l), ink(g2e),
            mid(M.tuft(152, 946, 62, 54) + M.tuft(706, 940, 58, 50))]
