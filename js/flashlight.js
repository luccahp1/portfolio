/* flashlight.js - uv ink.
   `flashlight` in the terminal (or `f`) kills the lights and hands you a uv torch.
   the page was always covered in invisible notes; the beam is the only way to read them.

   the dark is one big div with a hole in its gradient. moving the beam is a
   translate3d on that div, so it stays on the compositor and never repaints. */
(() => {
  const site = window.__site;
  const R = 150;                // beam radius in px; notes count as found inside ~70% of it
  const FOUND_AFTER = 350;      // ms a note has to sit in the beam before it counts

  // anchor: a section id. at: where the note sits inside it (percent of the section box).
  const NOTES = [
    { anchor: "hello",     at: [62, 4],  tilt: -4, text: "psst. all of this is hand-written. this too." },
    { anchor: "now",       at: [56, 88], tilt: 3,  text: "pull the cord hard. then do it again. i dare you." },
    { anchor: "work",      at: [4, 6],   tilt: -2, text: "grab the tape on a card. it's fine. probably." },
    { anchor: "about",     at: [58, 2],  tilt: 4,  text: "press d and draw on my site. i'll keep it." },
    { anchor: "guestbook", at: [6, 90],  tilt: -3, text: "type race in the terminal. my time is beatable." },
    { anchor: "hi",        at: [50, 6],  tilt: 2,  text: "you found all the uv ink. ok, now you have to email me." },
  ];

  let on = false, room, exitBtn, notes = [], raf = 0, lastInput = 0;
  let x = innerWidth / 2, y = innerHeight / 2, tx = x, ty = y;
  let found = 0, themeBefore;

  function build() {
    room = document.createElement("div");
    room.className = "dark-room";
    room.setAttribute("aria-hidden", "true");
    document.body.appendChild(room);

    exitBtn = document.createElement("button");
    exitBtn.className = "lights-on hand";
    exitBtn.type = "button";
    exitBtn.textContent = "turn the lights back on";
    exitBtn.addEventListener("click", () => toggle(false));
    document.body.appendChild(exitBtn);

    notes = NOTES.flatMap((n) => {
      const host = document.getElementById(n.anchor);
      if (!host) return [];
      host.classList.add("uv-host");
      const el = document.createElement("p");
      el.className = "uv-note";
      el.setAttribute("aria-hidden", "true");
      el.textContent = n.text;
      el.style.left = n.at[0] + "%";
      el.style.top = n.at[1] + "%";
      el.style.setProperty("--tilt", n.tilt + "deg");
      host.appendChild(el);
      return [{ el, inBeamSince: 0, found: false }];
    });
  }

  function aim(px, py) { tx = px; ty = py; lastInput = performance.now(); }
  const onPointer = (e) => aim(e.clientX, e.clientY);
  const onTouch = (e) => { const t = e.touches[0]; if (t) aim(t.clientX, t.clientY); };

  function frame(now) {
    // left alone for a couple of seconds, the beam drifts a little so it looks held
    if (now - lastInput > 2200) {
      const t = now / 1000;
      tx = innerWidth / 2 + Math.sin(t * 0.6) * innerWidth * 0.28;
      ty = innerHeight * 0.45 + Math.sin(t * 0.9 + 1) * innerHeight * 0.2;
    }
    x += (tx - x) * 0.22;
    y += (ty - y) * 0.22;
    room.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    checkNotes(now);
    raf = requestAnimationFrame(frame);
  }

  function checkNotes(now) {
    for (const n of notes) {
      if (n.found) continue;
      const r = n.el.getBoundingClientRect();
      const lit = Math.hypot(r.left + r.width / 2 - x, r.top + r.height / 2 - y) < R * 0.7 + r.width / 3;
      if (!lit) { n.inBeamSince = 0; continue; }
      if (!n.inBeamSince) n.inBeamSince = now;
      else if (now - n.inBeamSince > FOUND_AFTER) discover(n);
    }
  }

  function discover(n) {
    n.found = true;
    n.el.classList.add("found");
    found++;
    if (found === notes.length) {
      site.confetti?.();
      site.toast("all " + notes.length + " found. you have a future in forensics.", 3600);
    } else {
      site.toast("uv ink: " + found + " of " + notes.length, 1400);
    }
  }

  function toggle(force) {
    const next = force === undefined ? !on : force;
    if (next === on) return on ? "already dark in here." : "lights are already on.";
    on = next;
    if (!room) build();
    document.body.classList.toggle("lights-out", on);
    // uv ink is unreadable on cream paper, so the room really goes dark. the
    // visitor's own theme comes back on exit and is never saved over.
    const root = document.documentElement;
    if (on) {
      themeBefore = root.dataset.theme;
      root.dataset.theme = "dark";
    } else if (themeBefore === undefined) delete root.dataset.theme;
    else root.dataset.theme = themeBefore;
    if (on) {
      x = tx = innerWidth / 2; y = ty = innerHeight * 0.45;
      lastInput = performance.now();
      addEventListener("pointermove", onPointer, { passive: true });
      addEventListener("pointerdown", onPointer, { passive: true });
      addEventListener("touchmove", onTouch, { passive: true });
      raf = requestAnimationFrame(frame);
      return "click. lights out. there's writing on the walls - go look.";
    }
    removeEventListener("pointermove", onPointer);
    removeEventListener("pointerdown", onPointer);
    removeEventListener("touchmove", onTouch);
    cancelAnimationFrame(raf);
    return "lights on. the ink's still there, you just can't see it.";
  }

  addEventListener("keydown", (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest?.("input, textarea, [contenteditable]")) return;
    if (document.body.classList.contains("drawing")) return;
    if (e.key === "f") toggle();
    else if (e.key === "Escape" && on) toggle(false);
  });

  window.__flashlight = { toggle };
})();
