"""Page 6 -- Kite Weather.

A deliberate breather after the busier liftoff pages: four big shapes, four
long tails, nothing small.
"""
import math
from inkstyle import mid, fine, at, circle, curve, blob, line, poly, group
import motifs as M

TITLE = "Kite Weather"
SLUG = "kite-weather"


def kite(cx, cy, w, h, rot, tail):
    """Diamond kite with cross spars and a bowed tail."""
    body = poly([(cx, cy - h / 2.0), (cx + w / 2.0, cy), (cx, cy + h / 2.0),
                 (cx - w / 2.0, cy)])
    spars = [line(cx, cy - h / 2.0, cx, cy + h / 2.0),
             line(cx - w / 2.0, cy, cx + w / 2.0, cy),
             circle(cx, cy, w * 0.11)]
    string = curve(tail)
    bows = []
    seg = [math.hypot(tail[i + 1][0] - tail[i][0], tail[i + 1][1] - tail[i][1])
           for i in range(len(tail) - 1)]
    total = sum(seg) or 1.0
    spots = (0.55,) if total < 170 else ((0.40, 0.88) if total < 300 else (0.28, 0.60, 0.92))
    for f in spots:
        want, j = f * total, 0
        while j < len(seg) - 1 and want > seg[j]:
            want -= seg[j]
            j += 1
        t = want / seg[j]
        bx = tail[j][0] + (tail[j + 1][0] - tail[j][0]) * t
        by = tail[j][1] + (tail[j + 1][1] - tail[j][1]) * t
        bows.append(poly([(bx - 30, by - 22), (bx, by), (bx - 30, by + 22)]))
        bows.append(poly([(bx + 30, by - 22), (bx, by), (bx + 30, by + 22)]))
    g = "rotate(%d %d %d)" % (rot, cx, cy)
    return group([body], transform=g), group(spars, transform=g, fill="none"), [string], bows


def draw():
    out = []
    kites = ((266, 292, 224, 274, -12, [(266, 436), (238, 552), (296, 648), (256, 742)]),
             (606, 396, 196, 240, 14, [(606, 524), (642, 630), (586, 722), (622, 812)]),
             (248, 772, 178, 214, 10, [(248, 886), (216, 948)]),
             (608, 812, 152, 184, -10, [(608, 908), (582, 954)]))
    for cx, cy, w, h, rot, tail in kites:
        body, spars, string, bows = kite(cx, cy, w, h, rot, tail)
        out += [mid([body]), fine([spars]), fine(string), mid(bows)]

    sky = mid([M.cloud(432, 210, 180, 82, bumps=3, seed=2)] +
              M.bird(420, 560, 60) + M.bird(480, 616, 48) + M.bird(392, 640, 44))
    return [sky] + out
