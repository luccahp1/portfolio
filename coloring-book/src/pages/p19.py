"""Page 19 -- Dune Sled.

Long curved dunes give the eye somewhere to travel, and the sled is a leaf --
the same leaf shape Mo rides on page 2.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M

TITLE = "Dune Sled"
SLUG = "dune-sled"


def jerboa(cx, cy, s=1.0, flip=False):
    """Long-eared desert hopper with a tufted tail."""
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    tail = blob([P(-64, -6), P(-150, -40), P(-206, -104), P(-176, -128),
                 P(-136, -70), P(-58, -34)], t=0.9)
    tuft = M.puff(*P(-196, -140), 96 * s, 74 * s, bumps=3, seed=2)
    body = blob([P(-10, -84), P(56, -54), P(70, 16), P(6, 52), P(-58, 26),
                 P(-64, -40)], t=0.9)
    head = blob([P(40, -110), P(104, -96), P(116, -34), P(64, -10), P(20, -38)], t=0.9)
    ears = [blob([P(44, -104), P(20, -196), P(66, -206), P(80, -116)], t=0.85),
            blob([P(86, -100), P(88, -196), P(130, -182), P(120, -104)], t=0.85)]
    legs = [capsule(*P(20, 34), *P(46, 74), 15 * s), capsule(*P(-26, 30), *P(-14, 74), 15 * s)]
    feet = [ellipse(*P(56, 82), 34 * s, 16 * s), ellipse(*P(-6, 82), 34 * s, 16 * s)]
    arm = capsule(*P(52, -22), *P(96, 6), 12 * s)
    eyes = [circle(*P(84, -62), 13 * s)]
    nose = ellipse(*P(116, -40), 11 * s, 8 * s)
    smile = curve([P(96, -22), P(106, -14), P(116, -24)])
    return [tuft, tail] + ears + legs + feet + [arm, body, head, nose], [smile], eyes


def draw():
    sun = mid([circle(626, 236, 66)])
    balloon = at(240, 300, 0.22, M.wander(0.22))

    dune_a = mid([blob([(112, 706), (232, 620), (348, 578), (486, 616), (600, 556),
                        (738, 528), (738, 744), (112, 786)], t=0.95, sharp=(0, 5, 6, 7))])
    dune_b = mid([blob([(112, 864), (260, 806), (400, 788), (560, 820), (664, 776),
                        (738, 750), (738, 958), (112, 964)], t=0.95, sharp=(0, 5, 6, 7))])
    ripples = fine([curve([(200, 900), (256, 916), (312, 896)]),
                    curve([(430, 930), (486, 946), (542, 926)]),
                    curve([(596, 872), (648, 888), (700, 868)])])

    sled = mid([blob([(258, 686), (420, 646), (486, 668), (438, 726), (280, 736)],
                     t=0.9, sharp=(2,))])
    sled_vein = fine([curve([(276, 706), (368, 682), (462, 678)], t=0.9)])

    j, jl, je = jerboa(340, 578, 0.94)

    cacti = mid([capsule(688, 640, 688, 528, 30), capsule(686, 592, 726, 592, 20),
                 capsule(152, 626, 152, 546, 26)])

    return [sun, balloon, dune_a, dune_b, ripples, cacti, sled, sled_vein,
            mid(j), fine(jl), ink(je)]
