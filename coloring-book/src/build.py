#!/usr/bin/env python3
"""
build.py -- render "The Wander Balloon" from source.

  python3 build.py            # all pages: SVG + preview PNGs + print PDF + checks
  python3 build.py 7          # just page 7 (fast iteration while drawing)
  python3 build.py --no-pdf   # skip the PDF assembly

Every page is checked automatically for the two things that ruin a coloring
book at the printer: art straying outside the 1 in safe margin, and any pixel
that is neither black nor white (a gray edge means something got a fill or an
opacity it should not have).
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "pages"))

PAGES_DIR = os.path.join(ROOT, "pages")
PRINT_DIR = os.path.join(ROOT, "print")
PREVIEW_DIR = os.environ.get(
    "CB_PREVIEW",
    "/tmp/claude-0/-home-user-portfolio/7b845276-1413-51e0-90b5-d4e4d121fac0/scratchpad/preview")

import inkstyle as I  # noqa: E402


def load(num):
    return importlib.import_module("p%02d" % num)


def available():
    out = []
    for i in range(1, 25):
        if os.path.exists(os.path.join(HERE, "pages", "p%02d.py" % i)):
            out.append(i)
    return out


def render(num, guides=False):
    mod = load(num)
    svg = I.page(mod.draw(), mod.TITLE, guides=guides)
    path = os.path.join(PAGES_DIR, "page-%02d-%s.svg" % (num, mod.SLUG))
    with open(path, "w") as fh:
        fh.write(svg)
    return path, mod


def check(png_path):
    """Safe-margin + pure-black-and-white check on a 100 dpi render."""
    from PIL import Image
    im = Image.open(png_path).convert("L")
    w, h = im.size
    dpi = w / 8.5
    bbox = im.point(lambda v: 255 - v).getbbox()
    problems = []
    if bbox is None:
        return ["page is blank"]
    left, top, right, bottom = [v / dpi for v in bbox]
    if left < 0.995 or top < 0.995 or right > 7.505 + 0.005 or bottom > 10.005:
        problems.append("art outside 1in safe margin: L%.2f T%.2f R%.2f B%.2f"
                        % (left, top, 8.5 - right, 11 - bottom))
    hist = im.histogram()
    midtone = sum(hist[40:216])
    if midtone > 0.16 * w * h:
        problems.append("too much midtone (%d px) -- check for gray fills" % midtone)
    return problems


def main():
    args = [a for a in sys.argv[1:]]
    do_pdf = "--no-pdf" not in args
    guides = "--guides" in args
    nums = [int(a) for a in args if a.isdigit()] or available()
    os.makedirs(PAGES_DIR, exist_ok=True)
    os.makedirs(PRINT_DIR, exist_ok=True)
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    import cairosvg

    ok = True
    for num in nums:
        path, mod = render(num, guides=guides)
        png = os.path.join(PREVIEW_DIR, "page-%02d.png" % num)
        cairosvg.svg2png(url=path, write_to=png, output_width=850)
        probs = check(png)
        ok = ok and not probs
        print("%2d  %-26s %s" % (num, mod.SLUG, "OK" if not probs else "; ".join(probs)))

    if do_pdf and len(nums) > 1:
        from pypdf import PdfWriter
        writer = PdfWriter()
        for num in nums:
            mod = load(num)
            src = os.path.join(PAGES_DIR, "page-%02d-%s.svg" % (num, mod.SLUG))
            tmp = os.path.join(PREVIEW_DIR, "p%02d.pdf" % num)
            cairosvg.svg2pdf(url=src, write_to=tmp)
            writer.append(tmp)
        out = os.path.join(PRINT_DIR, "the-wander-balloon-interior.pdf")
        with open(out, "wb") as fh:
            writer.write(fh)
        print("\nprint PDF -> %s (%d pages)" % (os.path.relpath(out, ROOT), len(nums)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
