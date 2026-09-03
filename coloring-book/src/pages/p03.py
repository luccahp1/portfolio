"""Page 3 -- The Wander Wakes Up.

The balloon is introduced whole and at rest, so the hero object is established
before it ever leaves the ground. Sorrel stands in front of the basket, which
is what sets the depth order for the rest of the book.
"""
from inkstyle import mid, fine, at, circle, curve, blob, line
import motifs as M

TITLE = "The Wander Wakes Up"
SLUG = "the-wander-wakes-up"


def sack(cx, cy, w, h):
    """A tied sandbag: rounded body, cinched neck, tie line."""
    body = blob([(cx, cy - h * 0.30), (cx + w * 0.5, cy + h * 0.06),
                 (cx + w * 0.40, cy + h * 0.5), (cx, cy + h * 0.58),
                 (cx - w * 0.40, cy + h * 0.5), (cx - w * 0.5, cy + h * 0.06)], t=0.9)
    neck = blob([(cx - w * 0.20, cy - h * 0.28), (cx - w * 0.26, cy - h * 0.56),
                 (cx + w * 0.26, cy - h * 0.56), (cx + w * 0.20, cy - h * 0.28)], t=0.5)
    tie = curve([(cx - w * 0.22, cy - h * 0.24), (cx, cy - h * 0.14),
                 (cx + w * 0.22, cy - h * 0.24)])
    return [neck, body], [tie]


def draw():
    sky = mid([M.cloud(214, 206, 200, 92, bumps=3),
               M.cloud(648, 176, 176, 84, bumps=3, seed=2)])

    ground = mid([M.hill(106, 744, 984, 872, bumps=3)])

    balloon = at(478, 512, 0.72, M.wander(0.72))

    b1, t1 = sack(632, 856, 128, 126)
    b2, t2 = sack(692, 890, 88, 84)
    sacks = [mid(b1 + b2), fine(t1 + t2)]

    sorrel = at(234, 692, 0.44, M.sorrel(0.44, pose="wave", goggles=True))
    mo = at(392, 916, 0.34, M.mo(0.34, flip=True))

    return [sky, ground, balloon] + sacks + [sorrel, mo,
            mid(M.tuft(534, 924, 68, 58) + M.tuft(156, 934, 62, 52))]
