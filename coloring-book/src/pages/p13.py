"""Page 13 -- Over the Big Leaves.

Looking down into the canopy. The leaves are the biggest single shapes in the
book -- deliberately, after two busy pages.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M

TITLE = "Over the Big Leaves"
SLUG = "over-the-big-leaves"


def perch_bird(cx, cy, s=1.0, flip=False):
    """A long-tailed canopy bird: round body, three tail feathers, one wing."""
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    tail = [blob([P(46, 34), P(158, 6), P(196, 42), P(70, 70)], t=0.7, sharp=(2,)),
            blob([P(50, 52), P(168, 60), P(190, 104), P(64, 92)], t=0.7, sharp=(2,)),
            blob([P(42, 68), P(146, 112), P(152, 156), P(48, 106)], t=0.7, sharp=(2,))]
    body = blob([P(-16, -74), P(48, -30), P(60, 44), P(6, 84), P(-56, 52),
                 P(-70, -18)], t=0.9)
    wing = blob([P(6, -18), P(52, 20), P(28, 62), P(-14, 40)], t=0.9)
    beak = blob([P(-66, -30), P(-116, -14), P(-64, 2)], t=0.5, sharp=(0, 1, 2))
    crest = blob([P(-24, -74), P(-42, -128), P(-2, -104)], t=0.6, sharp=(1,))
    legs = [capsule(*P(-18, 76), *P(-22, 116), 9 * s),
            capsule(*P(16, 74), *P(22, 114), 9 * s)]
    eye = [circle(*P(-38, -34), 11 * s)]
    return [crest] + tail + legs + [body, beak, wing], [], eye


def draw():
    leaves = mid(
        M.leaf(272, 296, 300, 170, rot=-34, ribs=3) +
        M.leaf(606, 288, 290, 164, rot=30, ribs=3) +
        M.leaf(248, 792, 300, 168, rot=38, ribs=3) +
        M.leaf(622, 784, 280, 160, rot=-32, ribs=3) +
        M.leaf(430, 892, 260, 150, rot=84, ribs=3))

    vine = mid([curve([(300, 152), (368, 320), (318, 476), (392, 612)], t=0.9)] +
               M.leaf(268, 262, 116, 60, rot=-52) + M.leaf(376, 404, 116, 60, rot=64))

    b, bl, be = perch_bird(408, 512, 1.28)

    return [leaves, vine, mid(b), ink(be),
            mid([circle(268, 636, 30), circle(224, 682, 22), circle(306, 690, 18)])]
