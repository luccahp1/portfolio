"""Page 17 -- Whale Song.

The single-subject breather of the sea stretch: one enormous shape, one spout,
three little fish for scale.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, capsule, ink)
import motifs as M
from p16 import fish

TITLE = "Whale Song"
SLUG = "whale-song"


def draw():
    body = mid([blob([(126, 610), (196, 486), (352, 424), (528, 442), (628, 520),
                      (664, 604), (596, 690), (420, 736), (238, 714), (140, 668)],
                     t=0.9)])
    fluke = mid([blob([(628, 560), (724, 452), (744, 512), (700, 574), (742, 640),
                       (720, 700), (620, 640)], t=0.7, sharp=(1, 3, 5))])
    fin = mid([blob([(330, 690), (378, 782), (450, 748), (426, 686)], t=0.85)])
    mouth = fine([curve([(140, 648), (250, 686), (392, 674)], t=0.9)])
    belly = fine([curve([(206, 690), (288, 730), (392, 736)], t=0.9),
                  line(238, 700, 250, 736), line(300, 716, 306, 748),
                  line(360, 720, 362, 750)])
    eye = ink([circle(228, 592, 16)])
    brow = fine([curve([(196, 556), (228, 542), (258, 556)])])

    spout = mid([capsule(300, 424, 296, 360, 18),
                 M.puff(298, 292, 220, 150, bumps=3, seed=1)])
    drops = mid([circle(186, 288, 22), circle(430, 264, 18), circle(146, 372, 15),
                 circle(452, 348, 14)])

    f1, d1, e1 = fish(628, 830, 0.42, flip=True)
    f2, d2, e2 = fish(496, 878, 0.34, flip=True)
    f3, d3, e3 = fish(206, 856, 0.38)

    waves = fine([M.wave_line(120, 730, 942, 16, 4)])

    return [spout, drops, body, fluke, fin, mouth, belly, brow, eye,
            mid(f1), fine(d1), ink(e1), mid(f2), fine(d2), ink(e2),
            mid(f3), fine(d3), ink(e3), waves]
