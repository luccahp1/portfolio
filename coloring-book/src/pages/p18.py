"""Page 18 -- Cactus Garden.

Desert stretch opens with four cacti built from three shapes, each with its own
rib pattern -- a pattern-practice page disguised as a landscape.
"""
from inkstyle import (mid, fine, bold, at, circle, ellipse, curve, blob, line,
                      group, poly, capsule, ink)
import motifs as M

TITLE = "Cactus Garden"
SLUG = "cactus-garden"


def saguaro(cx, base, w, h):
    trunk = capsule(cx, base, cx, base - h, w * 0.5)
    arm_l = [capsule(cx - w * 0.10, base - h * 0.52, cx - w * 0.86, base - h * 0.52, w * 0.30),
             capsule(cx - w * 0.86, base - h * 0.52, cx - w * 0.86, base - h * 0.80, w * 0.30),
             circle(cx - w * 0.86, base - h * 0.52, w * 0.30)]
    arm_r = [capsule(cx + w * 0.10, base - h * 0.66, cx + w * 0.80, base - h * 0.66, w * 0.30),
             capsule(cx + w * 0.80, base - h * 0.66, cx + w * 0.80, base - h * 0.88, w * 0.30),
             circle(cx + w * 0.80, base - h * 0.66, w * 0.30)]
    ribs = [line(cx - w * 0.16, base - h * 0.22, cx - w * 0.16, base - h * 0.86),
            line(cx + w * 0.16, base - h * 0.22, cx + w * 0.16, base - h * 0.86)]
    return arm_l + arm_r + [trunk], ribs


def barrel(cx, base, w, h):
    body = blob([(cx, base - h), (cx + w * 0.5, base - h * 0.56), (cx + w * 0.44, base),
                 (cx - w * 0.44, base), (cx - w * 0.5, base - h * 0.56)], t=0.9)
    ribs = [curve([(cx - w * 0.26, base - h * 0.86), (cx - w * 0.32, base - h * 0.4),
                   (cx - w * 0.26, base - h * 0.06)]),
            curve([(cx, base - h * 0.92), (cx, base - h * 0.06)]),
            curve([(cx + w * 0.26, base - h * 0.86), (cx + w * 0.32, base - h * 0.4),
                   (cx + w * 0.26, base - h * 0.06)])]
    return [body], ribs


def prickly(cx, base, w, h):
    pads = [blob([(cx, base), (cx + w * 0.42, base - h * 0.30), (cx + w * 0.34, base - h * 0.72),
                  (cx - w * 0.06, base - h * 0.86), (cx - w * 0.40, base - h * 0.58),
                  (cx - w * 0.38, base - h * 0.16)], t=0.9),
            blob([(cx + w * 0.30, base - h * 0.60), (cx + w * 0.78, base - h * 0.74),
                  (cx + w * 0.84, base - h * 1.10), (cx + w * 0.46, base - h * 1.24),
                  (cx + w * 0.22, base - h * 0.94)], t=0.9)]
    dots = []
    for x, y in ((-0.16, -0.30), (0.08, -0.52), (-0.20, -0.62), (0.14, -0.20),
                 (0.44, -0.82), (0.62, -1.02), (0.40, -1.08)):
        dots.append(circle(cx + w * x, base + h * y, 8))
    return pads, dots


def lizard(cx, cy, s=1.0, flip=False):
    d = -1 if flip else 1

    def P(x, y):
        return (cx + d * x * s, cy + y * s)

    body = blob([P(-56, -24), P(40, -34), P(104, -12), P(96, 24), P(20, 34),
                 P(-52, 22)], t=0.9)
    tail = blob([P(-56, -18), P(-130, -2), P(-170, -40), P(-146, -72),
                 P(-124, -46), P(-108, -18), P(-54, 18)], t=0.9, sharp=(3,))
    head = blob([P(96, -30), P(154, -22), P(158, 16), P(100, 26)], t=0.9)
    legs = [capsule(*P(52, 22), *P(74, 62), 11 * s), capsule(*P(-24, 20), *P(-48, 58), 11 * s),
            capsule(*P(40, -30), *P(58, -66), 11 * s), capsule(*P(-30, -30), *P(-54, -62), 11 * s)]
    feet = [circle(*P(78, 68), 13 * s), circle(*P(-52, 64), 13 * s),
            circle(*P(62, -72), 13 * s), circle(*P(-58, -68), 13 * s)]
    stripes = [line(*P(-10, -28), *P(-14, 28)), line(*P(28, -32), *P(24, 32)),
               line(*P(66, -26), *P(64, 28))]
    eye = [circle(*P(132, -8), 9 * s)]
    return legs + feet + [tail, body, head], stripes, eye


def draw():
    SX, SY = 606, 268
    sun = mid([circle(SX, SY, 76)])
    rays = mid([poly([(SX + dx, SY + dy), (SX + dx * 1.62, SY + dy * 1.62),
                      (SX + dx * 0.72 - dy * 0.46, SY + dy * 0.72 + dx * 0.46)])
                for dx, dy in ((0, -84), (59, -59), (84, 0), (59, 59), (0, 84), (-59, 59),
                               (-84, 0), (-59, -59))])

    dunes = mid([M.hill(112, 738, 982, 806, bumps=2)])

    s1, sr1 = saguaro(286, 812, 130, 462)
    b1, br1 = barrel(464, 858, 170, 150)
    p1, pd1 = prickly(596, 872, 170, 200)

    blooms = mid(M.flower(266, 322, 24) + M.flower(464, 682, 22))

    lz, lzs, lze = lizard(278, 910, 0.92)

    return [sun, rays, dunes, mid(s1), fine(sr1), mid(b1), fine(br1),
            mid(p1), mid(pd1), blooms, mid(lz), fine(lzs), ink(lze),
            mid(M.tuft(704, 934, 60, 52))]
