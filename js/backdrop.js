/* the backdrop. five ways to make the paper move, none of them loud.

   it's one fixed, viewport-sized canvas living at z-index -1, so it never
   touches document height (ask pencil.js how that goes) and never eats a
   click. switch with `bg` in the terminal, shift+B, or lucca.bg().

   every mode is the same shape: init() sizes its own state, step() draws one
   frame. nothing here is saved except which one you picked. */

(function () {
  const site = window.__site;
  if (!site) return;
  const { state, save, toast, prefersReduced } = site;

  const canvas = document.createElement("canvas");
  canvas.className = "backdrop";
  canvas.setAttribute("aria-hidden", "true");
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");

  let W = 0, H = 0, DPR = 1;
  const TAU = Math.PI * 2;

  /* ---------- scroll, wherever it actually lives ---------- */
  const scrollY = () => Math.max(
    window.scrollY || 0,
    document.body.scrollTop || 0,
    document.documentElement.scrollTop || 0
  );

  /* ---------- colours, borrowed from the stylesheet ---------- */
  let INK = [32, 28, 23], PEN = [43, 80, 200];
  const probe = document.createElement("canvas").getContext("2d");
  function rgbOf(name, fallback) {
    const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    if (!v) return fallback;
    probe.fillStyle = "#000";
    probe.fillStyle = v;                    // let the browser normalise it
    const s = probe.fillStyle;
    if (s[0] === "#") {
      return [parseInt(s.slice(1, 3), 16), parseInt(s.slice(3, 5), 16), parseInt(s.slice(5, 7), 16)];
    }
    const m = s.match(/[\d.]+/g);
    return m ? [+m[0], +m[1], +m[2]] : fallback;
  }
  function readColours() {
    INK = rgbOf("--ink-soft", INK);
    PEN = rgbOf("--pen", PEN);
  }
  const rgba = (c, a) => "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")";

  /* ---------- value noise. cheap, seedless, good enough ---------- */
  function hash(x, y) {
    let h = Math.imul(x | 0, 374761393) + Math.imul(y | 0, 668265263);
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }
  const smooth = (t) => t * t * (3 - 2 * t);
  function noise2(x, y) {
    const xi = Math.floor(x), yi = Math.floor(y);
    const u = smooth(x - xi), v = smooth(y - yi);
    const a = hash(xi, yi), b = hash(xi + 1, yi);
    const c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
    return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v;
  }
  function fbm(x, y) {
    return noise2(x, y) * 0.6 + noise2(x * 2.1, y * 2.1) * 0.3 + noise2(x * 4.3, y * 4.3) * 0.1;
  }

  /* =====================================================================
     1. flow - particles dragged through a noise vector field
     ===================================================================== */
  const flow = {
    id: "flow",
    blurb: "ink on a vector field. particles drifting downstream.",
    alpha: 0.5,
    warm: 220,
    init() {
      const n = Math.min(420, Math.round((W * H) / 3400));
      this.p = [];
      for (let i = 0; i < n; i++) this.p.push(this.spawn());
      ctx.clearRect(0, 0, W, H);
    },
    spawn() {
      return { x: Math.random() * W, y: Math.random() * H, life: 60 + Math.random() * 260 };
    },
    step(t) {
      // fade the old trails without painting a background over them
      ctx.globalCompositeOperation = "destination-out";
      ctx.fillStyle = "rgba(0,0,0,0.035)";
      ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = "source-over";

      const sy = scrollY() * 0.12;
      ctx.lineWidth = 1;
      ctx.strokeStyle = rgba(INK, 0.34);
      ctx.beginPath();
      for (const p of this.p) {
        const a = fbm(p.x * 0.0016, (p.y + sy) * 0.0016 + t * 0.035) * TAU * 2;
        const px = p.x, py = p.y;
        p.x += Math.cos(a) * 0.85;
        p.y += Math.sin(a) * 0.85;
        p.life--;
        if (p.life <= 0 || p.x < -20 || p.x > W + 20 || p.y < -20 || p.y > H + 20) {
          Object.assign(p, this.spawn());
          continue;
        }
        ctx.moveTo(px, py);
        ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    },
  };

  /* =====================================================================
     2. topo - marching squares over a field that won't sit still
     ===================================================================== */
  const EDGE = [[0, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 0, 0]]; // corner pairs per edge
  const CASES = [
    [], [[3, 0]], [[0, 1]], [[3, 1]], [[1, 2]], [[3, 0], [1, 2]], [[0, 2]], [[3, 2]],
    [[2, 3]], [[2, 0]], [[0, 1], [2, 3]], [[2, 1]], [[1, 3]], [[1, 0]], [[0, 3]], [],
  ];
  const topo = {
    id: "topo",
    blurb: "contour lines. the ground keeps changing its mind.",
    alpha: 0.55,
    init() {
      this.step_ = 17;
      this.cols = Math.ceil(W / this.step_) + 2;
      this.rows = Math.ceil(H / this.step_) + 2;
      this.f = new Float32Array(this.cols * this.rows);
    },
    step(t) {
      ctx.clearRect(0, 0, W, H);
      const S = this.step_, C = this.cols, R = this.rows, f = this.f;
      const sy = scrollY() * 0.0011;
      for (let j = 0; j < R; j++) {
        for (let i = 0; i < C; i++) {
          f[j * C + i] = fbm(i * 0.055, j * 0.055 + sy + t * 0.028);
        }
      }
      const levels = [0.34, 0.42, 0.5, 0.58, 0.66, 0.74];
      for (let L = 0; L < levels.length; L++) {
        const lv = levels[L];
        // the mid contour gets the blue pen, the rest stay pencil
        ctx.strokeStyle = L === 2 ? rgba(PEN, 0.4) : rgba(INK, 0.3);
        ctx.lineWidth = L === 2 ? 1.2 : 0.9;
        ctx.beginPath();
        for (let j = 0; j < R - 1; j++) {
          for (let i = 0; i < C - 1; i++) {
            const v = [f[j * C + i], f[j * C + i + 1], f[(j + 1) * C + i + 1], f[(j + 1) * C + i]];
            const idx = (v[0] > lv ? 1 : 0) | (v[1] > lv ? 2 : 0) | (v[2] > lv ? 4 : 0) | (v[3] > lv ? 8 : 0);
            const segs = CASES[idx];
            for (let s = 0; s < segs.length; s++) {
              const p1 = this.edge(segs[s][0], v, lv, i, j, S);
              const p2 = this.edge(segs[s][1], v, lv, i, j, S);
              ctx.moveTo(p1[0], p1[1]);
              ctx.lineTo(p2[0], p2[1]);
            }
          }
        }
        ctx.stroke();
      }
    },
    edge(e, v, lv, i, j, S) {
      const [ax, ay, bx, by] = EDGE[e];
      const a = v[e], b = v[(e + 1) % 4];
      const d = b - a;
      const k = Math.abs(d) < 1e-6 ? 0.5 : (lv - a) / d;
      return [(i + ax + (bx - ax) * k) * S - S, (j + ay + (by - ay) * k) * S - S];
    },
  };

  /* =====================================================================
     3. life - conway, taking his time
     ===================================================================== */
  const life = {
    id: "life",
    blurb: "conway. it's alive, barely, and very slowly.",
    alpha: 0.42,
    init() {
      this.cell = 24;
      this.c = Math.ceil(W / this.cell) + 1;
      this.r = Math.ceil(H / this.cell) + 1;
      this.cur = new Uint8Array(this.c * this.r);
      this.prev = new Uint8Array(this.c * this.r);
      this.seed();
      this.last = 0;
      this.stale = 0;
      this.pop = -1;
    },
    seed() {
      for (let i = 0; i < this.cur.length; i++) this.cur[i] = Math.random() < 0.28 ? 1 : 0;
      this.prev.set(this.cur);
    },
    tick() {
      const { c, r, cur } = this;
      const next = new Uint8Array(c * r);
      let pop = 0;
      for (let y = 0; y < r; y++) {
        for (let x = 0; x < c; x++) {
          let n = 0;
          for (let dy = -1; dy <= 1; dy++) {
            for (let dx = -1; dx <= 1; dx++) {
              if (!dx && !dy) continue;
              // the board wraps, so gliders get to leave and come back
              n += cur[((y + dy + r) % r) * c + ((x + dx + c) % c)];
            }
          }
          const alive = cur[y * c + x];
          const v = alive ? (n === 2 || n === 3 ? 1 : 0) : (n === 3 ? 1 : 0);
          next[y * c + x] = v;
          pop += v;
        }
      }
      this.prev = cur;
      this.cur = next;
      // a still life is a dead show. nudge it with fresh soup.
      if (pop === this.pop) this.stale++; else this.stale = 0;
      this.pop = pop;
      if (pop < this.cur.length * 0.02 || this.stale > 6) {
        this.stale = 0;
        const ox = Math.floor(Math.random() * this.c), oy = Math.floor(Math.random() * this.r);
        for (let y = 0; y < 10; y++) {
          for (let x = 0; x < 10; x++) {
            this.cur[((oy + y) % this.r) * this.c + ((ox + x) % this.c)] = Math.random() < 0.4 ? 1 : 0;
          }
        }
      }
    },
    step(t) {
      const RATE = 0.85;                       // seconds per generation
      if (t - this.last > RATE) { this.tick(); this.last = t; }
      const k = Math.min(1, (t - this.last) / RATE);
      ctx.clearRect(0, 0, W, H);
      const S = this.cell, pad = 4.5;
      const off = (scrollY() * 0.05) % S;
      for (let y = 0; y < this.r; y++) {
        for (let x = 0; x < this.c; x++) {
          const i = y * this.c + x;
          // cells fade between generations instead of popping
          const a = this.prev[i] * (1 - k) + this.cur[i] * k;
          if (a < 0.03) continue;
          ctx.fillStyle = rgba(INK, a * 0.5);
          ctx.fillRect(x * S + pad, y * S + pad - off, S - pad * 2, S - pad * 2);
        }
      }
    },
  };

  /* =====================================================================
     4. truchet - arc tiles, flipping one at a time
     ===================================================================== */
  const truchet = {
    id: "truchet",
    blurb: "arc tiles flipping. a maze that redraws itself.",
    alpha: 0.45,
    init() {
      this.cell = 62;
      this.flips = new Map();                  // key -> {at, from}
      this.last = 0;
    },
    step(t) {
      const S = this.cell;
      const sy = scrollY() * 0.08;
      const row0 = Math.floor(sy / S) - 1;
      const cols = Math.ceil(W / S) + 2;
      const rows = Math.ceil(H / S) + 3;

      if (t - this.last > 0.45) {
        this.last = t;
        for (let k = 0; k < 2; k++) {
          const cx = Math.floor(Math.random() * cols);
          const cy = row0 + Math.floor(Math.random() * rows);
          this.flips.set(cx + "," + cy, { at: t, from: this.base(cx, cy) });
        }
        for (const [key, v] of this.flips) if (t - v.at > 3) this.flips.delete(key);
      }

      ctx.clearRect(0, 0, W, H);
      ctx.lineCap = "round";
      for (let j = 0; j < rows; j++) {
        const gy = row0 + j;
        for (let i = 0; i < cols; i++) {
          const key = i + "," + gy;
          const f = this.flips.get(key);
          let orient = this.base(i, gy);
          let a = 0.32;
          if (f) {
            const k = Math.min(1, (t - f.at) / 0.6);
            // fade the old tile out, the flipped one in
            orient = k < 0.5 ? f.from : 1 - f.from;
            a = 0.32 * Math.abs(k - 0.5) * 2;
          }
          if (a < 0.02) continue;
          const x = i * S, y = gy * S - sy;
          if (y > H + S || y < -S * 2) continue;
          ctx.strokeStyle = hash(i, gy) > 0.88 ? rgba(PEN, a + 0.1) : rgba(INK, a);
          ctx.lineWidth = 1.3;
          ctx.beginPath();
          if (orient) {
            ctx.arc(x, y, S / 2, 0, Math.PI / 2);
            ctx.moveTo(x + S, y + S - S / 2);
            ctx.arc(x + S, y + S, S / 2, Math.PI, Math.PI * 1.5);
          } else {
            ctx.arc(x + S, y, S / 2, Math.PI / 2, Math.PI);
            ctx.moveTo(x + S / 2, y + S);
            ctx.arc(x, y + S, S / 2, Math.PI * 1.5, TAU);
          }
          ctx.stroke();
        }
      }
    },
    base(x, y) { return hash(x * 7 + 11, y * 13 + 3) > 0.5 ? 1 : 0; },
  };

  /* =====================================================================
     5. dither - bayer 4x4 over a slow plasma, drawn chunky on purpose
     ===================================================================== */
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const dither = {
    id: "dither",
    blurb: "ordered dithering over a slow plasma. halftone, like cheap print.",
    alpha: 0.32,
    init() {
      this.cell = 7;
      this.off = document.createElement("canvas");
      this.octx = this.off.getContext("2d");
      this.off.width = Math.ceil(W / this.cell);
      this.off.height = Math.ceil(H / this.cell);
      this.img = this.octx.createImageData(this.off.width, this.off.height);
    },
    step(t) {
      const ow = this.off.width, oh = this.off.height;
      const d = this.img.data;
      const sy = scrollY() * 0.02;
      for (let y = 0; y < oh; y++) {
        for (let x = 0; x < ow; x++) {
          // plasma: a couple of slow sines plus noise, so it never tiles
          const v =
            0.5 + 0.28 * Math.sin(x * 0.055 + t * 0.5) +
            0.22 * Math.sin((y + sy) * 0.06 - t * 0.37) +
            0.3 * (fbm(x * 0.02, (y + sy) * 0.02 + t * 0.06) - 0.5);
          const thr = (BAYER[(y & 3) * 4 + (x & 3)] + 0.5) / 16;
          const i = (y * ow + x) * 4;
          const on = v > thr;
          d[i] = INK[0]; d[i + 1] = INK[1]; d[i + 2] = INK[2];
          // it covers half the screen, so it needs a much lighter touch than
          // the line-based modes to land at the same visual weight
          d[i + 3] = on ? 72 : 0;
        }
      }
      this.octx.putImageData(this.img, 0, 0);
      ctx.clearRect(0, 0, W, H);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(this.off, 0, 0, W, H);
      ctx.imageSmoothingEnabled = true;
    },
  };

  /* ---------- the roster ---------- */
  const MODES = [flow, topo, life, truchet, dither];
  const byId = (id) => MODES.find((m) => m.id === id);

  let cur = null;          // the live mode object, or null for `off`
  let raf = 0, t0 = 0, acc = 0, lastFrame = 0;

  function size() {
    /* a hidden or not-yet-laid-out viewport reports 0, and every mode here
       divides by it. clamp to 1 so nothing throws; the resize handler re-inits
       properly once the window has a real size again. */
    const w = Math.max(1, innerWidth || document.documentElement.clientWidth || 0);
    const h = Math.max(1, innerHeight || document.documentElement.clientHeight || 0);
    DPR = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = Math.round(w * DPR);
    canvas.height = Math.round(h * DPR);
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    W = w; H = h;
  }

  function frame(now) {
    raf = requestAnimationFrame(frame);
    if (!cur || document.hidden) return;
    // ~30fps is plenty for something this quiet, and it halves the battery cost
    if (now - lastFrame < 32) return;
    lastFrame = now;
    cur.step((now - t0) / 1000);
  }

  function start() {
    if (!cur) return;
    size();
    cur.init();
    t0 = performance.now();
    canvas.style.opacity = cur.alpha;
    if (prefersReduced) {
      // no animation, but a still frame beats a blank page. warm it up once.
      const n = cur.warm || 1;
      for (let i = 0; i < n; i++) cur.step(i * 0.033);
      return;
    }
    if (!raf) raf = requestAnimationFrame(frame);
  }

  function stop() {
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
    ctx.clearRect(0, 0, W, H);
  }

  function apply(id, quiet) {
    if (id === "off" || id === "none") {
      cur = null; stop();
      canvas.hidden = true;
      state.bg = "off"; save();
      return "backdrop off. just paper again.";
    }
    const m = byId(id);
    if (!m) return "no backdrop called `" + id + "`. try: " + MODES.map((x) => x.id).join(" · ");
    stop();
    cur = m;
    canvas.hidden = false;
    start();
    state.bg = m.id; save();
    if (!quiet) toast("backdrop: " + m.id + " - " + m.blurb, 3600);
    return "backdrop: " + m.id + " - " + m.blurb +
      (prefersReduced ? "\n(your system asked for reduced motion, so it's a still frame.)" : "");
  }

  function next() {
    const i = cur ? MODES.indexOf(cur) : -1;
    return apply(MODES[(i + 1) % MODES.length].id);
  }

  /* ---------- wiring ---------- */
  let rt = 0;
  addEventListener("resize", () => {
    clearTimeout(rt);
    rt = setTimeout(() => { if (cur) start(); }, 150);
  });

  // the inks change with the lights
  new MutationObserver(() => {
    readColours();
    if (cur && prefersReduced) start();
  }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

  document.addEventListener("keydown", (e) => {
    if (e.key !== "B" || !e.shiftKey || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target instanceof Element && e.target.matches("input, textarea")) return;
    e.preventDefault();
    next();
  });

  readColours();
  apply(state.bg || "flow", true);

  window.__backdrop = {
    set: apply,
    next,
    list: () => MODES.map((m) => ({ id: m.id, blurb: m.blurb })),
    current: () => (cur ? cur.id : "off"),
    // draw one frame by hand, at time t (seconds). handy when you want to
    // step through a mode, or when something upstream has starved rAF.
    tick: (t) => { if (cur) cur.step(t || 0); return cur ? cur.id : "off"; },
  };
})();
