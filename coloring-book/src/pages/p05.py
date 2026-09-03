"""Page 5 -- Cloud Sheep.

The same puff shape that draws the clouds becomes the sheep, so a child sees the
joke in the drawing itself: the clouds have faces.
"""
from inkstyle import mid, fine, bold, at, circle, curve, blob, line, group, capsule
import motifs as M

TITLE = "Cloud Sheep"
SLUG = "cloud-sheep"


def sheep(cx, cy, w, h, seed=0, flip=False):
    """A cloud with a face and four little legs."""
    d = -1 if flip else 1
    hx = cx + d * (w * 0.46)
    body = [M.puff(cx, cy, w, h, bumps=3, seed=seed)]
    legs = [capsule(cx - w * 0.22, cy + h * 0.26, cx - w * 0.25, cy + h * 0.82, 17),
            capsule(cx + w * 0.14, cy + h * 0.26, cx + w * 0.17, cy + h * 0.82, 17)]
    head = [blob([(hx, cy - h * 0.20), (hx + d * w * 0.20, cy - h * 0.06),
                  (hx + d * w * 0.19, cy + h * 0.20), (hx, cy + h * 0.30),
                  (hx - d * w * 0.14, cy + h * 0.12), (hx - d * w * 0.14, cy - h * 0.10)],
                 t=0.9)]
    ears = [blob([(hx - d * w * 0.10, cy - h * 0.14), (hx - d * w * 0.24, cy - h * 0.24),
                  (hx - d * w * 0.12, cy + h * 0.02)], t=0.7)]
    eyes = [circle(hx + d * w * 0.06, cy - h * 0.02, 9),
            circle(hx + d * w * 0.03, cy + h * 0.14, 7)]
    return body + legs, head + ears, eyes


def draw():
    out = []
    for cx, cy, w, h, seed, flip in ((286, 316, 300, 152, 0, False),
                                     (566, 546, 268, 134, 2, True),
                                     (268, 806, 280, 140, 1, False)):
        b, hd, ey = sheep(cx, cy, w, h, seed, flip)
        out += [mid(b), mid(hd), group(ey, fill="#000000", stroke="none")]

    balloon = at(636, 224, 0.26, M.wander(0.26))
    small = mid([M.cloud(186, 552, 150, 66, bumps=3, seed=3),
                 M.cloud(596, 916, 190, 80, bumps=3, seed=1)] +
                M.bird(672, 744, 54) + M.bird(178, 938, 46) + M.bird(430, 690, 46))
    return out[:3] + [balloon] + out[3:] + [small]
