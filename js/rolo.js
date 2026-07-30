/* the pile. four index cards on a desk: you read the front one, the rest wait
   their turn behind it. flip with the pencil arrows, the thumbtacks, a swipe,
   or the arrow keys while the pile has focus.

   two rules this file will not break:
   1. every transform lands on the .rolo-slot wrapper, never on .card itself.
      the card's transform already has two owners (tilt-a/tilt-b, and the tape
      incident's .fallen/.pinned) and a third would just fight them.
   2. arrow keys are only handled when focus is inside the pile. bound globally
      they would feed the konami blueprint egg in main.js garbage.

   no js means no .rolo-on, which means this stays the plain grid it was born as.
   same for "spread them out on the table" - that's the escape hatch for anyone
   who would rather see all four at once, screen readers included. */

(function () {
  const wrap = document.getElementById("cards");
  if (!wrap) return;

  const slots = Array.from(wrap.querySelectorAll(".rolo-slot"));
  if (slots.length < 2) return;

  const cardOf = (slot) => slot.firstElementChild;
  const nameOf = (slot) => (cardOf(slot).querySelector("h3")?.textContent || "card").trim();

  /* ---------- the controls, built here so a no-js visitor gets none ---------- */
  const ARROW = {
    "-1": '<svg viewBox="0 0 42 20" aria-hidden="true"><path d="M40 10 C 28 7, 16 13, 3 10 M11 4.5 L3 10 L11 15.5"/></svg>',
    "1":  '<svg viewBox="0 0 42 20" aria-hidden="true"><path d="M2 10 C 14 7, 26 13, 39 10 M31 4.5 L39 10 L31 15.5"/></svg>',
  };

  function arm(dir, label) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "rolo-arm";
    b.dataset.dir = String(dir);
    b.setAttribute("aria-label", label);
    b.innerHTML = ARROW[String(dir)];
    b.addEventListener("click", () => go(dir));
    return b;
  }

  const ui = document.createElement("div");
  ui.className = "rolo-ui";

  const bar = document.createElement("div");
  bar.className = "rolo-bar";

  const count = document.createElement("p");
  count.className = "rolo-count";
  count.setAttribute("role", "status");
  count.setAttribute("aria-live", "polite");

  bar.append(arm(-1, "previous card"), count, arm(1, "next card"));

  const tackRow = document.createElement("div");
  tackRow.className = "rolo-tacks";
  tackRow.setAttribute("role", "group");
  tackRow.setAttribute("aria-label", "pick a card");

  const tacks = slots.map((slot, k) => {
    const t = document.createElement("button");
    t.type = "button";
    t.className = "rolo-tack";
    t.setAttribute("aria-label", nameOf(slot));
    t.addEventListener("click", () => to(k));
    tackRow.appendChild(t);
    return t;
  });

  const spreadBtn = document.createElement("button");
  spreadBtn.type = "button";
  spreadBtn.className = "rolo-spread";
  spreadBtn.setAttribute("aria-pressed", "false");
  spreadBtn.addEventListener("click", () => setSpread(!spreadOn));

  ui.append(bar, tackRow, spreadBtn);
  wrap.insertAdjacentElement("afterend", ui);

  /* ---------- state ---------- */
  let i = 0;
  let spreadOn = false;

  function render() {
    const n = slots.length;
    slots.forEach((slot, k) => {
      const d = (k - i + n) % n;
      slot.style.setProperty("--d", d);
      const front = d === 0;
      slot.classList.toggle("is-front", front);
      // only the front card is reachable: the ones behind it are decoration,
      // and tabbing into a card you cannot read is a trap.
      if (front) {
        slot.removeAttribute("inert");
        slot.removeAttribute("aria-hidden");
      } else {
        slot.setAttribute("inert", "");
        slot.setAttribute("aria-hidden", "true");
      }
    });
    count.textContent = "card " + (i + 1) + " of " + n;
    tacks.forEach((t, k) => t.setAttribute("aria-current", k === i ? "true" : "false"));
  }

  function go(dir) {
    if (spreadOn) return;
    const n = slots.length;
    i = (i + dir + n) % n;
    render();
  }

  function to(k) {
    if (spreadOn) return;
    i = k;
    render();
  }

  /* the pile is only as tall as its tallest card, so flipping never makes the
     page jump. measured after .rolo-on lands, because a card is full width in
     the pile and a half-width column in the grid - different heights. */
  function measure() {
    if (spreadOn) return;
    let tall = 0;
    for (const slot of slots) tall = Math.max(tall, cardOf(slot).offsetHeight);
    if (tall) wrap.style.minHeight = tall + "px";
  }

  function setSpread(on) {
    spreadOn = on;
    spreadBtn.setAttribute("aria-pressed", String(on));
    spreadBtn.textContent = on
      ? "ok, stack them back up"
      : "or spread all four out on the table";
    bar.hidden = on;
    tackRow.hidden = on;

    if (on) {
      wrap.classList.remove("rolo-on");
      wrap.style.minHeight = "";
      slots.forEach((slot) => {
        slot.classList.remove("is-front");
        slot.removeAttribute("inert");
        slot.removeAttribute("aria-hidden");
        slot.style.removeProperty("--d");
      });
    } else {
      wrap.classList.add("rolo-on");
      render();
      measure();
    }
  }

  /* ---------- swipe / drag ---------- */
  let drag = null;

  wrap.addEventListener("pointerdown", (e) => {
    if (spreadOn || e.button !== 0) return;
    // the tape has its own pointer handlers, and links deserve their clicks
    if (e.target.closest(".tape, a, button, input, textarea")) return;
    const front = slots[i];
    drag = { x: e.clientX, y: e.clientY, el: front, moved: false };
  });

  wrap.addEventListener("pointermove", (e) => {
    if (!drag) return;
    const dx = e.clientX - drag.x;
    const dy = e.clientY - drag.y;
    if (!drag.moved) {
      // let vertical intent through: that's the page scrolling, not a flip
      if (Math.abs(dx) < 8 || Math.abs(dx) <= Math.abs(dy)) return;
      drag.moved = true;
      wrap.classList.add("rolo-dragging");
    }
    drag.el.style.transform =
      "translate3d(" + dx + "px, " + (Math.abs(dx) * -0.05).toFixed(2) + "px, 0)" +
      " rotate(" + (dx * 0.02).toFixed(2) + "deg)";
  });

  function endDrag(e) {
    if (!drag) return;
    const { el, moved, x } = drag;
    const dx = (e.clientX ?? x) - x;
    drag = null;
    wrap.classList.remove("rolo-dragging");
    el.style.transform = "";          // hand the transform back to the stylesheet
    if (moved && Math.abs(dx) > 60) go(dx < 0 ? 1 : -1);
  }
  wrap.addEventListener("pointerup", endDrag);
  wrap.addEventListener("pointercancel", endDrag);

  /* ---------- keys, scoped to the pile ---------- */
  function onKey(e) {
    if (spreadOn || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); go(1); }
  }
  wrap.addEventListener("keydown", onKey);
  ui.addEventListener("keydown", onKey);

  /* ---------- go ---------- */
  setSpread(false);

  let t = 0;
  addEventListener("resize", () => {
    clearTimeout(t);
    t = setTimeout(measure, 150);
  });
  // fraunces and caveat land late and change every card's height when they do
  if (document.fonts?.ready) document.fonts.ready.then(measure);
  addEventListener("load", measure);
})();
