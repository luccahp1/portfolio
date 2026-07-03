# portfolio

Lucca Prada's personal portfolio site. Hand-written HTML, CSS, and JavaScript — no framework, no build step, no dependencies.

**Live:** https://luccahp1.github.io/portfolio/

The concept: **a site that remembers you.** Everything it knows lives in the visitor's own localStorage; there is no backend and no analytics.

## Features

- **Adaptive memory** — greets you differently by time of day, visit count, and how long you've been away. Footer keeps a running relationship ("you first showed up 3 weeks ago · visit #6").
- **The ghost** — the site records your cursor locally and replays it on your next visit as a translucent ghost labeled "you, 2 days ago". First-time visitors get Lucca's own recorded wander instead.
- **Pencil mode** (`d`) — draw anywhere on the page. Doodles persist across visits, adapt to the theme, `z` undoes, `x` clears.
- **Terminal** (`/`) — `help`, `whoami`, `cat secrets.txt`, `open outpace`, `sudo hire lucca`, and a permanent record for anyone who tries `rm -rf`.
- **Blueprint mode** (Konami code) — exposes the site's construction lines and margin annotations. Every box confesses its pixel dimensions, and whatever you hover gets measured live.
- **Print = résumé** — `Ctrl+P` swaps the whole site for the real, professional one-page résumé (also at `resume.html`).
- **The lamp cord** — dark mode is a pull-cord in the top right, with a tiny click. It idles with a faint sway, builds real swing momentum if you bat it with repeated hover passes, and if you ignore the warning and keep yanking, it snaps: sparks, a screen flicker, a small glass-pop sound, and a taped-up repair nine seconds later.
- **The tape** — grab the tape holding any project card and pull. The card falls, and a very small "lucca" cursor arrives to pin it back with a real thumbtack (cropped from a vector pack) — a different pin, spot, and angle every time. The pinned note hangs crooked with a curled, shadowed corner. He is not thrilled.
- **The vouch card** — the guestbook, grown up. A popup form (name, email, optional company) that drafts the email in the visitor's own mail app; confirmed vouches get hand-typed into the HTML. The "role" question only exists if they type a company — friends and family never see it.
- **Toasts happen at the scene** — popups appear near whatever triggered them (the lamp's complaints at the lamp, the tape scolding on the note), as slanted handwriting with a paper halo. Happy little mistakes, per Bob Ross.
- **The spoilers** — a footer button that reveals every secret and how to trigger it. Hand-maintained.
- **It learns your name** — `call me maple` in the terminal; greetings use it from then on.
- Small acknowledgments (each once, politely): copy/select-all/idle toasts, a speedrun footer ending with your official time and paper-scrap confetti, seasonal margin notes, an "eavestroughs" hover tooltip, escalating Konami snark, three pencil inks (`c`), a favicon that naps when you leave the tab, and a birthday greeting on July 2.
- Console API (`lucca.ghost()`, `lucca.secrets()`, `lucca.forget()`, …), tab title that misses you, humans.txt, custom 404, a view-source banner.

## Getting started

It's static. Serve the folder with anything:

```
npx http-server . -p 4173
```

Or just open `index.html`.

## Deploying

Any static host works: nginx on luccaserver, GitHub Pages, Netlify. `404.html` is self-contained for host-level error routing.

## Editing content

- Copy lives directly in `index.html` (lowercase on purpose — printing swaps in the hidden `.print-resume` block, which has proper capitals).
- Résumé: edit the `.print-resume` block in `index.html` and `resume.html` together; the full version with phone number lives outside the repo in `C:\Bin\Resume\2026\`.
- Guestbook entries: add `<li>` items in the `#guestbook` section, by hand. That's the system.
- Site birthday / changelog: `BORN` in `js/main.js`, `CHANGELOG` in `js/terminal.js`.
