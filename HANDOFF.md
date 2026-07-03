# Handoff - portfolio

## Current state
- v1.4: the lamp cord is now a real physics rope (Verlet chain in `js/main.js`, `#cord-path`/`#cord-knob` in `index.html`): 9 nodes under gravity with distance constraints + damping, drawn every frame into the svg path. Grab it and pull in ANY direction - it stretches (held segments only correct partway, that's the stretch), and past ~16px of tension the switch gives and the theme flips. Swiping the mouse through it shoves the nodes it grazes (force from mouse velocity). Optimization: the rAF loop only runs while the pointer is within 160px of the cord (or a grab/energy is live); it naps and resets to rest otherwise. Plain taps and keyboard (enter/space, `e.detail === 0` clicks) still toggle. Snap gag kept: 8 fast pulls -> rope truncates to a 3-node stub, falls, repairs after 9s.
- v1.4 also: ghost replay slowed ~35% (dt scaled 1.35x, follow-lerp 0.24, longer scripted glides in `js/ghost.js`); anchored toasts sit on a translucent paper slip (`.toast.anchored`: color-mix paper at 82% + blur) so they read over anything; all em dashes replaced with plain hyphens across every file (site copy, docs, resume).
- v1.3: real thumbtack images (`img/pin-head.png`, `img/pin-classic.png`) at random spots/angles on pulled cards; pinned cards hang tilted with a curled-corner shadow; toasts anchor near their trigger; guestbook replaced by the vouch card (`js/vouch.js` - mailto-based, role question appears only when company is typed).
- Base site: single-page `index.html` + `resume.html`, `404.html`, `humans.txt`, `favicon.svg`. Vanilla JS features: memory/greetings/cord/blueprint/confetti (`js/main.js`), ghost cursor replay (`js/ghost.js`), pencil drawing (`js/pencil.js`), terminal (`js/terminal.js`), tape-pull skit (`js/tape.js`).
- Blueprint mode shows px dimensions; speedrun ending shows elapsed time + paper-scrap confetti; tape on cards is grab-and-pullable -> card falls -> "lucca" mouse pins it back.
- Ctrl+P on index prints ONLY the real one-page resume (`.print-resume` block); `resume.html` is the same resume as a normal page. Web versions omit the phone number on purpose; the full version with phone lives in `C:\Bin\Resume\2026\` (HTML + generated PDF).
- No backend, no build step. Visitor data stays in their localStorage.

## Next steps
- Deployed to GitHub Pages: https://luccahp1.github.io/portfolio/ (repo public, Pages on main/root).
- Optional: point a custom domain at it (update the two hardcoded URLs in `404.html` if so).
- Replace "somewhere north enough" with a real location if Lucca wants one.
- Add vouches as they arrive by email (hand-edit the `#vouch-list` in `#guestbook`; format: name - company/role - one good line).
- Optional: wire `uptime`'s "closet server" line to a real health endpoint on luccaserver.
- Optional: OG image for link previews.
- Cord physics tuning knobs, if it ever feels off: `GRAV`, `DAMPING`, `WAKE_R`, `BRUSH_R`, `STRETCH_PX`, `PULL_PX` at the top of the cord section in `js/main.js`.

## Notes / gotchas
- House style: no em dashes anywhere in this repo - use plain hyphens. Same for anything new you write into it.
- The ghost stores the *previous* session under `lucca.site.v1.ghostPrev`; it only stashes sessions with >=50 cursor samples and >=8s duration.
- Terminal `html()` helper must only ever receive static strings - never user input.
- Google Fonts (Fraunces, Caveat) are the only external requests; the site degrades fine without them.
- The lowercase voice is intentional everywhere on screen; print output comes from the hidden `.print-resume` block, which is professionally capitalized. Keep it in sync with `resume.html` and `C:\Bin\Resume\2026\` when the resume changes.
- Resume dates: WSIB is listed as "May 2025 – Present" - update if the co-op has ended.
- Reduced-motion users get a static cord; taps/keyboard still toggle the theme (physics never wakes, by design).
