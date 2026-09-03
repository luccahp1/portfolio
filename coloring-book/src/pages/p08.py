"""Page 8 -- Waterfall Steps.

A gorge read head-on: rock on both sides, water down the middle, pool at the
bottom. The water is one closed band, so it colors as a single stroke of blue.
"""
from inkstyle import mid, fine, at, circle, curve, blob, line
import motifs as M

TITLE = "Waterfall Steps"
SLUG = "waterfall-steps"


def fern(cx, base, h, lean=1, pairs=3):
    out = [curve([(cx, base), (cx + lean * h * 0.16, base - h * 0.52),
                  (cx + lean * h * 0.30, base - h)])]
    for i in range(pairs):
        f = 0.34 + 0.58 * i / float(pairs - 1)
        x = cx + lean * h * (0.10 * f + 0.24 * f * f)
        y = base - h * f
        L = h * 0.38 * (1.05 - f * 0.5)
        out += M.leaf(x - lean * L * 0.5, y - L * 0.16, L, L * 0.5, -62 * lean, vein=False)
        out += M.leaf(x + lean * L * 0.5, y - L * 0.06, L, L * 0.5, 62 * lean, vein=False)
    return out


def draw():
    water = mid([blob([(348, 168), (508, 168), (528, 340), (498, 500), (526, 660),
                       (546, 812), (318, 816), (338, 660), (312, 500), (330, 340)],
                      t=0.95)])
    crest = fine([curve([(340, 250), (426, 286), (516, 246)])])
    ripple = fine([curve([(346, 400), (420, 438), (496, 396)]),
                   curve([(340, 566), (424, 604), (508, 562)]),
                   curve([(342, 716), (428, 754), (520, 712)])])

    rock_l = mid([blob([(128, 170), (292, 158), (348, 268), (316, 398), (352, 536),
                        (306, 664), (196, 700), (130, 650)], t=0.7, sharp=(0, 7))])
    rock_r = mid([blob([(722, 168), (720, 620), (646, 674), (538, 636), (522, 512),
                        (556, 372), (510, 246), (558, 164)], t=0.7, sharp=(0, 1))])
    seams = fine([curve([(158, 318), (222, 336), (288, 312)]),
                  curve([(160, 470), (226, 488), (292, 462)]),
                  curve([(160, 596), (222, 614), (286, 590)]),
                  curve([(596, 320), (656, 338), (712, 314)]),
                  curve([(590, 470), (652, 488), (708, 462)]),
                  curve([(596, 588), (656, 606), (710, 582)])])

    pool = mid([blob([(178, 856), (430, 812), (686, 850), (712, 918), (444, 964),
                      (166, 922)], t=0.9)])
    foam = mid([circle(376, 848, 32), circle(462, 826, 26), circle(548, 852, 30),
                circle(286, 872, 22)])

    stones = mid([blob([(232, 856), (322, 846), (338, 906), (246, 918)], t=0.7),
                  blob([(566, 862), (652, 852), (666, 908), (580, 920)], t=0.7)])
    mo = at(284, 828, 0.28, M.mo(0.28, flip=True))

    ferns = mid(fern(176, 676, 210, 1) + fern(688, 672, 178, -1))

    return [water, crest, ripple, rock_l, rock_r, seams, pool, foam, stones, mo, ferns]
