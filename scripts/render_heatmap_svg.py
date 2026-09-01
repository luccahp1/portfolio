"""Draw the contribution calendar as an animated SVG.

53 weeks by 7 days of rounded boxes that slide in diagonally, once, and then
freeze. The motion is CSS keyframes inside the SVG, which GitHub runs for an
<img>-embedded file; there is no loop and no glow, because a README that keeps
moving is a README nobody finishes reading.

    python scripts/render_heatmap_svg.py
    STATIC=1 python scripts/render_heatmap_svg.py   # frozen frame

Reads profile/data/contributions.json. With no data file it draws an honest
empty grid instead of inventing numbers; the daily workflow fills it in.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile_config as cfg  # noqa: E402

PALETTE = ["#161b22", "#0e4429", "#006d32",
           "#26a641", "#39d353", "#69f0a0"]
#          none -> brightest (level 5 is a neon top end)

WEEKS = 53
PAD = 24.0
BAR_H = 30.0
LABEL_W = 30.0        # room for the Mon/Wed/Fri column
MONTH_H = 18.0
GAP = 3.0
FOOT_H = 34.0

DELAY_WEEK = 0.020    # seconds per column, left to right
DELAY_DAY = 0.060     # seconds per row, top to bottom -> a diagonal sweep
DROP = 0.45           # seconds for one box to settle

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load():
    if cfg.CONTRIB_JSON.exists():
        return json.loads(cfg.CONTRIB_JSON.read_text(encoding="utf-8"))
    print(f"{cfg.CONTRIB_JSON.relative_to(cfg.ROOT)} not found - drawing an "
          f"empty grid. Run fetch_contributions.py (or let the workflow do it).")
    end = date.today()
    start = end - timedelta(days=WEEKS * 7 - 1)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    days = [{"date": (start + timedelta(days=i)).isoformat(),
             "count": 0, "level": 0}
            for i in range((end - start).days + 1)]
    return {"user": cfg.USERNAME, "days": days, "total": None,
            "range": {"from": days[0]["date"], "to": days[-1]["date"]},
            "current_streak": None, "longest_streak": None,
            "best_day": {"date": None, "count": None}, "generated": None}


def to_columns(days):
    """Lay the days out the way GitHub does: one column per week, Sunday first."""
    by_date = {d["date"]: d for d in days}
    first = datetime.strptime(days[0]["date"], "%Y-%m-%d").date()
    first -= timedelta(days=(first.weekday() + 1) % 7)   # back to Sunday
    last = datetime.strptime(days[-1]["date"], "%Y-%m-%d").date()

    columns = []
    cursor = first
    while cursor <= last and len(columns) < WEEKS:
        week = []
        for i in range(7):
            day = cursor + timedelta(days=i)
            week.append(by_date.get(day.isoformat()) if day <= last else None)
        columns.append((cursor, week))
        cursor += timedelta(days=7)
    return columns[-WEEKS:]


def plural(n, word):
    return f"{n:,} {word}{'' if n == 1 else 's'}"


def footer_text(data):
    if data.get("total") is None:
        return ("waiting on the first sync - the workflow fills this in",
                "")
    span = data.get("range", {})
    left = f"{plural(data['total'], 'contribution')} in the last year"
    bits = []
    if data.get("current_streak") is not None:
        bits.append(f"{data['current_streak']}d streak")
    if data.get("longest_streak"):
        bits.append(f"best {data['longest_streak']}d")
    best = data.get("best_day") or {}
    if best.get("count"):
        bits.append(f"top day {best['count']} on {best['date']}")
    if span.get("to"):
        bits.append(f"through {span['to']}")
    return left, "  ·  ".join(bits)


def build(data, static):
    columns = to_columns(data["days"])
    w = cfg.HEATMAP_W
    grid_x = PAD + LABEL_W
    pitch = (w - grid_x - PAD) / WEEKS
    cell = pitch - GAP
    rx = round(cell * 0.22, 2)
    grid_y = BAR_H + 14 + MONTH_H
    h = round(grid_y + 7 * pitch + FOOT_H + PAD * 0.4)

    css = f"""
    .lbl {{ font-family: {cfg.MONO}; font-size: 10px; fill: {cfg.DIM}; }}
    .foot {{ font-family: {cfg.MONO}; font-size: 12px; fill: {cfg.FG}; }}
    .foot-dim {{ font-family: {cfg.MONO}; font-size: 11px; fill: {cfg.DIM}; }}
    """
    if not static:
        css += f"""
    .c {{ animation: drop {DROP}s cubic-bezier(.22,.9,.3,1) both; }}
    @keyframes drop {{
      from {{ opacity: 0; transform: translateY(-7px) scale(.72); }}
      to   {{ opacity: 1; transform: none; }}
    }}
    .fade {{ animation: fade .5s ease-out both; }}
    @keyframes fade {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .c, .fade {{ animation: none; opacity: 1; transform: none; }}
    }}
    """

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="{cfg.USERNAME}\'s GitHub contribution calendar">',
        f'<title>{cfg.USERNAME} - contributions</title>',
        f'<style>{css}</style>',
        cfg.rounded_panel(w, h, title=f"{cfg.USERNAME}@github: ~/contributions",
                          bar_h=BAR_H),
    ]

    def anim(delay, base="", kind="fade"):
        """Emit one class attribute: two would be a duplicate-attribute error."""
        names = [n for n in (base, "" if static else kind) if n]
        attr = f' class="{" ".join(names)}"' if names else ""
        return attr if static else f'{attr} style="animation-delay:{delay:.3f}s"'

    # Month labels, above the first column of each month. A month needs three
    # columns to earn one, or the label collides with the next month's: the
    # window rarely starts on a month boundary.
    last_month, last_label = None, -99
    for wi, (sunday, _) in enumerate(columns):
        month = (sunday + timedelta(days=6)).month
        if month == last_month:
            continue
        last_month = month
        # Column 0 is usually a stub of the month before the window; labelling
        # it just crowds the real first month out.
        if wi == 0 and len(columns) > 1 and \
                (columns[1][0] + timedelta(days=6)).month != month:
            continue
        if wi - last_label < 3 or wi > WEEKS - 3:
            continue
        last_label = wi
        x = grid_x + wi * pitch
        out.append(f'<text x="{x:.1f}" y="{grid_y - 6:.1f}"'
                   f'{anim(wi * DELAY_WEEK, "lbl")}>'
                   f'{MONTHS[month - 1]}</text>')

    # Weekday labels, the same three GitHub prints.
    for di, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = grid_y + di * pitch + cell * 0.78
        out.append(f'<text x="{PAD:.1f}" y="{y:.1f}"'
                   f'{anim(di * DELAY_DAY, "lbl")}>{name}</text>')

    # The grid.
    out.append("<g>")
    for wi, (sunday, week) in enumerate(columns):
        x = grid_x + wi * pitch
        for di, day in enumerate(week):
            if day is None:
                continue
            y = grid_y + di * pitch
            level = min(int(day.get("level", 0)), len(PALETTE) - 1)
            delay = wi * DELAY_WEEK + di * DELAY_DAY
            count = day["count"]
            label = (f'{plural(count, "contribution")} on {day["date"]}'
                     if count else f'No contributions on {day["date"]}')
            out.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell:.2f}" '
                f'height="{cell:.2f}" rx="{rx}" fill="{PALETTE[level]}" '
                f'transform-origin="{x + cell / 2:.2f}px {y + cell / 2:.2f}px"'
                f'{anim(delay, kind="c")}><title>{label}</title></rect>')
    out.append("</g>")

    tail = grid_y + 7 * pitch
    last_delay = (WEEKS - 1) * DELAY_WEEK + 6 * DELAY_DAY + DROP

    # Footer: the headline number on the left, the details under it.
    left, right = footer_text(data)
    out.append(f'<text x="{PAD:.1f}" y="{tail + 15:.1f}"'
               f'{anim(last_delay, "foot")}>{cfg.esc(left)}</text>')
    if right:
        out.append(f'<text x="{PAD:.1f}" y="{tail + 30:.1f}"'
                   f'{anim(last_delay + 0.1, "foot-dim")}>'
                   f'{cfg.esc(right)}</text>')

    # Legend, bottom right.
    lg_cell = cell * 0.85
    lg_pitch = lg_cell + 4
    lg_w = len(PALETTE) * lg_pitch
    lg_x = w - PAD - lg_w - 34
    lg_y = tail + 6
    out.append(f'<g{anim(last_delay)}>')
    out.append(f'<text class="lbl" x="{lg_x - 6:.1f}" '
               f'y="{lg_y + lg_cell * 0.8:.1f}" text-anchor="end">Less</text>')
    for i, colour in enumerate(PALETTE):
        out.append(f'<rect x="{lg_x + i * lg_pitch:.1f}" y="{lg_y:.1f}" '
                   f'width="{lg_cell:.1f}" height="{lg_cell:.1f}" '
                   f'rx="{rx}" fill="{colour}"/>')
    out.append(f'<text class="lbl" x="{lg_x + lg_w + 2:.1f}" '
               f'y="{lg_y + lg_cell * 0.8:.1f}">More</text>')
    out.append('</g>')

    out.append('</svg>')
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--static", action="store_true",
                    help="emit a frozen frame instead of the reveal")
    args = ap.parse_args()
    static = args.static or os.environ.get("STATIC") == "1"
    data = load()
    cfg.write(cfg.HEATMAP_SVG, build(data, static))


if __name__ == "__main__":
    main()
