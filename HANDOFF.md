# Handoff — portfolio

## Current state
- v1 built and working: single-page site (`index.html`) + `404.html`, `humans.txt`, `favicon.svg`.
- All interactive features implemented in vanilla JS: memory/greetings (`js/main.js`), ghost cursor replay (`js/ghost.js`), pencil drawing (`js/pencil.js`), terminal (`js/terminal.js`).
- Print stylesheet turns the page into a professional résumé (Ctrl+P).
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
- The lowercase voice is intentional everywhere on screen; the print stylesheet re-capitalizes via `::first-letter`.
