"""Page 14 -- Nap in the Hammock.

The quiet page of the jungle stretch. Closed eyes instead of dots -- the only
face in the book that changes, and only because it is asleep.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, capsule, ink)
import motifs as M

TITLE = "Nap in the Hammock"
SLUG = "nap-in-the-hammock"


def trunk(cx, top, base, w):
    body = blob([(cx - w / 2.0, top), (cx + w / 2.0, top), (cx + w * 0.58, base),
                 (cx - w * 0.58, base)], t=0.2, sharp=(0, 1, 2, 3))
    bark = [curve([(cx - w * 0.16, top + 90), (cx - w * 0.04, top + 190),
                   (cx - w * 0.18, top + 290)]),
            curve([(cx + w * 0.22, top + 160), (cx + w * 0.10, top + 250),
                   (cx + w * 0.24, top + 340)])]
    return body, bark


def sleeper(cx, cy, s=1.0):
    """A slow, sleepy friend curled in the hammock."""
    def P(x, y):
        return (cx + x * s, cy + y * s)

    body = blob([P(-150, 4), P(-60, -54), P(70, -50), P(150, 10), P(120, 76),
                 P(-110, 78)], t=0.9)
    head = blob([P(-146, -34), P(-88, -66), P(-30, -34), P(-38, 34), P(-100, 56),
                 P(-152, 26)], t=0.9)
    ear = blob([P(-140, -46), P(-160, -92), P(-102, -70)], t=0.7)
    arm = capsule(*P(30, -20), *P(96, -104), 24 * s)
    paw = circle(*P(102, -114), 28 * s)
    foot = [capsule(*P(-30, 60), *P(-40, 116), 20 * s), circle(*P(-44, 126), 24 * s)]
    eyes = [curve([P(-124, -14), P(-110, -4), P(-96, -14)]),
            curve([P(-76, -16), P(-62, -6), P(-48, -16)])]
    nose = ellipse(*P(-146, 2), 13 * s, 10 * s)
    smile = curve([P(-124, 20), P(-110, 32), P(-94, 20)])
    return [ear, arm, paw] + foot + [body, head, nose], eyes + [smile]


def draw():
    t1, b1 = trunk(206, 300, 962, 130)
    t2, b2 = trunk(664, 300, 962, 116)

    canopy = mid([M.puff(240, 224, 250, 176, bumps=3, seed=1),
                  M.puff(626, 210, 234, 162, bumps=3, seed=2)])

    hammock = mid([blob([(238, 520), (420, 700), (628, 512), (664, 548),
                         (426, 782), (204, 556)], t=0.85)])
    net = fine([curve([(268, 552), (420, 716), (596, 546)], t=0.9),
                curve([(298, 588), (422, 730), (566, 580)], t=0.9),
                line(300, 566, 316, 610), line(360, 640, 368, 686),
                line(420, 670, 422, 722), line(486, 636, 480, 682),
                line(546, 570, 534, 614)])

    ropes = mid([capsule(238, 520, 214, 486, 8), capsule(628, 512, 656, 480, 8)])

    body, face = sleeper(432, 574, 0.92)

    leaves = mid(M.leaf(300, 366, 190, 100, rot=-40) + M.leaf(566, 344, 180, 96, rot=42) +
                 M.leaf(160, 656, 150, 82, rot=-24) + M.leaf(704, 668, 140, 78, rot=26))

    return [canopy, mid([t1, t2]), fine(b1 + b2), leaves, ropes, hammock, net,
            mid(body), fine(face),
            mid(M.tuft(300, 940, 62, 54) + M.tuft(560, 946, 58, 50))]
