/* the tape. it's load-bearing, until someone tugs it.
   then a very small lucca has to come fix things. */

(function () {
  const site = window.__site;
  if (!site) return;
  const { toast, prefersReduced } = site;

  let pulls = 0;

  document.querySelectorAll(".card .tape").forEach((tape) => {
    let start = null;
    tape.addEventListener("pointerdown", (e) => {
      start = { x: e.clientX, y: e.clientY };
      try { tape.setPointerCapture(e.pointerId); } catch {}
      e.preventDefault();
    });
    tape.addEventListener("pointermove", (e) => {
      if (!start) return;
      if (Math.hypot(e.clientX - start.x, e.clientY - start.y) > 32) {
        start = null;
        peel(tape);
      }
    });
    const drop = () => (start = null);
    tape.addEventListener("pointerup", drop);
    tape.addEventListener("pointercancel", drop);
  });

  function peel(tape) {
    const card = tape.closest(".card");
    if (!card || card.dataset.pinned) return;
    card.dataset.pinned = "1";
    tape.classList.add("peeled");
    setTimeout(() => tape.remove(), prefersReduced ? 0 : 600);
    card.classList.add("fallen");
    setTimeout(() => sendLucca(card), prefersReduced ? 150 : 900);
  }

  function placePin(card) {
    const r = card.getBoundingClientRect();
    const pin = document.createElement("span");
    pin.className = "pin";
    // measured while fallen; the card rises ~13px to meet the pin
    pin.style.left = scrollX + r.left + r.width / 2 - 7 + "px";
    pin.style.top = scrollY + r.top - 20 + "px";
    document.body.appendChild(pin);
    card.classList.remove("fallen");
    card.classList.add("pinned");
    pulls++;
    toast(
      pulls === 1
        ? "hey! why you tryna destroy my website?"
        : "aw man. i lowkey gotta buy better tape.",
      4200
    );
  }

  function sendLucca(card) {
    if (prefersReduced) return placePin(card);

    const r = card.getBoundingClientRect();
    const tx = scrollX + r.left + r.width / 2 - 8;
    const ty = scrollY + r.top - 24;

    const m = document.createElement("div");
    m.className = "lmouse";
    m.innerHTML =
      '<svg width="17" height="22" viewBox="0 0 17 22" aria-hidden="true">' +
      '<path d="M1 1 L1 16.5 L5.2 12.8 L7.6 19 L10.4 17.9 L8 11.9 L14 11.6 Z"/></svg>' +
      '<span class="lmouse-tag">lucca</span>';
    const fx = scrollX + innerWidth + 30;
    const fy = ty + 80;
    m.style.transform = `translate3d(${fx}px, ${fy}px, 0)`;
    document.body.appendChild(m);

    const t0 = performance.now(), D = 950;
    function arrive(t) {
      const p = Math.min(1, (t - t0) / D);
      const e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      m.style.transform = `translate3d(${fx + (tx - fx) * e}px, ${fy + (ty - fy) * e}px, 0)`;
      if (p < 1) return requestAnimationFrame(arrive);
      setTimeout(() => {
        placePin(card);
        const t1 = performance.now();
        (function leave(t2) {
          const q = Math.min(1, (t2 - t1) / 800);
          m.style.opacity = String(1 - q);
          m.style.transform = `translate3d(${tx + q * 220}px, ${ty - q * 70}px, 0)`;
          q < 1 ? requestAnimationFrame(leave) : m.remove();
        })(t1);
      }, 380);
    }
    requestAnimationFrame(arrive);
  }
})();
