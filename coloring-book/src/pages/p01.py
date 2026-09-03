"""Page 1 -- Sorrel Says Hello.

The easiest page in the book on purpose: one large character, three big
flowers, two clouds. Nothing here is narrower than a crayon tip.
"""
from inkstyle import bold, mid, fine, at, group
import motifs as M

TITLE = "Sorrel Says Hello"
SLUG = "sorrel-says-hello"


def draw():
    sky = mid([M.cloud(230, 220, 250, 110, bumps=4),
               M.cloud(620, 175, 190, 90, bumps=3, seed=2)])

    ground = mid([M.hill(106, 744, 992, 838, bumps=3)])

    blooms = mid(M.flower(184, 828, 26, stem=56) +
                 M.flower(660, 638, 38, stem=204) +
                 M.flower(624, 796, 28, stem=84) +
                 M.tuft(286, 866, 74, 66) + M.tuft(556, 876, 66, 58) +
                 M.tuft(146, 884, 60, 52))

    hero = at(424, 424, 0.94, M.sorrel(0.94, pose="wave", goggles=True))

    return [sky, ground, blooms, hero]
