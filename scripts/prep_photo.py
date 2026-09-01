"""Turn a photo into a high-contrast grayscale plate for the ASCII converter.

A flatly lit face converts to an unreadable blob, because the ASCII ramp only
has thirteen steps to spend. Three things fix that:

  1. isolate the subject (rembg, when it is installed) so the background does
     not eat half the ramp,
  2. push local contrast with CLAHE, which is what gives a flat face real
     highlights and shadows,
  3. composite onto pure white, so whatever is left of the background lands on
     the blank end of the ramp and prints as nothing.

Run it once per photo:

    python scripts/prep_photo.py path/to/photo.jpg
    python scripts/prep_photo.py --github luccahp1   # use the GitHub avatar

Writes profile/data/source-prepped.png.
"""

import argparse
import io
import sys

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import profile_config as cfg  # noqa: E402

# The ASCII grid is 100 x 51 cells and a monospace cell is twice as tall as it
# is wide, so the plate wants to be 100 : 102 -> effectively square.
TARGET_ASPECT = 100 / 102.0


def load(args):
    if args.github:
        import requests
        url = f"https://github.com/{args.github}.png?size=1024"
        print(f"fetching {url}")
        r = requests.get(url, timeout=30,
                         headers={"User-Agent": "profile-art/1.0"})
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert("RGBA")
    return Image.open(args.photo).convert("RGBA")


def cut_out(img, enabled):
    """Return an RGBA image whose alpha marks the subject, or None."""
    if not enabled:
        return None
    try:
        from rembg import remove
    except ImportError:
        print("rembg not installed - skipping background removal "
              "(pip install rembg to enable it)")
        return None
    print("removing background with rembg ...")
    return remove(img)


def crop_to_subject(img, alpha):
    """Crop to the subject's bounding box, then out to the target aspect."""
    w, h = img.size
    if alpha is not None:
        ys, xs = np.nonzero(alpha > 8)
        if len(xs):
            x0, x1 = int(xs.min()), int(xs.max())
            y0, y1 = int(ys.min()), int(ys.max())
            pad_x = int((x1 - x0) * 0.06)
            pad_y = int((y1 - y0) * 0.06)
            x0, y0 = max(0, x0 - pad_x), max(0, y0 - pad_y)
            x1, y1 = min(w, x1 + pad_x), min(h, y1 + pad_y)
        else:
            x0, y0, x1, y1 = 0, 0, w, h
    else:
        x0, y0, x1, y1 = 0, 0, w, h

    cw, ch = x1 - x0, y1 - y0
    # Grow the box (never shrink the subject) until it hits the target aspect.
    if cw / ch > TARGET_ASPECT:
        want = cw / TARGET_ASPECT
        grow = (want - ch) / 2
        y0, y1 = y0 - grow, y1 + grow
    else:
        want = ch * TARGET_ASPECT
        grow = (want - cw) / 2
        x0, x1 = x0 - grow, x1 + grow
    return tuple(int(round(v)) for v in (x0, y0, x1, y1))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("photo", nargs="?", help="path to a source photo")
    src.add_argument("--github", metavar="USER",
                     help="use https://github.com/USER.png instead of a file")
    ap.add_argument("--no-cutout", action="store_true",
                    help="skip rembg even if it is installed")
    ap.add_argument("--clip", type=float, default=2.6,
                    help="CLAHE clip limit; higher is punchier (default 2.6)")
    ap.add_argument("--gamma", type=float, default=1.0,
                    help="<1 brightens the midtones, >1 darkens them")
    ap.add_argument("--size", type=int, default=900,
                    help="width of the prepped plate in pixels")
    args = ap.parse_args()

    img = load(args)
    cut = cut_out(img, not args.no_cutout)
    alpha = np.array(cut.split()[-1]) if cut is not None else None

    box = crop_to_subject(img, alpha)
    # Pad rather than clamp, so an off-centre subject stays off-centre.
    pad_l = max(0, -box[0])
    pad_t = max(0, -box[1])
    pad_r = max(0, box[2] - img.width)
    pad_b = max(0, box[3] - img.height)
    if pad_l or pad_t or pad_r or pad_b:
        canvas = Image.new("RGBA", (img.width + pad_l + pad_r,
                                    img.height + pad_t + pad_b), (255, 255, 255, 0))
        canvas.paste(img, (pad_l, pad_t))
        img = canvas
        if alpha is not None:
            a = Image.new("L", canvas.size, 0)
            a.paste(Image.fromarray(alpha), (pad_l, pad_t))
            alpha = np.array(a)
        box = (box[0] + pad_l, box[1] + pad_t, box[2] + pad_l, box[3] + pad_t)

    img = img.crop(box)
    if alpha is not None:
        alpha = np.array(Image.fromarray(alpha).crop(box))

    height = int(round(args.size / TARGET_ASPECT))
    img = img.resize((args.size, height), Image.LANCZOS)
    if alpha is not None:
        alpha = np.array(Image.fromarray(alpha).resize((args.size, height),
                                                       Image.LANCZOS))

    gray = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2GRAY)

    # Stretch levels using only the subject's pixels, so a bright background
    # cannot pin the white point and flatten the face.
    mask = alpha > 8 if alpha is not None else np.ones(gray.shape, bool)
    if mask.sum() > 64:
        lo, hi = np.percentile(gray[mask], (1.0, 99.0))
        if hi > lo:
            gray = np.clip((gray.astype(np.float32) - lo) * 255.0 / (hi - lo),
                           0, 255).astype(np.uint8)

    gray = cv2.createCLAHE(clipLimit=args.clip,
                           tileGridSize=(8, 8)).apply(gray)

    if abs(args.gamma - 1.0) > 1e-3:
        lut = np.array([((i / 255.0) ** args.gamma) * 255
                        for i in range(256)], np.uint8)
        gray = cv2.LUT(gray, lut)

    # A light unsharp mask puts the edges back that the downscale softened.
    gray = cv2.addWeighted(gray, 1.45, cv2.GaussianBlur(gray, (0, 0), 3.0),
                           -0.45, 0)

    if alpha is not None:
        a = (alpha.astype(np.float32) / 255.0)[..., None]
        flat = gray.astype(np.float32)[..., None]
        gray = (flat * a + 255.0 * (1 - a))[..., 0].astype(np.uint8)

    cfg.PREPPED_PNG.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(gray, "L").save(cfg.PREPPED_PNG, optimize=True)
    print(f"wrote {cfg.PREPPED_PNG.relative_to(cfg.ROOT)} "
          f"({args.size}x{height})")
    print("next: python scripts/make_ascii_svg.py")


if __name__ == "__main__":
    main()
