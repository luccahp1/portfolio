# The Wander Balloon — interior style guide

One page, one style, twenty-four times. These are the rules the art is built to,
and `src/build.py` checks the ones a machine can check.

## Page

| | |
|---|---|
| Trim | 8.5 × 11 in portrait |
| Coordinate system | `viewBox="0 0 850 1100"` — 100 user units = 1 inch |
| Safe area | 1.00 in on all four sides → x 100–750, y 100–1000 |
| Background | Solid white rectangle, always drawn first |
| Colour | Black strokes on white fills. Nothing else. No gray, no screens, no gradients, no opacity |

## Line

| Weight | Units | Metric | Used for |
|---|---|---|---|
| `BOLD` | 11 | ≈ 2.8 mm | The outermost silhouette of any subject |
| `MID` | 8 | ≈ 2.0 mm | Secondary objects, mid-ground, scenery |
| `FINE` | 6 | ≈ 1.5 mm | Interior detail, pattern, texture |
| solid black | — | — | Eyes, noses and tiny accents only |

Every stroke is `stroke-linejoin="round"` and `stroke-linecap="round"`. Scaled
artwork divides its stroke widths by the scale factor, so a character drawn at
40% keeps exactly the same line weight as one drawn at 100%.

## Shape

* **Everything closes.** No open contour anywhere a child might colour — colour
  has to have somewhere to stop.
* **Minimum colourable gap ≈ 20 units (0.2 in / 5 mm).** If a fat crayon can't
  land inside a shape, the shape is wrong.
* **White fills carry depth.** Objects are drawn back-to-front; a nearer shape's
  white fill hides the lines behind it. There is no other overlap trick.
* **Organic outlines come from point lists,** smoothed with a Catmull-Rom pass
  (`inkstyle.smooth`). Corners that must stay sharp — ear tips, leaf points,
  star points — are flagged per point.

## Cast consistency

* Every creature in the book uses the same face module: two solid round eyes and
  one smile curve, at the same relative sizes.
* Sorrel always wears the striped scarf; the flight goggles appear only when
  flying or on the cover.
* Clouds, bushes, tree canopies, sheep wool, sea foam and Sorrel's tail are all
  the same puff primitive at different sizes. That single reuse is most of why
  the pages look like one hand drew them.

## Automated checks (`python3 src/build.py`)

1. **Safe margin** — the rendered bounding box of every page must sit inside the
   1 in margin. A page that fails names which edge it broke.
2. **Ink purity** — a page rendered at 100 dpi must be essentially black and
   white; too many midtone pixels means something picked up a fill or an opacity
   it should not have.

## Not in the interiors, ever

No text, letters or numerals. No trademarked or copyrighted characters, logos or
brand marks. No real-person likenesses. No page numbers inside the art (if the
printer needs folios, they sit in the trim margin at layout time, not in the
drawing).
