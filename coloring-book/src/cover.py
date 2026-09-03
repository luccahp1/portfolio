#!/usr/bin/env python3
"""
cover.py -- front cover composition for "The Wander Balloon".

This renders the cover as LINE ART ONLY, the way a cover is roughed before it
goes to color. The title, subtitle and page-count callout are left as empty
zones (the banner across the top and the badge bottom-right): type is set at
design time in a hand-lettered open-licence face, never baked into the drawing.
Colour, type and back-cover direction are written up in ../CONCEPT.md.

  python3 cover.py     -> ../cover/cover-mockup.svg (+ a preview PNG)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "pages"))

import inkstyle as I  # noqa: E402
import motifs as M  # noqa: E402
from p05 import sheep  # noqa: E402

PREVIEW = os.environ.get(
    "CB_PREVIEW",
    "/tmp/claude-0/-home-user-portfolio/7b845276-1413-51e0-90b5-d4e4d121fac0/scratchpad/preview")


def draw():
    keyline = I.group([I.rect(30, 30, 790, 1040, r=26)],
                      fill="none", stroke_width="6")

    # title zone: a ribbon banner, left empty for lettering
    banner = I.mid([I.blob([(112, 150), (425, 116), (738, 150), (720, 292),
                            (425, 258), (130, 292)], t=0.6)])
    banner_in = I.fine([I.blob([(146, 178), (425, 150), (704, 178), (690, 262),
                                (425, 230), (160, 262)], t=0.6)])

    sky = I.mid([M.cloud(196, 430, 190, 88, bumps=3),
                 M.cloud(686, 386, 160, 78, bumps=3, seed=2)] +
                M.bird(214, 336, 56) + M.bird(300, 372, 46) + M.bird(690, 300, 50))

    flock = []
    for cx, cy, w, h, seed, flip in ((206, 664, 200, 102, 0, True),
                                     (706, 656, 172, 90, 2, False)):
        b, hd, ey = sheep(cx, cy, w, h, seed, flip)
        flock += [I.mid(b), I.mid(hd), I.ink(ey)]

    balloon = I.at(452, 620, 0.74, M.wander(0.74, patch=True))
    pilot = I.at(452, 726, 0.62, M.sorrel(0.62, pose="peek", goggles=True))
    mo = I.at(292, 894, 0.34, M.mo(0.34, flip=True))

    stars = I.mid([M.star(146, 796, 28), M.star(700, 800, 24), M.star(168, 946, 20)])

    # page-count badge: empty circle, bottom right
    badge = I.mid([I.circle(716, 962, 74)])
    badge_in = I.fine([I.circle(716, 962, 56)])

    return [keyline, sky] + flock + [banner, banner_in, balloon, pilot, mo,
                                     stars, badge, badge_in]


def main():
    os.makedirs(os.path.join(ROOT, "cover"), exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    out = os.path.join(ROOT, "cover", "cover-mockup.svg")
    with open(out, "w") as fh:
        fh.write(I.page(draw(), "The Wander Balloon -- cover mockup"))
    import cairosvg
    cairosvg.svg2png(url=out, write_to=os.path.join(PREVIEW, "cover.png"), output_width=850)
    print("cover -> %s" % os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
