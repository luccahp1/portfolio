"""Page 9 -- Pine Ridge Picnic.

Both characters together on the ground. The blanket's grid is the page's pattern
workout -- big cells only, nothing a crayon can miss.
"""
from inkstyle import mid, fine, bold, at, circle, curve, blob, line, group, poly, rect
import motifs as M

TITLE = "Pine Ridge Picnic"
SLUG = "pine-ridge-picnic"


def blanket(x0, y0, x1, y1, cols=3, rows=2):
    """Soft-edged blanket with a big-cell check pattern."""
    w, h = x1 - x0, y1 - y0
    quad = blob([(x0 + 10, y0), (x0 + w * 0.5, y0 - 12), (x1 - 10, y0),
                 (x1 + 10, y0 + h * 0.5), (x1 - 10, y1), (x0 + w * 0.5, y1 + 12),
                 (x0 + 10, y1), (x0 - 10, y0 + h * 0.5)], t=0.55)
    lines = []
    for i in range(1, cols):
        f = i / float(cols)
        lines.append(line(x0 + w * f, y0 + 4, x0 + w * f, y1 - 4))
    for j in range(1, rows):
        g = j / float(rows)
        lines.append(line(x0 + 6, y0 + h * g, x1 - 6, y0 + h * g))
    return quad, lines


def hamper(cx, cy, w, h):
    box = blob([(cx - w / 2.0, cy - h / 2.0), (cx + w / 2.0, cy - h / 2.0),
                (cx + w * 0.42, cy + h / 2.0), (cx - w * 0.42, cy + h / 2.0)],
               t=0.2, sharp=(0, 1, 2, 3))
    handle = curve([(cx - w * 0.30, cy - h * 0.44), (cx - w * 0.24, cy - h * 0.94),
                    (cx, cy - h * 1.04), (cx + w * 0.24, cy - h * 0.94),
                    (cx + w * 0.30, cy - h * 0.44)], t=0.8)
    weave = [line(cx - w * 0.46, cy, cx + w * 0.46, cy)]
    for f in (-0.24, 0.06, 0.36):
        weave.append(line(cx + w * f, cy - h * 0.46, cx + w * f, cy + h * 0.46))
    return box, handle, weave


def draw():
    trees = mid(M.pine(200, 748, 170, 344) + M.pine(338, 712, 132, 250) +
                M.pine(658, 744, 164, 326))
    sky = mid([M.cloud(492, 210, 200, 92, bumps=3),
               M.cloud(206, 296, 156, 72, bumps=3, seed=2)] +
              M.bird(346, 226, 54) + M.bird(646, 300, 46))

    ground = mid([M.hill(112, 738, 980, 786, bumps=2)])

    quad, grid = blanket(212, 800, 654, 940)
    box, handle, weave = hamper(578, 776, 146, 120)

    food = mid([circle(392, 892, 32), circle(468, 916, 26), circle(330, 918, 24)])

    sorrel = at(300, 684, 0.46, M.sorrel(0.46, pose="sit"))
    mo = at(636, 906, 0.30, M.mo(0.30, flip=True))

    return [sky, trees, ground, mid([quad]), fine(grid),
            mid([box]), fine([handle] + weave), food, sorrel, mo,
            mid(M.tuft(158, 876, 62, 54) + M.tuft(706, 880, 58, 50))]
