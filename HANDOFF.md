# Handoff — portfolio

## Current state
- v1.2 built, tested, deployed: single-page site (`index.html`) + `resume.html`, `404.html`, `humans.txt`, `favicon.svg`.
- Vanilla JS features: memory/greetings/cord/blueprint/confetti (`js/main.js`), ghost cursor replay (`js/ghost.js`), pencil drawing (`js/pencil.js`), terminal (`js/terminal.js`), tape-pull skit (`js/tape.js`).
- v1.2 additions: blueprint mode shows px dimensions (static labels + live hover measurer); lamp cord idles with a sway, builds swing momentum on consecutive hovers, and snaps after 8 rapid pulls (sparks, screen flicker, glass-pop sound, auto-repair with visible tape after 9s); ghost auto-plays at 2.5s every visit + encore at 150s; speedrun ending shows elapsed time + paper-scrap confetti (reveals within 1.2s of load are ignored — that's scroll restoration, not a run); tape on cards is grab-and-pullable → card falls → "lucca" mouse pins it back.
- Ctrl+P on index prints ONLY the real one-page résumé (`.print-resume` block); `resume.html` is the same résumé as a normal page. Web versions omit the phone number on purpose; the full version with phone lives in `C:\Bin\Resume\2026\` (HTML + generated PDF).
- No backend, no build step. Visitor data stays in their localStorage.

## Next steps
- Deployed to GitHub Pages: https://luccahp1.github.io/portfolio/ (repo public, Pages on main/root).
- Optional: point a custom domain at it (update the two hardcoded URLs in `404.html` if so).
- Replace "somewhere north enough" with a real location if Lucca wants one.
- Add real guestbook entries as they arrive by email (hand-edit `#guestbook` list).
- Optional: wire `uptime`'s "closet server" line to a real health endpoint on luccaserver.
- Optional: OG image for link previews.

## Notes / gotchas
- The ghost stores the *previous* session under `lucca.site.v1.ghostPrev`; it only stashes sessions with ≥50 cursor samples and ≥8s duration.
- Terminal `html()` helper must only ever receive static strings — never user input.
- Google Fonts (Fraunces, Caveat) are the only external requests; the site degrades fine without them.
- The lowercase voice is intentional everywhere on screen; print output comes from the hidden `.print-resume` block, which is professionally capitalized. Keep it in sync with `resume.html` and `C:\Bin\Resume\2026\` when the résumé changes.
- Résumé dates: WSIB is listed as "May 2025 – Present" — update if the co-op has ended.
