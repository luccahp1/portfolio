/* the ghost. this site records your cursor (locally, only locally)
   and next visit, it wanders the page again — a little echo of you.
   first-timers get my ghost instead. i recorded it so nobody's first
   visit feels lonely. */

(function () {
  const site = window.__site;
  if (!site) return;
  const { state, save, toast, prefersReduced, isTouch, rel } = site;

  const SAMPLE_MS = 70;
  const MAX_PTS = 700;
  const MIN_PTS = 50;
  const MIN_DUR = 8000;
  const AUTO_DELAY = 6000;
  const MAX_REPLAY = 35000;

  const docH = () => document.documentElement.scrollHeight;

  /* ---------- record this visit ---------- */
  const rec = { start: Date.now(), w: innerWidth, dh: docH(), pts: [] };
  let lastSample = 0;

  addEventListener("pointermove", (e) => {
    if (e.pointerType && e.pointerType !== "mouse") return;
    const t = Date.now();
    if (t - lastSample < SAMPLE_MS || rec.pts.length >= MAX_PTS) return;
    lastSample = t;
    rec.pts.push({
      t: t - rec.start,
      x: +(e.pageX / innerWidth).toFixed(4),
      y: Math.round(e.pageY),
    });
  }, { passive: true });

  addEventListener("pointerdown", (e) => {
    if (e.pointerType && e.pointerType !== "mouse") return;
    if (rec.pts.length < MAX_PTS) {
      rec.pts.push({
        t: Date.now() - rec.start,
        x: +(e.pageX / innerWidth).toFixed(4),
        y: Math.round(e.pageY),
        c: 1,
      });
    }
  }, { passive: true });

  function stash() {
    if (rec.pts.length < MIN_PTS) return;
    if (rec.pts[rec.pts.length - 1].t < MIN_DUR) return;
    state.ghostPrev = { rec: rec.start, w: rec.w, dh: rec.dh, pts: rec.pts };
    save();
  }
  addEventListener("pagehide", stash);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stash();
  });

  /* the previous session's ghost, captured before this session overwrites it */
  const prev = state.ghostPrev && state.ghostPrev.pts ? state.ghostPrev : null;

  /* ---------- my ghost, for first visits ---------- */
  function luccaPath() {
    const pts = [];
    let t = 0;
    const push = (x, y, dt, c) => { t += dt; pts.push({ t, x, y: Math.round(y), c }); };
    const at = (sel, fx = 0.5, fy = 0.5) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: (r.left + r.width * fx + scrollX) / innerWidth, y: r.top + r.height * fy + scrollY };
    };
    const glide = (from, to, dur, n) => {
      for (let i = 1; i <= n; i++) {
        const p = i / n, e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
        const wobble = Math.sin(p * Math.PI * 3) * 0.004;
        push(from.x + (to.x - from.x) * e + wobble, from.y + (to.y - from.y) * e, dur / n);
      }
    };

    const hello = at("#greeting", 0.1) || { x: 0.2, y: 140 };
    const uL = at("#hello .u", 0.02, 1.1), uR = at("#hello .u", 0.98, 1.1);
    const card = at("#outpace h3", 0.4);
    const guest = at("#guestbook-h", 0.6);
    const cord = at("#cord", 0.5, 0.8);

    let cur = { x: hello.x - 0.1, y: hello.y - 60 };
    pts.push({ t: 0, x: cur.x, y: Math.round(cur.y) });
    glide(cur, hello, 900, 12); cur = hello;
    push(cur.x, cur.y, 500);
    if (uL && uR) {
      glide(cur, uL, 700, 10); cur = uL;
      glide(cur, uR, 1100, 16); cur = uR;   // re-tracing my own underline
      push(cur.x, cur.y, 400);
    }
    if (card) {
      glide(cur, card, 1000, 14); cur = card;
      for (let i = 0; i < 14; i++) {        // a little proud circle around it
        const a = (i / 14) * Math.PI * 2;
        push(card.x + Math.cos(a) * 0.035, card.y + Math.sin(a) * 16, 60);
      }
      cur = { x: card.x + 0.035, y: card.y };
      push(cur.x, cur.y, 600, 1);
    }
    if (guest) {
      glide(cur, guest, 1100, 14); cur = guest;
      push(cur.x + 0.01, cur.y + 4, 300);
      push(cur.x - 0.01, cur.y - 4, 300);
    }
    if (cord) {
      glide(cur, cord, 1000, 12); cur = cord;
      push(cur.x, cur.y, 800);              // considered pulling it. didn't.
    }
    glide(cur, { x: cur.x + 0.08, y: Math.max(0, cur.y - 200) }, 700, 8);
    return { w: innerWidth, dh: docH(), pts, label: "lucca, 2:14 am — checking this thing works" };
  }

  /* ---------- replay ---------- */
  let playing = false;

  function makeGhost(label) {
    const el = document.createElement("div");
    el.className = "ghost";
    el.innerHTML =
      '<svg width="17" height="22" viewBox="0 0 17 22" aria-hidden="true">' +
      '<path d="M1 1 L1 16.5 L5.2 12.8 L7.6 19 L10.4 17.9 L8 11.9 L14 11.6 Z"/></svg>' +
      '<span class="ghost-tag"></span>';
    el.querySelector(".ghost-tag").textContent = label;
    document.body.appendChild(el);
    return el;
  }

  function ping(x, y) {
    const p = document.createElement("div");
    p.className = "ghost-ping";
    p.style.left = x - 4 + "px";
    p.style.top = y - 4 + "px";
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 950);
  }

  function play(which) {
    if (playing) return "one ghost at a time.";
    if (prefersReduced) return "your system asked for less motion, so the ghost is resting.";

    let src, label;
    if (which !== "lucca" && prev) {
      src = prev;
      label = "you, " + rel(Date.now() - prev.rec) + " ago";
    } else {
      src = luccaPath();
      label = src.label;
    }
    if (!src.pts || src.pts.length < 2) return "nothing to replay yet.";

    // map to today's page, gently compress long pauses and long sessions
    const hRatio = src.dh ? Math.min(2, docH() / src.dh) : 1;
    const pts = [];
    let tAcc = 0;
    for (let i = 0; i < src.pts.length; i++) {
      const p = src.pts[i];
      const dt = i === 0 ? 0 : Math.min(1500, p.t - src.pts[i - 1].t);
      tAcc += dt;
      pts.push({ t: tAcc, x: p.x * innerWidth, y: Math.min(docH() - 10, p.y * hRatio), c: p.c });
    }
    const scale = pts[pts.length - 1].t > MAX_REPLAY ? MAX_REPLAY / pts[pts.length - 1].t : 1;
    pts.forEach((p) => (p.t *= scale));

    playing = true;
    const el = makeGhost(label);
    let gx = pts[0].x, gy = pts[0].y;
    el.style.transform = `translate3d(${gx}px, ${gy}px, 0)`;
    requestAnimationFrame(() => el.classList.add("show"));

    const t0 = performance.now() + 400;
    let idx = 0;

    function frame(nowT) {
      const t = nowT - t0;
      while (idx < pts.length - 1 && pts[idx + 1].t <= t) {
        idx++;
        if (pts[idx].c) ping(pts[idx].x, pts[idx].y);
      }
      if (idx >= pts.length - 1) return end();
      const a = pts[idx], b = pts[idx + 1];
      const f = Math.max(0, Math.min(1, (t - a.t) / Math.max(1, b.t - a.t)));
      const tx = a.x + (b.x - a.x) * f, ty = a.y + (b.y - a.y) * f;
      gx += (tx - gx) * 0.35;  // a ghost should drift a little behind itself
      gy += (ty - gy) * 0.35;
      el.style.transform = `translate3d(${gx}px, ${gy}px, 0)`;
      if (document.hidden) return end();
      requestAnimationFrame(frame);
    }
    function end() {
      el.classList.remove("show");
      setTimeout(() => el.remove(), 1300);
      playing = false;
      if (src === prev && !state.ghostExplained) {
        state.ghostExplained = true;
        save();
        toast("that was you, by the way. last visit.", 4200);
      }
    }
    requestAnimationFrame(frame);
    return "…";
  }

  /* ---------- auto-play, once, politely ---------- */
  if (!prefersReduced && !isTouch && innerWidth > 760) {
    setTimeout(() => {
      if (document.hidden) return;
      if (prev || state.visits <= 2) play(prev ? "you" : "lucca");
    }, AUTO_DELAY);
  }

  window.__ghost = { play };
})();
