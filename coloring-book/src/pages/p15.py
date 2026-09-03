"""Page 15 -- Turtle Ferry.

Three shells, three sets of plates: the page where a child can invent a pattern
and then repeat it twice more.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, capsule, ink)
import motifs as M

TITLE = "Turtle Ferry"
SLUG = "turtle-ferry"


def turtle(cx, cy, s=1.0, flip=False):
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    shell = blob([P(-130, 20), P(-104, -66), P(0, -104), P(104, -66), P(130, 20)],
                 t=0.85, sharp=(0, 4))
    rim = blob([P(-146, 18), P(0, -14), P(146, 18), P(120, 58), P(0, 76), P(-120, 58)],
               t=0.85)
    plates = [curve([P(-64, -60), P(-72, 4)]), curve([P(0, -96), P(0, -10)]),
              curve([P(64, -60), P(72, 4)]),
              curve([P(-96, -34), P(0, -52), P(96, -34)], t=0.9)]
    head = blob([P(140, -22), P(196, -34), P(216, 8), P(178, 36), P(138, 22)], t=0.9)
    flip1 = blob([P(-104, 44), P(-172, 74), P(-146, 108), P(-88, 76)], t=0.85)
    flip2 = blob([P(96, 48), P(166, 76), P(140, 110), P(84, 80)], t=0.85)
    eye = [circle(*P(186, -8), 10 * s)]
    smile = curve([P(196, 16), P(206, 22), P(212, 14)])
    return [flip1, flip2, head, rim, shell], plates + [smile], eye


def pad(cx, cy, r):
    """Lily pad: a full round leaf with a wedge notch cut out of one side."""
    import math
    a0, a1 = math.radians(-28), math.radians(28)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    notch = __import__("inkstyle").path(
        "M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f Z"
        % (cx, cy, x0, y0, r, r, x1, y1))
    veins = []
    for k in range(5):
        a = math.radians(52 + k * 64)
        veins.append(line(cx + r * 0.12 * math.cos(a), cy + r * 0.12 * math.sin(a),
                          cx + r * 0.82 * math.cos(a), cy + r * 0.82 * math.sin(a)))
    return notch, veins


def draw():
    water = fine([M.wave_line(120, 730, 300, 16, 4), M.wave_line(120, 730, 940, 18, 4)])

    p1, v1 = pad(212, 420, 104)
    p2, v2 = pad(624, 640, 96)
    p3, v3 = pad(266, 880, 90)

    t1, l1, e1 = turtle(452, 356, 0.72)
    t2, l2, e2 = turtle(330, 620, 0.86, flip=True)
    t3, l3, e3 = turtle(590, 848, 0.66)

    mo = at(330, 566, 0.30, M.mo(0.30))

    ripples = fine([M.wave_line(160, 420, 560, 12, 3),
                    M.wave_line(470, 700, 760, 12, 3)])

    return [water, ripples, mid([p1, p2, p3]), fine(v1 + v2 + v3),
            mid(t1), fine(l1), ink(e1), mo,
            mid(t2), fine(l2), ink(e2),
            mid(t3), fine(l3), ink(e3)]
