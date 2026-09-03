"""Page 2 -- Mo Reads the Map.

Second-easiest page: one character on one big leaf, one map. The shell spiral
and the dotted route give a child two "follow the line" invitations.
"""
from inkstyle import mid, fine, at, circle, curve, blob
import motifs as M

TITLE = "Mo Reads the Map"
SLUG = "mo-reads-the-map"


def draw():
    sky = mid([M.cloud(212, 206, 200, 92, bumps=3),
               M.cloud(652, 178, 180, 84, bumps=3, seed=2)])

    big_leaf = mid(M.leaf(422, 744, 600, 300, rot=90, ribs=4))

    mo = at(318, 574, 1.18, M.mo(1.18, flip=True))

    # the map Mo is reading: a tilted sheet with a dotted route and a star
    sheet = blob([(528, 336), (716, 372), (696, 552), (508, 516)], t=0.3)
    route = curve([(556, 480), (604, 404), (656, 444), (664, 392)], t=0.9)
    marks = [M.star(666, 380, 26), circle(556, 484, 13)]

    dew = [circle(232, 700, 24), circle(296, 728, 16), circle(566, 700, 20)]

    return [sky,
            big_leaf,
            mid([sheet]),
            fine([route]),
            mid(marks),
            mo,
            mid(dew),
            mid(M.tuft(184, 892, 78, 66) + M.tuft(616, 896, 70, 60) +
                M.flower(672, 800, 26, stem=76))]
