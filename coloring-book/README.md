# The Wander Balloon 🎈

An original 24-page kids' coloring book — concept, cover direction, and all 24
print-ready interior pages as vector line art.

| | |
|---|---|
| **Concept, 24-page outline, cover direction** | [`CONCEPT.md`](CONCEPT.md) |
| **Interior style rules + what the build checks** | [`STYLE-GUIDE.md`](STYLE-GUIDE.md) |
| **The 24 pages** | [`pages/`](pages) — one SVG each, 8.5 × 11 in |
| **Print file** | [`print/the-wander-balloon-interior.pdf`](print) |
| **Cover rough** | [`cover/cover-mockup.svg`](cover) — line art, title zones left empty |
| **Source** | [`src/`](src) — the drawing system every page is built from |

Ages 4–8. Bold black outlines, closed shapes, white backgrounds, no gray, no
text, no trademarked characters, 1 in safe margins on every page.

## Building

```bash
pip install cairosvg pypdf pillow
python3 src/build.py          # all 24 pages: SVG + previews + print PDF + checks
python3 src/build.py 7        # just page 7, while drawing it
python3 src/build.py --guides # draw the safe-margin box into the SVGs
python3 src/cover.py          # the cover rough
```

`build.py` prints a line per page and fails the run if any page strays outside
the 1 in safe margin or renders anything that isn't black or white.

## How the art is made

Nothing here is traced or adapted from existing artwork. Three files do the work:

* **`src/inkstyle.py`** — the house style: page geometry, the three line weights,
  and the primitives (smoothed organic outlines, capsule limbs, stars, arcs).
* **`src/motifs.py`** — the recurring cast (Sorrel the fox cub, Mo the snail, the
  balloon) and the scenery vocabulary (clouds, puffs, trees, leaves, grass).
  Characters are drawn once in local coordinates and placed at any scale with
  their stroke widths pre-compensated, so line weight never changes.
* **`src/pages/pNN.py`** — one module per page: composition only.

Re-skinning the book to a different theme or age band means changing motifs and
compositions, not redrawing 24 pages by hand.
