"""
motifs.py -- the reusable cast and scenery for "The Wander Balloon".

Nothing here is traced from or based on any existing character or artwork.
Every shape is built from the primitives in inkstyle.py, which is what keeps
one visual style running across all 24 interior pages:

  * every face uses simple_face()  -> same eyes, same smile, everywhere
  * every character is drawn in local units and placed with at(), with stroke
    widths pre-divided by the scale so line weight never changes
  * organic outlines come from smooth() point lists, so curves stay flowing
    and closed (no open gaps for color to leak out of)
"""

from inkstyle import (BOLD, MID, FINE, BLACK, n, blob, curve, circle, ellipse,
                      rect, line, poly, path, group, at, smooth, capsule)
import math


def _w(s):
    """Stroke widths compensated for a scale factor."""
    return BOLD / s, MID / s, FINE / s


# --------------------------------------------------------------------------
# the shared face -- used by every creature in the book
# --------------------------------------------------------------------------
def simple_face(dx=45, ey=-15, r=12, smile=None, blush=False, s=1.0):
    """Two round eyes and an optional smile, in local coords around (0,0)."""
    bw, mw, fw = _w(s)
    out = [group([circle(-dx, ey, r), circle(dx, ey, r)], fill=BLACK, stroke="none")]
    if smile:
        cx, cy, sw2, sh = smile
        out.append(group([curve([(cx - sw2, cy), (cx, cy + sh), (cx + sw2, cy)])],
                         stroke_width=n(fw), fill="none"))
    if blush:
        out.append(group([curve([(-dx - 26, ey + 34), (-dx - 20, ey + 40), (-dx - 14, ey + 34)]),
                          curve([(dx + 14, ey + 34), (dx + 20, ey + 40), (dx + 26, ey + 34)])],
                         stroke_width=n(fw), fill="none"))
    return out


# --------------------------------------------------------------------------
# Sorrel -- the fox cub pilot
# --------------------------------------------------------------------------
def sorrel_head(s=1.0, goggles=False, scarf=False):
    """Head in local units: head is ~215 wide, chin at y=105, ear tips y=-165."""
    bw, mw, fw = _w(s)
    head_pts = [(0, -80), (44, -74), (136, -156), (126, -40), (122, 4),
                (104, 54), (62, 92), (0, 108), (-62, 92), (-104, 54),
                (-122, 4), (-126, -40), (-136, -156), (-44, -74)]
    out = []
    out.append(group([blob(head_pts, t=0.85, sharp=(1, 2, 3, 11, 12, 13))],
                     stroke_width=n(bw)))
    # inner ears
    out.append(group([blob([(56, -78), (116, -130), (110, -58)], t=0.6, sharp=(0, 1, 2)),
                      blob([(-56, -78), (-116, -130), (-110, -58)], t=0.6, sharp=(0, 1, 2))],
                     stroke_width=n(fw)))
    # muzzle
    out.append(group([blob([(0, 12), (58, 44), (46, 88), (0, 102), (-46, 88), (-58, 44)],
                           t=0.9)], stroke_width=n(mw)))
    out += simple_face(dx=52, ey=-14, r=14, s=s)
    out.append(group([ellipse(0, 32, 17, 12)], fill=BLACK, stroke="none"))
    out.append(group([line(0, 44, 0, 58),
                      curve([(-28, 62), (-14, 76), (0, 58)]),
                      curve([(0, 58), (14, 76), (28, 62)])],
                     stroke_width=n(fw), fill="none"))
    if goggles:
        out.append(group([
            curve([(-120, -58), (0, -104), (120, -58)]),
            circle(-56, -78, 36), circle(56, -78, 36),
            line(-20, -86, 20, -86)], stroke_width=n(mw), fill="#ffffff"))
        out.append(group([circle(-56, -78, 21), circle(56, -78, 21)],
                         stroke_width=n(fw), fill="none"))
    if scarf:
        out += sorrel_scarf(s, flick=scarf if scarf in (1, -1) else 1)
    return out


def sorrel_scarf(s=1.0, flick=1):
    """The striped scarf -- Sorrel's signature, sits just under the chin."""
    bw, mw, fw = _w(s)
    band = blob([(-96, 108), (0, 92), (96, 108), (100, 150), (0, 138), (-100, 150)], t=0.8)
    tail = blob([(96 * flick, 120), (150 * flick, 138), (188 * flick, 196),
                 (150 * flick, 214), (128 * flick, 168), (92 * flick, 150)], t=0.8)
    lines = [line(-52, 100, -52, 143), line(0, 94, 0, 139), line(52, 100, 52, 143),
             line(140 * flick, 140, 128 * flick, 178)]
    return [group([tail, band], stroke_width=n(bw)),
            group(lines, stroke_width=n(fw), fill="none")]


def sorrel(s=1.0, pose="wave", goggles=False, flip=False, flick=-1):
    """Full-body Sorrel. Head centre sits at local (0,0); feet near y=430."""
    bw, mw, fw = _w(s)
    parts = []
    if pose == "wave":
        tail = blob([(-58, 318), (-152, 348), (-234, 302), (-264, 214), (-238, 134),
                     (-186, 112), (-170, 186), (-166, 252), (-120, 302), (-66, 302)],
                    t=0.9, sharp=(5,))
        legs = [capsule(-52, 330, -62, 404, 28), capsule(52, 330, 62, 404, 28)]
        feet = [ellipse(-66, 418, 44, 26), ellipse(66, 418, 44, 26)]
        arms = [capsule(66, 190, 190, 92, 27), capsule(-66, 196, -122, 296, 27)]
        paws = [circle(198, 82, 33), circle(-128, 306, 31)]
        body = blob([(0, 116), (92, 172), (108, 272), (88, 348), (0, 372),
                     (-88, 348), (-108, 272), (-92, 172)], t=0.9)
        parts.append(group([tail] + legs + feet + arms + paws + [body],
                           stroke_width=n(bw)))
        parts.append(group([
            curve([(-242, 146), (-206, 182), (-170, 190)]),
            blob([(0, 178), (62, 226), (62, 310), (0, 340), (-62, 310), (-62, 226)], t=0.9)],
            stroke_width=n(fw), fill="none"))
    elif pose == "sit":
        tail = blob([(58, 300), (150, 300), (232, 262), (262, 186), (236, 128),
                     (186, 150), (176, 220), (140, 268), (76, 286)],
                    t=0.9, sharp=(5,))
        body = blob([(0, 116), (98, 176), (112, 280), (86, 352), (0, 372),
                     (-86, 352), (-112, 280), (-98, 176)], t=0.9)
        legs = [capsule(-46, 330, -108, 372, 30), capsule(46, 330, 108, 372, 30)]
        feet = [ellipse(-124, 380, 40, 26), ellipse(124, 380, 40, 26)]
        arms = [capsule(-74, 210, -116, 306, 26), capsule(74, 210, 116, 306, 26)]
        paws = [circle(-120, 318, 30), circle(120, 318, 30)]
        parts.append(group([tail] + legs + feet + arms + paws + [body],
                           stroke_width=n(bw)))
        parts.append(group([
            curve([(238, 138), (206, 174), (180, 208)]),
            blob([(0, 180), (60, 228), (60, 306), (0, 336), (-60, 306), (-60, 228)], t=0.9)],
            stroke_width=n(fw), fill="none"))
    elif pose == "peek":
        # head plus two paws hooked over a rim (basket, wall, boat edge)
        parts.append(group([blob([(-138, 150), (-96, 128), (-58, 150), (-64, 196),
                                  (-134, 196)], t=0.85),
                            blob([(138, 150), (96, 128), (58, 150), (64, 196),
                                  (134, 196)], t=0.85)], stroke_width=n(bw)))
        parts.append(group([line(-118, 158, -118, 186), line(-92, 156, -92, 186),
                            line(118, 158, 118, 186), line(92, 156, 92, 186)],
                           stroke_width=n(fw), fill="none"))
    out = parts + sorrel_head(s=s, goggles=goggles, scarf=flick)
    if flip:
        return [group(out, transform="scale(-1,1)")]
    return out


# --------------------------------------------------------------------------
# Mo -- the snail navigator
# --------------------------------------------------------------------------
def spiral(cx, cy, r0, r1, turns=2.0, start=0.0, steps=64):
    pts = []
    for i in range(steps + 1):
        f = i / float(steps)
        a = start + f * turns * 2 * math.pi
        r = r0 + (r1 - r0) * f
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M" + " L".join("%s,%s" % (n(x), n(y)) for x, y in pts)


def mo(s=1.0, flip=False):
    """Snail in local units: shell centre (0,0), foot base at y=118."""
    bw, mw, fw = _w(s)
    foot = blob([(-56, 62), (-136, 74), (-176, 100), (-150, 118), (120, 118),
                 (150, 96), (110, 66)], t=0.8)
    head = blob([(-150, 30), (-186, 52), (-192, 94), (-150, 112), (-108, 84)], t=0.9)
    shell = circle(0, 0, 96)
    stalks = [curve([(-172, 40), (-190, -14), (-172, -46)]),
              curve([(-140, 24), (-146, -28), (-124, -56)])]
    out = [group([foot, head, shell], stroke_width=n(bw)),
           group(stalks, stroke_width=n(mw), fill="none"),
           group([circle(-172, -58, 20), circle(-122, -68, 20)], stroke_width=n(mw)),
           group([path(spiral(0, 0, 74, 12, turns=1.75, start=-1.9))],
                 stroke_width=n(fw), fill="none"),
           group([circle(-176, -58, 8), circle(-126, -68, 8),
                  ], fill=BLACK, stroke="none"),
           group([curve([(-176, 66), (-164, 78), (-150, 68)])],
                 stroke_width=n(fw), fill="none")]
    if flip:
        return [group(out, transform="scale(-1,1)")]
    return out


# --------------------------------------------------------------------------
# The Wander -- the patchwork balloon
# --------------------------------------------------------------------------
def wander(s=1.0, basket=True, riders=None, patch=False, ropes=True):
    """The Wander -- a patchwork hot-air balloon.

    Local units: crown at y=-360, envelope neck at y=150, basket floor y=470.
    Five gores carry five different colorable patterns (dots, chevrons,
    stars, waves, checks) so a child gets variety inside one object.
    """
    bw, mw, fw = _w(s)
    env = blob([(0, -334), (152, -300), (238, -190), (258, -70), (216, 40),
                (140, 110), (74, 158), (0, 172), (-74, 158), (-140, 110),
                (-216, 40), (-258, -70), (-238, -190), (-152, -300)], t=0.9)
    out = [group([env], stroke_width=n(bw))]

    def gore(x_out, neck_x):
        return curve([(0, -334), (x_out * 0.64, -216), (x_out, -40), (neck_x, 164)], t=0.9)

    out.append(group([gore(-120, -46), gore(120, 46)], stroke_width=n(mw), fill="none"))
    # three panels, three colorable patterns
    out.append(group([circle(-190, -168, 26), circle(-208, -74, 26),
                      circle(-192, 22, 26)], stroke_width=n(fw)))
    out.append(group([curve([(148, -196), (196, -230), (238, -186)]),
                      curve([(154, -96), (204, -130), (244, -86)]),
                      curve([(148, 4), (196, -30), (232, 14)])],
                     stroke_width=n(fw), fill="none"))
    out.append(group([star(0, -238, 40, s=s), star(0, -122, 40, s=s),
                      star(0, -6, 40, s=s), star(0, 92, 28, s=s)],
                     stroke_width=n(fw), fill="none"))
    if patch:
        out.append(group([blob([(150, -282), (218, -250), (196, -178), (128, -206)],
                               t=0.3, sharp=(0, 1, 2, 3))], stroke_width=n(mw)))
        out.append(group([path("M150,-282 L218,-250 L196,-178 L128,-206 Z")],
                         stroke_width=n(fw), fill="none", stroke_dasharray="16 14"))
    if basket:
        if ropes:
            out.append(group([curve([(-74, 160), (-112, 250), (-136, 342)]),
                              curve([(-30, 170), (-46, 256), (-58, 342)]),
                              curve([(30, 170), (46, 256), (58, 342)]),
                              curve([(74, 160), (112, 250), (136, 342)])],
                             stroke_width=n(mw), fill="none"))
        out.append(group([blob([(-142, 340), (142, 340), (128, 436), (112, 500),
                                (-112, 500), (-128, 436)], t=0.35)],
                         stroke_width=n(bw)))
        weave = [line(-138, 396, 138, 396), line(-126, 452, 126, 452)]
        for x in (-70, 0, 70):
            weave.append(line(x, 346, x, 494))
        out.append(group(weave, stroke_width=n(fw), fill="none"))
    if riders:
        out += riders
    return out


# --------------------------------------------------------------------------
# scenery
# --------------------------------------------------------------------------
def star(cx, cy, r, inner=0.45, points=5, rot=-90, s=1.0, **kw):
    pts = []
    for i in range(points * 2):
        a = math.radians(rot + i * 180.0 / points)
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts, **kw)


def _chain(cx, cy, w, h, bumps, seed, k, base):
    """Lay out an overlapping circle chain that fits the given box."""
    shapes = (0.78, 1.0, 0.86, 0.94, 0.72, 0.90)
    f = [shapes[(i + seed) % len(shapes)] for i in range(bumps)]
    fm = max(f)
    span = f[0] + f[-1] + k * sum(f[i] + f[i + 1] for i in range(bumps - 1))
    tall = fm * (2.0 if base == "round" else 1.34)
    scale = min(w / span, h / tall)
    r = [scale * v for v in f]
    xs = [0.0]
    for i in range(bumps - 1):
        xs.append(xs[-1] + (r[i] + r[i + 1]) * k)
    off = cx - (xs[0] - r[0] + xs[-1] + r[-1]) / 2.0
    return [x + off for x in xs], r, cy + (0 if base == "round" else h / 2.0 - scale * fm * 0.34)


def cloud(cx, cy, w, h, bumps=4, seed=0, k=0.72, base="flat", **kw):
    """A real cloud outline: overlapping circles stitched at their
    intersections. base="flat" cuts a straight bottom (sky clouds); base="round"
    closes the underside with arcs too (bushes, canopies, wool, sea foam).

    One puffy vocabulary, reused all through the book -- part of what makes the
    24 pages feel like one hand drew them.
    """
    xs, r, cyc = _chain(cx, cy, w, h, bumps, seed, k, base)
    nb = len(xs)
    dy = 0.0
    if base == "flat":
        dy = min(r) * 0.34

    def cut(i, j, upper=True):
        dx = xs[j] - xs[i]
        a = (dx * dx + r[i] ** 2 - r[j] ** 2) / (2 * dx)
        hh = max(0.0, r[i] ** 2 - a * a) ** 0.5
        return (xs[i] + a, cyc - hh if upper else cyc + hh)

    def ang(i, p):
        return math.degrees(math.atan2(p[1] - cyc, p[0] - xs[i])) % 360

    stops = []  # (circle index, end point)
    start = (xs[0] - (r[0] ** 2 - dy ** 2) ** 0.5, cyc + dy)
    for i in range(nb - 1):
        stops.append((i, cut(i, i + 1, True)))
    if base == "round":
        stops.append((nb - 1, (xs[-1] + r[-1], cyc)))
        for i in range(nb - 1, 0, -1):
            stops.append((i, cut(i, i - 1, False)))
        stops.append((0, start))
    else:
        stops.append((nb - 1, (xs[-1] + (r[-1] ** 2 - dy ** 2) ** 0.5, cyc + dy)))

    d = ["M%s,%s" % (n(start[0]), n(start[1]))]
    cur = start
    for i, p in stops:
        sweep = (ang(i, p) - ang(i, cur)) % 360
        d.append("A%s,%s 0 %d 1 %s,%s" % (n(r[i]), n(r[i]), 1 if sweep > 180 else 0,
                                          n(p[0]), n(p[1])))
        cur = p
    d.append("Z")
    return path("".join(d), **kw)


def puff(cx, cy, w, h, bumps=3, seed=0, **kw):
    """Rounder cloud mass -- bush, canopy, wool, foam."""
    return cloud(cx, cy, w, h, bumps=bumps, seed=seed, k=0.52, base="round", **kw)


def hill(x0, x1, y_base, y_top, bumps=2, **kw):
    """Smooth ground mound closed along the base line."""
    pts = [(x0, y_base)]
    span = x1 - x0
    for i in range(bumps):
        f = (i + 0.5) / bumps
        lift = 0 if i % 2 == 0 else (y_base - y_top) * 0.22
        pts.append((x0 + span * f, y_top + lift))
    pts += [(x1, y_base)]
    return blob(pts, t=1.0, sharp=(0, len(pts) - 1), **kw)


def tuft(x, y, w=60, h=54, blades=3):
    """Closed grass blades -- colorable, not just strokes."""
    out = []
    for i in range(blades):
        f = (i - (blades - 1) / 2.0) / max(1.0, (blades - 1) / 2.0)
        tipx, tipy = x + f * w * 0.62, y - h * (1.0 - abs(f) * 0.28)
        out.append(blob([(x + f * w * 0.2 - 9, y), (tipx, tipy),
                         (x + f * w * 0.2 + 9, y)], t=0.9, sharp=(1,)))
    return out


def flower(cx, cy, r=28, petals=5, stem=0):
    out = []
    for i in range(petals):
        a = math.radians(-90 + i * 360.0 / petals)
        out.append(circle(cx + r * 1.30 * math.cos(a), cy + r * 1.30 * math.sin(a), r * 0.70))
    out.append(circle(cx, cy, r * 0.62))
    if stem:
        out.append(curve([(cx, cy + r * 1.5), (cx + 10, cy + r * 1.5 + stem * 0.5),
                          (cx, cy + r * 1.5 + stem)]))
    return out


def leaf(cx, cy, l=90, w=44, rot=0, vein=True, ribs=0):
    out = [blob([(0, -l / 2.0), (w / 2.0, 0), (0, l / 2.0), (-w / 2.0, 0)],
                t=0.95, sharp=(0, 2))]
    if vein:
        out.append(line(0, -l / 2.0 + 10, 0, l / 2.0 - 10))
    for i in range(ribs):
        f = -0.42 + 0.84 * (i / float(max(1, ribs - 1)))
        y = f * l * 0.5
        reach = w * 0.5 * (1 - abs(f) * 1.25)
        out.append(curve([(0, y), (reach * 0.7, y + l * 0.06), (reach, y + l * 0.13)]))
        out.append(curve([(0, y), (-reach * 0.7, y + l * 0.06), (-reach, y + l * 0.13)]))
    return [group(out, transform="translate(%s,%s) rotate(%s)" % (n(cx), n(cy), n(rot)))]


def pine(cx, base_y, w, h, tiers=3):
    """Stacked-triangle conifer, drawn bottom tier first so each tier's white
    fill sits cleanly over the one below."""
    out = [rect(cx - w * 0.11, base_y - h * 0.18, w * 0.22, h * 0.18, r=6)]
    for i in range(tiers):
        f = i / float(tiers)
        base = base_y - h * 0.14 - f * h * 0.30
        tw = w * (1.0 - f * 0.30)
        th = h * 0.34
        out.append(blob([(cx, base - th), (cx + tw / 2.0, base), (cx - tw / 2.0, base)],
                        t=0.35, sharp=(0, 1, 2)))
    return out


def round_tree(cx, base_y, w, h):
    """Trunk plus a puffy canopy that fits the given box."""
    canopy_h = h * 0.76
    out = [rect(cx - w * 0.13, base_y - h * 0.50, w * 0.26, h * 0.50, r=10)]
    out.append(puff(cx, base_y - h + canopy_h * 0.5, w * 0.98, canopy_h, bumps=2, seed=1))
    return out


def bird(cx, cy, w=70):
    return [curve([(cx - w, cy), (cx - w * 0.5, cy - w * 0.42), (cx, cy)]),
            curve([(cx, cy), (cx + w * 0.5, cy - w * 0.42), (cx + w, cy)])]


def bubble_field(spots):
    return [circle(x, y, r) for x, y, r in spots]


def wave_line(x0, x1, y, amp=18, waves=4):
    pts = [(x0, y)]
    span = x1 - x0
    for i in range(waves * 2):
        f = (i + 1) / float(waves * 2)
        pts.append((x0 + span * f, y + (amp if i % 2 == 0 else -amp)))
    return curve(pts, t=0.9)
