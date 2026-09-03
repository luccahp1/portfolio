"""Page 22 -- The Sky Fox.

A constellation of Sorrel. Big stars joined by thin lines: the child colors the
stars and the fox appears out of the joins. No numbers, no letters -- the shape
does the work.
"""
from inkstyle import mid, fine, at, circle, line, group
import motifs as M

TITLE = "The Sky Fox"
SLUG = "the-sky-fox"

# the outline of the constellation, walked in order
# a fox's head: two ear tips, cheeks, jaw and chin, walked as a closed loop
FOX = [(256, 268), (346, 372), (424, 336), (502, 372), (592, 268), (628, 470),
       (566, 618), (424, 706), (282, 618), (220, 470)]
SIZES = [36, 22, 26, 22, 36, 26, 24, 32, 24, 26]
FACE = [(356, 462, 26), (492, 462, 26), (424, 566, 30)]


def draw():
    joins = fine([line(FOX[i][0], FOX[i][1], FOX[(i + 1) % len(FOX)][0],
                       FOX[(i + 1) % len(FOX)][1]) for i in range(len(FOX))])
    stars = mid([M.star(x, y, r) for (x, y), r in zip(FOX, SIZES)])

    face = mid([M.star(x, y, r) for x, y, r in FACE])
    grin = fine([line(356, 500, 424, 540), line(492, 500, 424, 540)])

    loose = mid([M.star(160, 738, 24), M.star(690, 726, 26), M.star(432, 852, 30),
                 M.star(268, 894, 22), M.star(604, 900, 24), M.star(150, 210, 20),
                 M.star(704, 196, 22)])
    sparkles = fine([line(196, 806, 196, 852), line(174, 828, 218, 828),
                     line(660, 812, 660, 856), line(638, 834, 682, 834),
                     line(534, 782, 534, 822), line(514, 802, 554, 802)])

    return [joins, stars, grin, face, loose, sparkles]
