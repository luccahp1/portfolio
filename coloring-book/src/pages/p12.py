"""Page 12 -- Patch Day.

The balloon is down for repairs, which turns the hero object into a pattern
sampler: four patches, each with a different fill for a child to invent.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, path, capsule, ink)
import motifs as M

TITLE = "Patch Day"
SLUG = "patch-day"


def patch(cx, cy, w, h, rot, kind):
    """A patch with stitch marks and one of four fill motifs."""
    quad = blob([(cx - w / 2.0, cy - h / 2.0), (cx + w / 2.0, cy - h * 0.42),
                 (cx + w * 0.44, cy + h / 2.0), (cx - w * 0.46, cy + h * 0.44)],
                t=0.3, sharp=(0, 1, 2, 3))
    marks = []
    for i in range(4):
        f = -0.3 + 0.2 * i
        marks.append(line(cx + w * f, cy - h * 0.60, cx + w * f, cy - h * 0.40))
        marks.append(line(cx + w * f, cy + h * 0.42, cx + w * f, cy + h * 0.62))
    fill = []
    if kind == "dots":
        for x in (-0.22, 0.10):
            for y in (-0.18, 0.18):
                fill.append(circle(cx + w * x, cy + h * y, 15))
    elif kind == "stripes":
        for f in (-0.24, 0.0, 0.24):
            fill.append(line(cx + w * f - 14, cy - h * 0.28, cx + w * f + 14, cy + h * 0.28))
    elif kind == "star":
        fill.append(M.star(cx, cy, min(w, h) * 0.34))
    else:
        fill.append(curve([(cx - w * 0.30, cy), (cx - w * 0.10, cy - h * 0.22),
                           (cx + w * 0.10, cy), (cx + w * 0.30, cy - h * 0.22)], t=0.9))
    return quad, marks, fill


def draw():
    # a big sweep of balloon fabric laid out on the grass
    fabric = mid([blob([(150, 470), (330, 372), (556, 384), (710, 486), (690, 616),
                        (596, 700), (480, 654), (356, 730), (238, 692), (150, 606)],
                       t=0.9)])
    seams = fine([curve([(258, 402), (300, 552), (272, 700)]),
                  curve([(430, 372), (444, 548), (426, 724)]),
                  curve([(604, 400), (630, 552), (594, 706)])])

    parts = []
    for cx, cy, w, h, rot, kind in ((222, 522, 118, 118, 0, "dots"),
                                    (368, 468, 126, 122, 0, "stripes"),
                                    (536, 512, 124, 120, 0, "star"),
                                    (628, 626, 112, 110, 0, "wave")):
        q, m, f = patch(cx, cy, w, h, rot, kind)
        parts += [mid([q]), fine(m), mid(f)]

    needle = mid([blob([(636, 296), (700, 236), (712, 250), (650, 310)],
                       t=0.2, sharp=(0, 1, 2, 3)), circle(700, 244, 13)])
    thread = fine([curve([(694, 248), (622, 218), (556, 268), (492, 236),
                          (432, 292), (392, 386), (372, 448)], t=0.9)])

    spool = mid([blob([(178, 806), (268, 806), (268, 906), (178, 906)],
                      t=0.15, sharp=(0, 1, 2, 3)),
                 ellipse(223, 806, 45, 18), ellipse(223, 906, 45, 18)])
    spool_lines = fine([line(196, 838, 250, 838), line(196, 872, 250, 872)])

    buttons = mid([circle(360, 872, 34), circle(444, 900, 28), circle(536, 866, 32)])
    holes = ink([circle(350, 864, 6), circle(370, 864, 6), circle(350, 882, 6),
                 circle(370, 882, 6), circle(436, 894, 5), circle(452, 894, 5),
                 circle(436, 908, 5), circle(452, 908, 5), circle(528, 858, 6),
                 circle(546, 858, 6), circle(528, 876, 6), circle(546, 876, 6)])

    mo = at(672, 872, 0.34, M.mo(0.34, flip=True))
    sky = mid(M.bird(232, 262, 52) + M.bird(300, 216, 44))

    return [sky, fabric, seams] + parts + [needle, thread, spool, spool_lines,
            buttons, holes, mo]
