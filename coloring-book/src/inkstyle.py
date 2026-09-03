"""
inkstyle.py -- the house style for "The Wander Balloon" coloring book.

Every page in this book is drawn with these primitives so that line weight,
corner treatment, page size and safe margins stay identical across all 24
interior pages.

Page geometry
-------------
  Trim        8.5 x 11 in  (portrait)
  User unit   1/100 in  ->  viewBox "0 0 850 1100"
  Safe area   1.00 in all round -> x 100..750, y 100..1000

Line weights (in user units; 100 units = 1 inch)
-----------------------------------------------
  BOLD 11  (~2.8 mm) hero silhouettes, the outermost outline of any subject
  MID   8  (~2.0 mm) secondary objects, mid-ground shapes
  FINE  6  (~1.5 mm) interior detail, pattern lines, texture
  Solid black is used ONLY for eyes / noses / tiny accents. No gray anywhere.

Colorable-gap rule: no two lines closer than ~20 units (0.2 in / 5 mm) so a
fat crayon can still land inside every shape.
"""

W, H = 850, 1100
MARGIN = 100
LEFT, RIGHT, TOP, BOTTOM = MARGIN, W - MARGIN, MARGIN, H - MARGIN
CX = W / 2.0

BOLD, MID, FINE = 11.0, 8.0, 6.0
WHITE, BLACK = "#ffffff", "#000000"


def n(v):
    """Compact number formatting so the SVG stays readable."""
    return ("%.2f" % v).rstrip("0").rstrip(".")


# --------------------------------------------------------------------------
# paths
# --------------------------------------------------------------------------
def smooth(pts, closed=True, t=1.0, sharp=()):
    """Catmull-Rom through `pts` as cubic beziers.

    Indices listed in `sharp` keep a hard corner (zero-length handles), which
    is how ears, beaks, leaf tips and star points stay pointy.
    """
    pts = [(float(x), float(y)) for x, y in pts]
    m = len(pts)
    sharp = set(i % m for i in sharp)

    def P(i):
        if closed:
            return pts[i % m]
        return pts[max(0, min(m - 1, i))]

    d = ["M%s,%s" % (n(pts[0][0]), n(pts[0][1]))]
    segs = m if closed else m - 1
    for i in range(segs):
        p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
        if i % m in sharp:
            c1 = p1
        else:
            c1 = (p1[0] + (p2[0] - p0[0]) * t / 6.0, p1[1] + (p2[1] - p0[1]) * t / 6.0)
        if (i + 1) % m in sharp:
            c2 = p2
        else:
            c2 = (p2[0] - (p3[0] - p1[0]) * t / 6.0, p2[1] - (p3[1] - p1[1]) * t / 6.0)
        d.append("C%s,%s %s,%s %s,%s" % (n(c1[0]), n(c1[1]), n(c2[0]), n(c2[1]),
                                         n(p2[0]), n(p2[1])))
    if closed:
        d.append("Z")
    return "".join(d)


def path(d, **kw):
    return tag("path", d=d, **kw)


def blob(pts, **kw):
    """Closed organic shape through the given points."""
    return path(smooth(pts, closed=True, **{k: v for k, v in kw.items()
                                            if k in ("t", "sharp")}),
                **{k: v for k, v in kw.items() if k not in ("t", "sharp")})


def curve(pts, **kw):
    """Open flowing line through the given points."""
    return path(smooth(pts, closed=False, **{k: v for k, v in kw.items()
                                             if k in ("t", "sharp")}),
                **{k: v for k, v in kw.items() if k not in ("t", "sharp")})


def tag(name, **attrs):
    body = attrs.pop("_body", None)
    parts = []
    for k, v in attrs.items():
        if v is None:
            continue
        parts.append('%s="%s"' % (k.replace("_", "-"), v))
    open_tag = "<%s %s" % (name, " ".join(parts))
    if body is None:
        return open_tag + "/>"
    return open_tag + ">" + body + "</%s>" % name


# --------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------
def circle(cx, cy, r, **kw):
    return tag("circle", cx=n(cx), cy=n(cy), r=n(r), **kw)


def ellipse(cx, cy, rx, ry, rot=0, **kw):
    if rot:
        kw["transform"] = "rotate(%s %s %s)" % (n(rot), n(cx), n(cy))
    return tag("ellipse", cx=n(cx), cy=n(cy), rx=n(rx), ry=n(ry), **kw)


def rect(x, y, w, h, r=0, **kw):
    return tag("rect", x=n(x), y=n(y), width=n(w), height=n(h),
               rx=(n(r) if r else None), **kw)


def line(x1, y1, x2, y2, **kw):
    return tag("line", x1=n(x1), y1=n(y1), x2=n(x2), y2=n(y2), **kw)


def poly(pts, closed=True, **kw):
    d = "M" + " L".join("%s,%s" % (n(x), n(y)) for x, y in pts) + ("Z" if closed else "")
    return path(d, **kw)


def arc(x1, y1, x2, y2, r, sweep=1, large=0, **kw):
    return path("M%s,%s A%s,%s 0 %d %d %s,%s" % (n(x1), n(y1), n(r), n(r),
                                                 large, sweep, n(x2), n(y2)), **kw)


def capsule(x1, y1, x2, y2, r, **kw):
    """A closed rounded limb between two points -- arms, legs, branches, ropes.
    Pair it with a circle at the far end for a paw or a foot."""
    import math
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    px, py = -uy * r, ux * r
    return path("M%s,%s L%s,%s A%s,%s 0 0 0 %s,%s L%s,%s A%s,%s 0 0 0 %s,%s Z" % (
        n(x1 + px), n(y1 + py), n(x2 + px), n(y2 + py), n(r), n(r),
        n(x2 - px), n(y2 - py), n(x1 - px), n(y1 - py), n(r), n(r),
        n(x1 + px), n(y1 + py)), **kw)


def group(children, **attrs):
    if isinstance(children, (list, tuple)):
        children = "\n    ".join(c for c in children if c)
    return tag("g", _body="\n    " + children + "\n  ", **attrs)


def at(x, y, s, children, sw=None):
    """Place a sub-drawing. Stroke widths are pre-divided by `s` by the
    character builders, so scaling never thins a line."""
    tr = "translate(%s,%s)" % (n(x), n(y))
    if s != 1:
        tr += " scale(%s)" % n(s)
    return group(children, transform=tr, stroke_width=(n(sw) if sw else None))


# --------------------------------------------------------------------------
# style layers -- every page is assembled from these four buckets
# --------------------------------------------------------------------------
def bold(children):
    return group(children, stroke_width=n(BOLD))


def mid(children):
    return group(children, stroke_width=n(MID))


def fine(children):
    return group(children, stroke_width=n(FINE), fill="none")


def ink(children):
    """Solid black -- eyes, noses, tiny accents only."""
    return group(children, fill=BLACK, stroke="none")


def page(body, title, guides=False):
    g = ""
    if guides:
        g = ('\n  <rect x="100" y="100" width="650" height="900" fill="none" '
             'stroke="#e0e0e0" stroke-width="3" stroke-dasharray="12 12"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="8.5in" height="11in" '
        'viewBox="0 0 %d %d">\n'
        '  <title>%s</title>\n'
        '  <rect width="%d" height="%d" fill="%s"/>%s\n'
        '  <g fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" '
        'stroke-linecap="round" stroke-miterlimit="4">\n  %s\n  </g>\n</svg>\n'
        % (W, H, title, W, H, WHITE, g, WHITE, BLACK, n(MID),
           "\n  ".join(x for x in body if x))
    )
