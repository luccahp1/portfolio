# portfolio

Lucca Prada's personal portfolio site. Hand-written HTML, CSS, and JavaScript — no framework, no build step, no dependencies.

The concept: **a site that remembers you.** Everything it knows lives in the visitor's own localStorage; there is no backend and no analytics.

## Features

- **Adaptive memory** — greets you differently by time of day, visit count, and how long you've been away. Footer keeps a running relationship ("you first showed up 3 weeks ago · visit #6").
- **The ghost** — the site records your cursor locally and replays it on your next visit as a translucent ghost labeled "you, 2 days ago". First-time visitors get Lucca's own recorded wander instead.
- **Pencil mode** (`d`) — draw anywhere on the page. Doodles persist across visits, adapt to the theme, `z` undoes, `x` clears.
- **Terminal** (`/`) — `help`, `whoami`, `cat secrets.txt`, `open outpace`, `sudo hire lucca`, and a permanent record for anyone who tries `rm -rf`.
- **Blueprint mode** (Konami code) — exposes the site's construction lines and margin annotations.
- **Print = résumé** — `Ctrl+P` reformats the entire page into a clean, professional one-page résumé.
- **The lamp cord** — dark mode is a pull-cord in the top right, with a tiny click.
- **Analog guestbook** — no database; guests email in and get hand-typed into the HTML.
- Console API (`lucca.ghost()`, `lucca.forget()`, …), tab title that misses you, humans.txt, custom 404.

## Getting started

It's static. Serve the folder with anything:

```
npx http-server . -p 4173
```

Or just open `index.html`.

## Deploying

Any static host works: nginx on luccaserver, GitHub Pages, Netlify. `404.html` is self-contained for host-level error routing.

## Editing content

- Copy lives directly in `index.html` (lowercase on purpose — the printed résumé re-capitalizes itself).
- Guestbook entries: add `<li>` items in the `#guestbook` section, by hand. That's the system.
- Site birthday / changelog: `BORN` in `js/main.js`, `CHANGELOG` in `js/terminal.js`.
