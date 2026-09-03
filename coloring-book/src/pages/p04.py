"""Page 4 -- Liftoff Over Thistle Hollow.

The first flying page. Sorrel peeks over the basket rim, which is the pose used
for every in-flight page after this one.
"""
from inkstyle import mid, fine, bold, at, circle, curve, blob, line, group, arc
import motifs as M

TITLE = "Liftoff Over Thistle Hollow"
SLUG = "liftoff-over-thistle-hollow"


def burrow(cx, base, w, h):
    """A round burrow house: dome, arched door, round window, roof stripes."""
    dome = ("M%.0f,%.0f A%.0f,%.0f 0 0 1 %.0f,%.0f Z"
            % (cx - w / 2.0, base, w / 2.0, h, cx + w / 2.0, base))
    door = ("M%.0f,%.0f A%.0f,%.0f 0 0 1 %.0f,%.0f Z"
            % (cx - w * 0.15, base, w * 0.15, h * 0.42, cx + w * 0.15, base))
    win = circle(cx + w * 0.28, base - h * 0.44, w * 0.09)
    stripes = [arc(cx - w * 0.42, base - h * 0.36, cx - w * 0.06, base - h * 0.72,
                   w * 0.62),
               arc(cx + w * 0.10, base - h * 0.74, cx + w * 0.44, base - h * 0.30,
                   w * 0.62)]
    return [dome], [door, win], stripes


def draw():
    sky = mid([M.cloud(214, 236, 190, 88, bumps=3),
               M.cloud(660, 292, 150, 74, bumps=3, seed=2)] + M.bird(232, 420, 58) +
              M.bird(676, 430, 48))

    ground = mid([M.hill(112, 738, 986, 800, bumps=2)])

    houses = []
    for cx, base, w, h in ((216, 862, 190, 150), (420, 902, 170, 132),
                           (626, 856, 200, 158)):
        d, holes, st = burrow(cx, base, w, h)
        houses += [mid([__import__("inkstyle").path(d[0])]),
                   mid([__import__("inkstyle").path(holes[0]), holes[1]]),
                   fine(st)]

    balloon = at(452, 392, 0.58, M.wander(0.58))
    pilot = at(452, 486, 0.58, M.sorrel(0.58, pose="peek", goggles=True))

    return [sky, ground] + houses + [balloon, pilot,
            mid(M.tuft(150, 908, 66, 56) + M.tuft(742 - 60, 930, 62, 52))]
