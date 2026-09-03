"""Page 10 -- Nib's Berry Cart.

A new friend on the ground. The berries are the reward: a dozen big circles a
child can go at with a different color each.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, capsule, ink, poly)
import motifs as M

TITLE = "Nib's Berry Cart"
SLUG = "nibs-berry-cart"


def hedgehog(cx, cy, s=1.0, flip=False):
    """Round hedgehog: soft face, spiny back drawn as one zigzag shape."""
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    face = blob([P(-118, -4), P(-92, -54), P(-30, -76), P(26, -54), P(34, 26),
                 P(-24, 62), P(-92, 46)], t=0.9)
    spikes = [P(-72, -28)]
    for i in range(9):
        f = i / 8.0
        spikes.append(P(-58 + 192 * f, -96 + 56 * f + (0 if i % 2 == 0 else 36)))
    spikes += [P(134, 40), P(62, 80), P(-24, 74), P(-60, 42)]
    back = blob(spikes, t=0.35, sharp=tuple(range(1, 10)))
    legs = [capsule(*P(-46, 52), *P(-52, 92), 15 * s),
            capsule(*P(30, 52), *P(36, 92), 15 * s)]
    feet = [ellipse(*P(-56, 100), 26 * s, 15 * s), ellipse(*P(40, 100), 26 * s, 15 * s)]
    snout = ellipse(*P(-116, -6), 15 * s, 12 * s)
    eyes = [circle(*P(-62, -34), 11 * s)]
    ear = blob([P(-30, -62), P(-4, -78), P(6, -50)], t=0.8)
    smile = curve([P(-96, 6), P(-84, 16), P(-70, 6)])
    return [ear] + legs + feet + [back, face, snout], [smile], eyes


def cart(cx, cy, w, h):
    box = blob([(cx - w / 2.0, cy - h / 2.0), (cx + w / 2.0, cy - h / 2.0),
                (cx + w * 0.40, cy + h / 2.0), (cx - w * 0.40, cy + h / 2.0)],
               t=0.2, sharp=(0, 1, 2, 3))
    slats = [line(cx - w * 0.46, cy, cx + w * 0.46, cy)]
    for f in (-0.22, 0.10):
        slats.append(line(cx + w * f, cy - h * 0.46, cx + w * f, cy + h * 0.46))
    wheels = [circle(cx - w * 0.22, cy + h * 0.62, 44), circle(cx + w * 0.24, cy + h * 0.62, 44)]
    hubs = [circle(cx - w * 0.22, cy + h * 0.62, 15), circle(cx + w * 0.24, cy + h * 0.62, 15)]
    handle = capsule(cx - w * 0.48, cy - h * 0.30, cx - w * 0.86, cy - h * 0.62, 12)
    return wheels + [box, handle], slats + hubs


def draw():
    sky = mid([M.cloud(232, 226, 190, 88, bumps=3),
               M.cloud(596, 296, 150, 70, bumps=3, seed=2)] +
              M.bird(392, 268, 52) + M.bird(462, 320, 44))
    ground = mid([M.hill(114, 736, 980, 806, bumps=3)])
    bush = mid(M.pine(678, 796, 112, 240) + [M.puff(184, 736, 140, 116, bumps=3, seed=1)])

    cshapes, cdetail = cart(540, 768, 262, 168)
    berries = mid([circle(x, y, r) for x, y, r in
                   ((462, 662, 36), (540, 636, 40), (618, 662, 36),
                    (498, 702, 32), (580, 702, 32), (638, 714, 26))])
    stems = fine([curve([(462, 626), (454, 600), (432, 590)]),
                  curve([(540, 596), (542, 570), (564, 560)])])

    h, hl, he = hedgehog(272, 744, 1.12)

    balloon = at(316, 388, 0.22, M.wander(0.22))

    return [sky, balloon, ground, bush, mid(cshapes), fine(cdetail), berries, stems,
            mid(h), fine(hl), ink(he),
            mid(M.tuft(158, 902, 66, 56) + M.tuft(408, 916, 60, 52) +
                M.tuft(700, 900, 58, 50))]
