"""Page 11 -- Rain Hats and Puddles.

A rest page. One huge umbrella, fat drops, two boots, three puddle rings --
nothing on this page needs a small hand to be steady.
"""
from inkstyle import mid, fine, at, circle, ellipse, curve, blob, line, path, poly
import motifs as M

TITLE = "Rain Hats and Puddles"
SLUG = "rain-hats-and-puddles"


def umbrella(cx, cy, w, h, scallops=5):
    """Dome canopy with a scalloped hem, ribs, a knob and a hooked handle."""
    r = w / (2.0 * scallops)
    d = ["M%.1f,%.1f" % (cx - w / 2.0, cy)]
    d.append("A%.1f,%.1f 0 0 1 %.1f,%.1f" % (w / 2.0, h, cx + w / 2.0, cy))
    for i in range(scallops):
        x = cx + w / 2.0 - 2 * r * (i + 1)
        d.append("A%.1f,%.1f 0 0 1 %.1f,%.1f" % (r, r * 0.72, x, cy))
    d.append("Z")
    ribs = []
    for i in range(1, scallops):
        x = cx - w / 2.0 + 2 * r * i
        ribs.append(curve([(cx, cy - h), (x + (cx - x) * 0.30, cy - h * 0.46), (x, cy)]))
    knob = circle(cx, cy - h - 16, 18)
    handle = [curve([(cx + 4, cy + h * 1.52), (cx - 44, cy + h * 1.76),
                     (cx - 68, cy + h * 1.34)])]
    return d, ribs, knob, handle


def drop(cx, cy, s=1.0):
    return blob([(cx, cy - 44 * s), (cx + 26 * s, cy + 6 * s), (cx, cy + 40 * s),
                 (cx - 26 * s, cy + 6 * s)], t=0.9, sharp=(0,))


def draw():
    d, ribs, knob, handle = umbrella(352, 462, 440, 200)
    canopy = mid([path("".join(d)), knob])
    stick = mid([__import__("inkstyle").capsule(352, 286, 358, 792, 13)])
    hook = mid(handle)

    drops = mid([drop(178, 296, 1.0), drop(646, 300, 1.1), drop(146, 552, 0.9),
                 drop(690, 486, 1.0), drop(226, 716, 0.85), drop(676, 668, 0.9),
                 drop(596, 400, 0.8)])

    boots = []
    for bx in (516, 636):
        boots.append(blob([(bx - 44, 792), (bx + 34, 792), (bx + 38, 872),
                           (bx + 70, 886), (bx + 66, 926), (bx - 46, 926),
                           (bx - 50, 860)], t=0.35, sharp=(0, 1, 2, 3, 4, 5, 6)))
    boot_lines = fine([line(472, 830, 554, 830), line(592, 830, 674, 830)])

    puddles = mid([ellipse(232, 924, 100, 32), ellipse(566, 946, 118, 30)])
    rings = fine([ellipse(232, 924, 56, 16), ellipse(566, 946, 66, 16)])

    mo = at(238, 812, 0.30, M.mo(0.30, flip=True))

    return [drops, stick, hook, canopy, mid(ribs), mo, mid(boots), boot_lines,
            puddles, rings]
