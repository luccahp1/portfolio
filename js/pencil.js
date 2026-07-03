/* the pencil. press d, draw on the page, and the page keeps it.
   your doodles live in your browser — this is your copy of the site. */

(function () {
  const site = window.__site;
  if (!site) return;
  const { state, save, toast } = site;

  const MAX_POINTS = 6000;

  const canvas = document.createElement("canvas");
  canvas.className = "doodle";
  canvas.setAttribute("aria-hidden", "true");
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  let strokes = [];
  let active = false;
  let drawing = null;
  let saveTimer;

  const btn = document.getElementById("pencil-btn");
  const hud = document.getElementById("pencil-hud");

  /* ---------- sizing & redraw ---------- */
  function inkColor() {
    return getComputedStyle(document.body).color;
  }

  /* three inks on the desk: graphite, the blue pen, the margin red */
  const INKS = ["graphite", "ballpoint", "margin red"];
  let curCol = state.pencilCol || 0;
  function strokeColor(col) {
    const styles = getComputedStyle(document.documentElement);
    if (col === 1) return styles.getPropertyValue("--pen").trim() || inkColor();
    if (col === 2) return styles.getPropertyValue("--red").trim() || inkColor();
    return inkColor();
  }
  function cycleInk() {
    curCol = (curCol + 1) % INKS.length;
    state.pencilCol = curCol;
    save();
    toast(INKS[curCol] + ".");
  }

  function fit() {
    const w = document.documentElement.clientWidth;
    const h = document.documentElement.scrollHeight;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    if (canvas.width === Math.round(w * dpr) && canvas.height === Math.round(h * dpr)) return;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    redraw();
  }

  function drawStroke(s) {
    const pts = s.pts;
    if (pts.length < 2) return;
    ctx.strokeStyle = strokeColor(s.col);
    ctx.globalAlpha = 0.82;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1], b = pts[i];
      ctx.lineWidth = b.w || 2;
      ctx.beginPath();
      const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
      ctx.moveTo(a.x, a.y);
      ctx.quadraticCurveTo(a.x, a.y, mx, my);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function redraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    strokes.forEach(drawStroke);
  }

  /* ---------- persistence ---------- */
  function persist() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      let total = strokes.reduce((n, s) => n + s.pts.length, 0);
      while (total > MAX_POINTS && strokes.length > 1) {
        total -= strokes.shift().pts.length;   // oldest doodles retire first
      }
      state.doodle = { w: document.documentElement.clientWidth, strokes };
      save();
    }, 400);
  }

  function restore() {
    const d = state.doodle;
    if (!d || !d.strokes || !d.strokes.length) return;
    const r = d.w ? document.documentElement.clientWidth / d.w : 1;
    strokes = d.strokes.map((s) => ({
      col: s.col,
      pts: s.pts.map((p) => ({ x: p.x * r, y: p.y * r, w: p.w })),
    }));
    redraw();
  }

  /* ---------- input ---------- */
  function pos(e) {
    return { x: e.pageX, y: e.pageY };
  }

  canvas.addEventListener("pointerdown", (e) => {
    if (!active) return;
    canvas.setPointerCapture(e.pointerId);
    const p = pos(e);
    drawing = { col: curCol, pts: [{ ...p, w: 2 }], last: p, lastT: performance.now() };
    strokes.push(drawing);
    e.preventDefault();
  });

  canvas.addEventListener("pointermove", (e) => {
    if (!active || !drawing) return;
    const p = pos(e);
    const t = performance.now();
    const dist = Math.hypot(p.x - drawing.last.x, p.y - drawing.last.y);
    if (dist < 2) return;
    const speed = dist / Math.max(1, t - drawing.lastT);
    const prevW = drawing.pts[drawing.pts.length - 1].w || 2;
    const w = Math.max(1.3, Math.min(3.1, prevW * 0.7 + (2.9 - speed * 1.6) * 0.3));
    drawing.pts.push({ ...p, w: +w.toFixed(2) });
    drawing.last = p;
    drawing.lastT = t;
    const n = drawing.pts.length;
    drawStroke({ col: drawing.col, pts: drawing.pts.slice(n - 2) });
  });

  function endStroke() {
    if (!drawing) return;
    delete drawing.last;
    delete drawing.lastT;
    if (drawing.pts.length < 2) strokes.pop();
    drawing = null;
    persist();
  }
  canvas.addEventListener("pointerup", endStroke);
  canvas.addEventListener("pointercancel", endStroke);

  /* ---------- toggle ---------- */
  function toggle(force) {
    active = force !== undefined ? force : !active;
    document.body.classList.toggle("drawing", active);
    btn?.classList.toggle("on", active);
    if (hud) hud.hidden = !active;
    if (active) {
      fit();
      if (!state.penciled) {
        state.penciled = true;
        save();
        toast("pencil on. the page is yours — it keeps what you draw.");
      }
    }
  }

  btn?.addEventListener("click", () => toggle());

  document.addEventListener("keydown", (e) => {
    if (!(e.target instanceof Element) || e.target.matches("input, textarea") || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === "d") toggle();
    else if (!active) return;
    else if (e.key === "Escape") toggle(false);
    else if (e.key === "c") cycleInk();
    else if (e.key === "z") { strokes.pop(); redraw(); persist(); }
    else if (e.key === "x") {
      strokes = [];
      redraw();
      persist();
      toast("cleared. like it never happened.");
    }
  });

  /* keep the canvas the size of the page */
  addEventListener("resize", fit);
  if ("ResizeObserver" in window) {
    new ResizeObserver(fit).observe(document.body);
  }

  /* redraw in the new ink when the lights change */
  new MutationObserver(redraw).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });

  fit();
  restore();

  window.__pencil = { toggle };
})();
