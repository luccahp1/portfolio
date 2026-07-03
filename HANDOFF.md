# Handoff - portfolio

## Current state
- v1.5 headline: **the cord snaps twice.** First snap = the v1.4 gag (stub, sparks, flicker, 9s tape repair - the repair toast now hints at what a second snap does). Second snap = `condemnCord()` in `js/main.js`: the rope is restored visually but duct-taped static (`.ducttape` x2 on the button, button `disabled`), and a real wall switch (`#wallswitch`, drill-in animation) appears beside it. The switch clicks the theme like a normal house. Terminal command `rewire` undoes all of it and resets the break counter. None of this persists - a reload always gives a fresh cord, on purpose.
- v1.5 also:
  - **`race`** terminal command: scrolls to top, locks scrolling (html overflow + wheel/touch/key blockers), shows a full-width 400px semi-transparent checkered banner, counts 3-2-1-GO with blips, then unlocks and restarts the speedrun clock (`rearmSpeedrun`) with `raceRun = true`. A race finish ALWAYS celebrates (confetti + time), regardless of how long it took - unlike a passive speedrun, which only fires inside the time window. `finishLine()` shows the current time and the saved best, and updates `state.raceBest` (persisted - a legit highscore, not a physics slider) when beaten. `whoami` surfaces the best too.
  - **speedrun trackpad support**: a wheel-event heuristic (`padLike()` - many small deltaY steps = trackpad) widens the speedrun window from 9s to 15s.
  - **`physics`** terminal command: live sliders (gravity, damping, wake/brush radius, stretch, pull threshold, segments) editing the `PH` object the rope reads every frame. DELIBERATELY never written to localStorage so a wild slider session can't brick anyone's lamp past a reload. `PHYS_DEF` holds factory values.
  - **`forget` actually works now**: it used to remove the key, then the 30s heartbeat / ghost pagehide stash / any later `save()` re-wrote the still-populated in-memory state. Fix: a `forgotten` latch inside the shared `save()` (all modules use it via `window.__site`), then a reload.
  - **pencil vs lights bug fixed**: body's `color` has a 0.35s transition, so redrawing at theme-change time read the OLD color and painted doodles invisible. `inkColor()` now reads `--ink` off the root (custom props don't transition) and the redraw happens on the next frame.
  - the snap **flicker is an overlay now** (`.flick`, ~2.4s of hard opacity stutters; warm flash in dark mode). Never use a filter on body for this: filters make body a containing block and rip every `position: fixed` element out of the viewport.
  - **cord toasts land in the vicinity**: `cordAt()` returns a random on-screen `{x, y}` within ~300px of the cord, always left of it, never on top. `toast()` accepts `{x, y}` points now, plus the old `{el, ...}` anchors.
  - **all toasts linger 2s longer** (single `ms += 2000` inside `toast()`).
  - **tape pull lines** are a 6-entry random pool in `js/tape.js` (no immediate repeats).
  - **hover eggs**: "prada" in the header wordmark has a tooltip (`.tip-down` opens downward), and the "also: coffee" margin note steams on hover (`.steam` wisps, CSS-only).
  - terminal `help` is now one `command - description` line each; `secrets.txt` and the spoiler panel list the new eggs; hints sprinkled in `hi-extras`, the console message, and the first-break repair toast.
- v1.4: lamp cord is a Verlet rope (`#cord-path`/`#cord-knob`), physics only wakes within `PH.wake` px of the cord, naps when settled; grab/pull any direction, tension past `PH.pull` fires the switch; ghost replay slowed ~35%; anchored toasts sit on a translucent paper slip; all em dashes replaced with hyphens.
- v1.3: real thumbtack images at random spots/angles on pulled cards; toasts anchor near their trigger; guestbook replaced by the vouch card (`js/vouch.js`).
- Base site: single-page `index.html` + `resume.html`, `404.html`, `humans.txt`, `favicon.svg`. Vanilla JS: memory/greetings/cord/blueprint/confetti/race/physics (`js/main.js`), ghost cursor replay (`js/ghost.js`), pencil drawing (`js/pencil.js`), terminal (`js/terminal.js`), tape-pull skit (`js/tape.js`).
- Ctrl+P prints ONLY the real one-page resume (`.print-resume`); `resume.html` is the same resume as a page. Full version with phone lives in `C:\Bin\Resume\2026\`.
- No backend, no build step. Visitor data stays in their localStorage.

## Next steps
- Deployed to GitHub Pages: https://luccahp1.github.io/portfolio/ (repo public, Pages on main/root). The root https://luccahp1.github.io redirects here via a separate `luccahp1.github.io` repo.
- Optional: point a custom domain at it (update the two hardcoded URLs in `404.html` if so).
- Replace "somewhere north enough" with a real location if Lucca wants one.
- Add vouches as they arrive by email (hand-edit `#vouch-list`; format: name - company/role - one good line).
- Optional: wire `uptime`'s "closet server" line to a real health endpoint on luccaserver.
- Optional: OG image for link previews.

## Notes / gotchas
- House style: no em dashes anywhere in this repo - use plain hyphens. Same for anything new you write into it.
- The physics sliders (`physics` command) must NEVER persist to localStorage. That is a design requirement, not an oversight: if a visitor breaks the cord with the sliders, a reload must always fix it.
- The cord's second-break state (duct tape + wall switch) is session-only for the same reason.
- `save()` in main.js is shared by every module through `window.__site` and goes inert once `forget` runs (the `forgotten` latch). Don't add a new localStorage write path that bypasses it.
- Never animate a filter on body (the old flicker did): body becomes a containing block and every `position: fixed` element (cord, toasts, tools) re-anchors to the document instead of the viewport. The flicker is a fixed overlay (`.flick`) instead.
- `inkColor()` in pencil.js must read `--ink` from the root, not `getComputedStyle(body).color` - body's color transitions for 0.35s on theme change and mid-transition reads paint doodles invisible.
- Terminal `html()` helper must only ever receive static strings - never user input.
- The ghost stores the previous session under `state.ghostPrev` (inside `lucca.site.v1`); it only stashes sessions with >=50 cursor samples and >=8s duration.
- Google Fonts (Fraunces, Caveat) are the only external requests; the site degrades fine without them.
- The lowercase voice is intentional on screen; print output comes from the hidden `.print-resume` block (professionally capitalized). Keep it in sync with `resume.html` and `C:\Bin\Resume\2026\`.
- Resume dates: WSIB is listed as "May 2025 – Present" - update if the co-op has ended.
- Reduced-motion users get a static cord (physics never wakes; `physics` command explains itself instead of opening); taps/keyboard still toggle the theme. The race banner still works (it's just text swaps).
- Cord tuning defaults live in `PHYS_DEF` at the top of the cord section in `js/main.js`.
