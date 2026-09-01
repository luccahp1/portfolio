"""Shared settings for the profile art scripts.

Every generated SVG paints its own dark terminal panel instead of relying on
GitHub's theme. An SVG embedded with <img> only sees the reader's OS colour
scheme, not the theme they picked on GitHub, so a transparent background with
light text would vanish for half the people who look at the page.
"""

from pathlib import Path

USERNAME = "luccahp1"

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "profile"
DATA = OUT / "data"

PORTRAIT_SVG = OUT / "ascii-portrait.svg"
INFO_CARD_SVG = OUT / "info-card.svg"
HEATMAP_SVG = OUT / "contrib-heatmap.svg"
CONTRIB_JSON = DATA / "contributions.json"
PREPPED_PNG = DATA / "source-prepped.png"

# Terminal palette (GitHub's own dark-mode values, so the panels sit naturally
# next to the site chrome).
BG = "#0d1117"
PANEL_EDGE = "#21262d"
BAR = "#161b22"
FG = "#c9d1d9"
DIM = "#8b949e"
GREEN = "#39d353"
BLUE = "#58a6ff"
ORANGE = "#f0883e"
PURPLE = "#bc8cff"
RED = "#ff7b72"

# Single quotes on purpose: this string lands inside double-quoted XML
# attributes as well as inside <style> blocks, and double quotes would end the
# attribute early.
MONO = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'DejaVu Sans Mono', 'Liberation Mono', monospace")

# The README lays the portrait and the card side by side at 370 + 490 = 860,
# which is also the heatmap's width. These two viewBoxes are sized so both
# columns render at the same height at those widths.
PORTRAIT_W, PORTRAIT_H = 636, 670
CARD_W, CARD_H = 700, 557
HEATMAP_W = 860


def rounded_panel(w, h, title=None, bar_h=30):
    """Dark rounded panel with an optional title bar. Returns an SVG fragment."""
    parts = [
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" '
        f'fill="{BG}" stroke="{PANEL_EDGE}"/>'
    ]
    if title is not None:
        parts.append(
            f'<path d="M0.5 10.5a10 10 0 0 1 10-10h{w - 21}a10 10 0 0 1 10 10'
            f'V{bar_h}H0.5Z" fill="{BAR}"/>'
            f'<line x1="0.5" y1="{bar_h}" x2="{w - 0.5}" y2="{bar_h}" '
            f'stroke="{PANEL_EDGE}"/>'
        )
        for i, colour in enumerate((RED, ORANGE, GREEN)):
            parts.append(
                f'<circle cx="{18 + i * 15}" cy="{bar_h / 2}" r="4.5" '
                f'fill="{colour}" opacity="0.85"/>'
            )
        parts.append(
            f'<text x="{w / 2}" y="{bar_h / 2 + 4}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="11" fill="{DIM}">'
            f'{esc(title)}</text>'
        )
    return "".join(parts)


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def write(path, svg):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({len(svg.encode()):,} bytes)")
