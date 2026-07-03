/* the site's memory, and its small manners.
   everything stays in YOUR localStorage. delete it and we've never met. */

(function () {
  const BORN = new Date("2026-07-02T12:00:00");
  const KEY = "lucca.site.v1";
  const SESSION_GAP_MIN = 30;

  const $ = (s) => document.querySelector(s);
  const now = () => Date.now();

  const prefersReduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isTouch = matchMedia("(pointer: coarse)").matches;

  /* ---------- state ---------- */
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
    catch { return {}; }
  }
  let forgotten = false;   // once you ask to be forgotten, nothing re-saves you
  function save() {
    if (forgotten) return;
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch {}
  }

  const state = load();
  const fresh = !state.firstVisit;
  if (fresh) {
    state.firstVisit = now();
    state.visits = 1;
  } else if (now() - (state.lastSeen || 0) > SESSION_GAP_MIN * 60 * 1000) {
    state.visits = (state.visits || 1) + 1;
  }
  const cameBackAfter = state.lastSeen ? now() - state.lastSeen : 0;
  state.lastSeen = now();
  save();
  setInterval(() => { state.lastSeen = now(); save(); }, 30000);

  /* ---------- tiny helpers ---------- */
  function rel(ms) {
    const m = Math.round(ms / 60000);
    if (m < 2) return "moments";
    if (m < 60) return m + " minutes";
    const h = Math.round(m / 60);
    if (h < 36) return h + " hours";
    const d = Math.round(h / 24);
    if (d < 45) return d + " days";
    return Math.round(d / 30) + " months";
  }

  let toastEl, toastTimer;
  // toast(msg, ms, at) - pass at = { el, fixed?, ax?, dy?, shift? } (or a plain
  // { x, y } viewport point) and the note appears near where the thing actually
  // happened, slightly crooked on purpose.
  function toast(msg, ms = 3200, at) {
    ms += 2000;   // toasts linger a little - people kept missing the punchline
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      document.body.appendChild(toastEl);
    }
    toastEl.classList.remove("show");
    toastEl.classList.toggle("anchored", !!(at && (at.el || at.x !== undefined)));
    toastEl.style.cssText = "";
    toastEl.style.setProperty("--toast-rot", (Math.random() * 5 - 2.5).toFixed(1) + "deg");
    if (at && at.x !== undefined) {
      toastEl.style.position = "fixed";
      toastEl.style.left = at.x + "px";
      toastEl.style.top = at.y + "px";
      toastEl.style.transform = "translateX(-50%)";
      toastEl.style.bottom = "auto";
    } else if (at && at.el) {
      const r = at.el.getBoundingClientRect();
      const jx = Math.random() * 20 - 10, jy = Math.random() * 6 - 3;
      const ax = at.ax === undefined ? 0.5 : at.ax;
      const dy = at.dy === undefined ? -40 : at.dy;
      if (at.fixed) {
        toastEl.style.position = "fixed";
        toastEl.style.left = Math.max(8, Math.min(innerWidth - 8, r.left + r.width * ax + jx)) + "px";
        toastEl.style.top = Math.max(8, r.top + dy + jy) + "px";
        toastEl.style.transform = "translateX(" + (at.shift || "-50%") + ")";
      } else {
        toastEl.style.position = "absolute";
        toastEl.style.left = scrollX + r.left + r.width * ax + jx + "px";
        toastEl.style.top = scrollY + r.top + dy + jy + "px";
        toastEl.style.transform = "translateX(-50%)";
      }
      toastEl.style.bottom = "auto";
    }
    toastEl.textContent = msg;
    requestAnimationFrame(() => toastEl.classList.add("show"));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("show"), ms);
  }

  /* ---------- greeting: the site knows you ---------- */
  function greetingLine() {
    const d = new Date();
    const h = d.getHours();
    const late = h >= 23 || h < 5;
    const v = state.visits;
    const name = state.name;

    // the site's birthday outranks everything
    if (d.getMonth() === 6 && d.getDate() === 2) {
      const age = d.getFullYear() - BORN.getFullYear();
      return age < 1
        ? "it's this site's birthday. born today, actually. no gifts - a vouch, maybe."
        : "it's this site's birthday - " + age + " today. no gifts. vouches accepted.";
    }

    if (fresh || v === 1) {
      if (late) return "you're up late. same, honestly.";
      if (h < 12) return "good morning. you're new here.";
      if (h < 18) return "hi. you're new here.";
      return "good evening. you're new here.";
    }
    if (name) {
      if (late) return name + ". it's late. i respect it.";
      if (v <= 4) return "welcome back, " + name + ".";
      return name + "! visit #" + v + ". the locker's still yours.";
    }
    if (late) return "back again - and at this hour. respect.";
    if (v === 2) return "oh - you came back. hi again.";
    if (v <= 4) return "welcome back. visit #" + v + ".";
    if (v <= 9) return "visit #" + v + ". you basically have a locker here now.";
    return "visit #" + v + ". should i just give you a key?";
  }
  const g = $("#greeting");
  if (g) g.textContent = greetingLine();

  function setName(raw) {
    const name = String(raw || "").replace(/\s+/g, " ").trim().slice(0, 24);
    if (!name) return null;
    state.name = name;
    save();
    if (g) g.textContent = "nice to meet you properly, " + name + ".";
    return name;
  }

  /* ---------- footer memory line ---------- */
  const daysAlive = Math.max(1, Math.round((now() - BORN.getTime()) / 86400000));
  const fm = $("#foot-memory");
  if (fm) {
    fm.textContent = fresh
      ? "this site is " + daysAlive + " day" + (daysAlive > 1 ? "s" : "") + " old. it will remember you from now on."
      : "alive " + daysAlive + " day" + (daysAlive > 1 ? "s" : "") + " · you first showed up " + rel(now() - state.firstVisit) +
        " ago · this is visit #" + state.visits +
        (cameBackAfter > 6 * 3600000 ? " · it missed you" : "");
  }

  /* ---------- your local time, ticking ---------- */
  const clock = $("#clock");
  function tick() {
    if (!clock) return;
    const d = new Date();
    clock.textContent =
      String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
  }
  tick();
  setInterval(tick, 15000);

  /* ---------- the lamp cord ---------- */
  function currentTheme() {
    return document.documentElement.dataset.theme ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  function setTheme(t, quiet) {
    document.documentElement.dataset.theme = t;
    state.theme = t;
    save();
    if (!quiet) click();
  }
  if (state.theme) document.documentElement.dataset.theme = state.theme;

  // one tiny triangle blip, reused everywhere something should go "tick"
  let actx;
  function blip(freq) {
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const o = actx.createOscillator(), gn = actx.createGain();
      o.type = "triangle";
      o.frequency.value = freq;
      gn.gain.setValueAtTime(0.06, actx.currentTime);
      gn.gain.exponentialRampToValueAtTime(0.0001, actx.currentTime + 0.07);
      o.connect(gn).connect(actx.destination);
      o.start();
      o.stop(actx.currentTime + 0.08);
    } catch {}
  }
  // a very small, very quiet "click". a lamp should sound like something.
  function click() { blip(currentTheme() === "dark" ? 620 : 880); }

  // a short, quiet "glass gave up" noise for when the cord snaps
  function crack() {
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const t0 = actx.currentTime;
      const buf = actx.createBuffer(1, Math.floor(actx.sampleRate * 0.1), actx.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / d.length, 2);
      const src = actx.createBufferSource();
      src.buffer = buf;
      const hp = actx.createBiquadFilter();
      hp.type = "highpass";
      hp.frequency.value = 1800;
      const gn = actx.createGain();
      gn.gain.setValueAtTime(0.16, t0);
      gn.gain.exponentialRampToValueAtTime(0.001, t0 + 0.12);
      src.connect(hp).connect(gn).connect(actx.destination);
      src.start();
      const o = actx.createOscillator(), g2 = actx.createGain();
      o.type = "sine";
      o.frequency.setValueAtTime(2900, t0);
      o.frequency.exponentialRampToValueAtTime(1400, t0 + 0.09);
      g2.gain.setValueAtTime(0.09, t0);
      g2.gain.exponentialRampToValueAtTime(0.001, t0 + 0.1);
      o.connect(g2).connect(actx.destination);
      o.start();
      o.stop(t0 + 0.12);
    } catch {}
  }

  function sparks(x, y) {
    if (prefersReduced) return;
    for (let i = 0; i < 14; i++) {
      const s = document.createElement("i");
      s.className = "spark";
      s.style.left = x + "px";
      s.style.top = y + "px";
      s.style.setProperty("--dx", (Math.random() * 130 - 65).toFixed(0) + "px");
      s.style.setProperty("--dy", (Math.random() * 100 - 25).toFixed(0) + "px");
      s.style.background = Math.random() < 0.5 ? "var(--pen)" : "#e8b74d";
      document.body.appendChild(s);
      setTimeout(() => s.remove(), 850);
    }
  }

  let cordPulls = [];
  let cordJoked = false;
  let cordSnapped = false;
  let cordBreaks = 0;      // it survives one snap. the second one changes things.
  let cordDead = false;    // duct-taped: the rope is scenery now
  const cordBtn = $("#cord");
  // lamp commentary lands within arm's reach of the lamp - never ON the cord,
  // always on screen, and somewhere a little different every time
  function cordAt() {
    const r = cordBtn.getBoundingClientRect();
    const x = r.left - 140 - Math.random() * 150;               // left of the cord
    const y = r.top + r.height / 2 - 30 + Math.random() * 230;  // beside to below
    return {
      x: Math.max(150, Math.min(innerWidth - 170, x)),
      y: Math.max(14, Math.min(innerHeight - 80, y)),
    };
  }

  // the cord is a real rope now: a chain of verlet nodes under gravity,
  // with hooke's-law-ish distance constraints holding it together.
  // it hangs perfectly still (zero cpu) until the mouse gets close - only
  // then does the physics loop wake up, and it naps again once the cord
  // settles. grab it and pull in any direction: it stretches, and past
  // enough tension the switch gives and the lights flip. swiping through
  // it shoves whichever nodes you graze.
  const cordSvg = cordBtn?.querySelector("svg");
  const cordPathEl = $("#cord-path");
  const cordKnobEl = $("#cord-knob");
  // the tuning knobs. `physics` in the terminal opens live sliders for these.
  // deliberately never written to localStorage: a wild slider session should
  // never outlive a reload, so nobody's lamp can be bricked permanently.
  const PHYS_DEF = {
    segs: 9,        // chain links (70px of cord, same as it ever was)
    grav: 2600,     // px/s^2 in svg space
    damping: 0.985, // air resistance: F_d = -c*v, folded into verlet
    wake: 160,      // physics doesn't exist until you're this close
    brush: 16,      // a swipe this near a node shoves it
    stretch: 28,    // the most the cord will stretch past natural
    pull: 16,       // stretch where the switch gives
  };
  const PH = { ...PHYS_DEF };
  let REST = 70 / PH.segs;
  let nodes = [];
  let ropeEnd = PH.segs;              // last live node (shrinks when snapped)
  let ropeRunning = false, ropeCalm = 0, ropeT = 0;
  let grab = null;                    // { i, cx, cy, x0, y0, t0, fired }
  let mCX = -1e4, mCY = -1e4, mVX = 0, mVY = 0, mT = 0;
  let svgRect = null;

  function ropeRect() {
    if (!svgRect) svgRect = cordSvg.getBoundingClientRect();
    return svgRect;
  }
  addEventListener("resize", () => { svgRect = null; });
  function toLocal(cx, cy) {
    const r = ropeRect();
    return { x: (cx - r.left) * (24 / r.width), y: (cy - r.top) * (90 / r.height) };
  }
  function ropeReset() {
    nodes = [];
    for (let i = 0; i <= PH.segs; i++) nodes.push({ x: 12, y: i * REST, px: 12, py: i * REST });
    ropeRender();
  }
  function ropeRender() {
    let d = "M12 0";
    for (let i = 1; i <= ropeEnd; i++) d += " L" + nodes[i].x.toFixed(1) + " " + nodes[i].y.toFixed(1);
    cordPathEl.setAttribute("d", d);
    // the knob rides just past the last node, along the cord's direction
    const e = nodes[ropeEnd], p = nodes[ropeEnd - 1];
    const dx = e.x - p.x, dy = e.y - p.y, len = Math.hypot(dx, dy) || 1;
    cordKnobEl.setAttribute("cx", (e.x + (dx / len) * 6).toFixed(1));
    cordKnobEl.setAttribute("cy", (e.y + (dy / len) * 6).toFixed(1));
  }

  function ropeStep(dt) {
    // verlet: x_new = x + (x - x_prev)*damping + a*dt^2
    const g = PH.grav * dt * dt;
    for (let i = 1; i <= ropeEnd; i++) {
      const n = nodes[i];
      const vx = (n.x - n.px) * PH.damping, vy = (n.y - n.py) * PH.damping;
      n.px = n.x; n.py = n.y;
      n.x += vx; n.y += vy + g;
    }
    // a swipe near the cord shoves the nodes it grazes (force ∝ mouse velocity)
    if (!grab && mVX * mVX + mVY * mVY > 1) {
      const m = toLocal(mCX, mCY);
      for (let i = 1; i <= ropeEnd; i++) {
        const n = nodes[i];
        if (Math.hypot(n.x - m.x, n.y - m.y) < PH.brush) {
          n.px -= Math.max(-14, Math.min(14, mVX * dt * 0.6));
          n.py -= Math.max(-14, Math.min(14, mVY * dt * 0.6));
        }
      }
    }
    // the grabbed node follows the pointer, clamped to max stretch;
    // tension = how far past the held section's natural length you've pulled
    if (grab) {
      const m = toLocal(grab.cx, grab.cy);
      const natural = grab.i * REST;
      let dx = m.x - 12, dy = m.y;
      const dist = Math.hypot(dx, dy), max = natural + PH.stretch;
      if (dist > max) { dx *= max / dist; dy *= max / dist; }
      const n = nodes[grab.i];
      n.x = 12 + dx; n.y = dy; n.px = n.x; n.py = n.y;
      if (!grab.fired && dist - natural > PH.pull) {
        grab.fired = true;
        endGrab(true);   // the switch gives: lights flip, knob slips free
      }
    }
    // distance constraints, a few relaxation passes. while held, over-long
    // segments only correct partway - that's the stretch you feel.
    for (let k = 0; k < 4; k++) {
      for (let i = 0; i < ropeEnd; i++) {
        const a = nodes[i], b = nodes[i + 1];
        let dx = b.x - a.x, dy = b.y - a.y;
        const d = Math.hypot(dx, dy) || 1e-6;
        let diff = (d - REST) / d;
        if (grab && diff > 0) diff *= 0.55;
        const ox = dx * diff, oy = dy * diff;
        const aPin = i === 0 || (grab && i === grab.i);
        const bPin = grab && i + 1 === grab.i;
        if (aPin && bPin) continue;
        if (aPin) { b.x -= ox; b.y -= oy; }
        else if (bPin) { a.x += ox; a.y += oy; }
        else { a.x += ox * 0.5; a.y += oy * 0.5; b.x -= ox * 0.5; b.y -= oy * 0.5; }
      }
    }
  }

  function ropeEnergy() {
    let e = 0;
    for (let i = 1; i <= ropeEnd; i++) e += Math.abs(nodes[i].x - nodes[i].px) + Math.abs(nodes[i].y - nodes[i].py);
    return e;
  }
  function mouseNearCord() {
    const r = ropeRect();
    return Math.hypot(mCX - (r.left + r.width / 2), mCY - (r.top + r.height * 0.7)) < PH.wake;
  }
  function ropeWake() {
    if (ropeRunning || prefersReduced || !cordSvg) return;
    ropeRunning = true; ropeCalm = 0; ropeT = performance.now();
    requestAnimationFrame(ropeLoop);
  }
  function ropeLoop(t) {
    if (!ropeRunning) return;
    const dt = Math.min(0.033, (t - ropeT) / 1000 || 0.016);
    ropeT = t;
    ropeStep(dt / 2); ropeStep(dt / 2);   // two substeps keep the springs stable
    ropeRender();
    // nap once the cord has settled and you've wandered off
    if (!grab && !mouseNearCord() && ropeEnergy() < 0.3) {
      if (++ropeCalm > 40) { ropeRunning = false; ropeReset(); return; }
    } else ropeCalm = 0;
    requestAnimationFrame(ropeLoop);
  }

  function endGrab(byTension) {
    if (!grab) return;
    const g = grab;
    grab = null;
    if (byTension) pullCord();
    // a plain tap (no real drag) still just toggles, like a normal button
    else if (Math.hypot(g.cx - g.x0, g.cy - g.y0) < 7 && now() - g.t0 < 400) pullCord();
  }

  if (cordSvg && cordPathEl && cordKnobEl) {
    ropeReset();
    addEventListener("pointermove", (e) => {
      const t = performance.now();
      const dtm = Math.min(64, t - mT) || 16;
      const r = ropeRect();
      // mouse velocity in svg px/s, for the brush force
      mVX = ((e.clientX - mCX) * (24 / r.width) / dtm) * 1000;
      mVY = ((e.clientY - mCY) * (90 / r.height) / dtm) * 1000;
      mCX = e.clientX; mCY = e.clientY; mT = t;
      if (grab) { grab.cx = e.clientX; grab.cy = e.clientY; }
      // the optimization: the physics only runs when you're near the cord
      if (!cordDead && mouseNearCord()) ropeWake();
    }, { passive: true });
    addEventListener("pointerup", () => endGrab(false));
    addEventListener("pointercancel", () => { grab = null; });
    cordBtn.addEventListener("pointerdown", (e) => {
      if (cordSnapped || cordDead) return;
      const m = toLocal(e.clientX, e.clientY);
      // grab whichever node is under your finger (never right at the anchor)
      let gi = ropeEnd, best = 1e9;
      for (let i = 2; i <= ropeEnd; i++) {
        const d = Math.hypot(nodes[i].x - m.x, nodes[i].y - m.y);
        if (d < best) { best = d; gi = i; }
      }
      grab = { i: gi, cx: e.clientX, cy: e.clientY, x0: e.clientX, y0: e.clientY, t0: now(), fired: false };
      mCX = e.clientX; mCY = e.clientY;
      ropeWake();
      e.preventDefault();
    });
    // keyboard "clicks" (enter/space) arrive with detail 0; pointer taps are
    // handled by the grab logic above, so this never double-fires
    cordBtn.addEventListener("click", (e) => { if (e.detail === 0) pullCord(); });
  }

  // the lights cut out properly when the cord snaps - a full-screen overlay
  // that stutters, long enough that people actually see it. (an overlay, not
  // a filter on body: filters turn body into a containing block and yank
  // every position:fixed thing out of the viewport.)
  function flickerLights() {
    if (prefersReduced) return;
    const f = document.createElement("div");
    f.className = "flick";
    document.body.appendChild(f);
    setTimeout(() => f.remove(), 2600);
  }

  function flipLights() {
    setTheme(currentTheme() === "dark" ? "light" : "dark");
  }

  function snapCord() {
    cordSnapped = true;
    grab = null;
    cordBreaks++;
    const again = cordBreaks >= 2;
    ropeEnd = Math.min(3, PH.segs);   // a sad little stub stays behind
    ropeRender();
    crack();
    const r = cordBtn.getBoundingClientRect();
    sparks(r.left + r.width / 2, r.top + 10);
    cordBtn.classList.add("snapped");
    if (!prefersReduced) {
      // the loose end goes where gravity says
      const fall = document.createElement("div");
      fall.className = "cord-fall";
      fall.style.left = r.left - 2 + "px";
      fall.style.top = r.top + 22 + "px";
      fall.innerHTML =
        '<svg viewBox="0 0 24 62" width="24" height="62" aria-hidden="true">' +
        '<line x1="12" y1="0" x2="12" y2="48" class="cord-line"/>' +
        '<circle cx="12" cy="54" r="6" class="cord-knob"/></svg>';
      document.body.appendChild(fall);
      setTimeout(() => fall.remove(), 1500);
      flickerLights();
    }
    toast(again
      ? "you broke it AGAIN. ok. hold on. i'm getting the toolbox."
      : "annnd it snapped. lights are stuck like this now. hope it was worth it.", 4200, cordAt());
    setTimeout(again ? condemnCord : repairCord, again ? 4200 : 9000);
  }

  function repairCord() {
    cordSnapped = false;
    cordPulls = [];
    cordBtn.classList.remove("snapped");
    cordBtn.classList.add("repaired");   // the tape stays. a reminder.
    ropeEnd = PH.segs;
    ropeReset();
    toast("fixed it. that was my last spare cord - if this one snaps, i'm getting the duct tape.", 4600, cordAt());
  }

  // the second snap. no more nice repairs: the cord gets duct-taped into
  // scenery, and a real wall switch gets drilled in next to it.
  let wallSwitch = null, wsToasted = false;
  function condemnCord() {
    cordSnapped = false;
    cordDead = true;
    cordPulls = [];
    grab = null;
    cordBtn.classList.remove("snapped");
    cordBtn.classList.add("dead");
    cordBtn.disabled = true;
    ropeEnd = PH.segs;
    ropeReset();
    ropeRunning = false;   // physics is over for this cord
    const t1 = document.createElement("i"), t2 = document.createElement("i");
    t1.className = "ducttape dt1";
    t2.className = "ducttape dt2";
    t1.setAttribute("aria-hidden", "true");
    t2.setAttribute("aria-hidden", "true");
    cordBtn.append(t1, t2);
    makeWallSwitch();
    setTimeout(() => {
      toast("duct tape and a real switch, like a normal house. flip that instead. (miss the string? the terminal knows `rewire`.)", 8200, cordAt());
    }, 800);
  }

  function makeWallSwitch() {
    if (wallSwitch) return;
    wallSwitch = document.createElement("button");
    wallSwitch.className = "wallswitch";
    wallSwitch.id = "wallswitch";
    wallSwitch.setAttribute("aria-label", "toggle the lights (the boring way)");
    wallSwitch.title = "the boring way";
    wallSwitch.innerHTML = '<span class="ws-nub" aria-hidden="true"></span>';
    wallSwitch.addEventListener("click", () => {
      flipLights();
      if (!wsToasted) {
        wsToasted = true;
        toast("click. no rope, no physics, no soul. i hope you're happy.", 4600, cordAt());
      }
    });
    document.body.appendChild(wallSwitch);
  }

  // the way back. only means something once the cord is duct tape.
  function rewire() {
    if (!cordDead) return "the cord is fine. sweet of you to check on it.";
    cordDead = false;
    cordBreaks = 0;
    cordPulls = [];
    cordBtn.disabled = false;
    cordBtn.classList.remove("dead");
    cordBtn.querySelectorAll(".ducttape").forEach((el) => el.remove());
    wallSwitch?.remove();
    wallSwitch = null;
    wsToasted = false;
    ropeEnd = PH.segs;
    ropeReset();
    toast("restrung. one brand new cord. i can't believe i'm giving you a third one.", 5200, cordAt());
    return "rewired. the string is back, the switch is gone. please be gentle. (you won't be.)";
  }

  function pullCord() {
    if (cordSnapped || cordDead) return;
    if (!prefersReduced && nodes.length) {
      nodes[ropeEnd].py -= 10;   // a yank counts as a shove
      ropeWake();
    }
    flipLights();
    if (!state.cordPulled) {
      state.cordPulled = true;
      save();
      toast(currentTheme() === "dark" ? "there. easier on the eyes." : "and the lights are back.", 3200, cordAt());
    }
    const t = now();
    cordPulls = cordPulls.filter((p) => t - p < 6000);
    cordPulls.push(t);
    if (!cordJoked && cordPulls.length >= 4) {
      cordJoked = true;
      toast("the lamp is not a toy. (it is. i literally made it a toy.)", 4000, cordAt());
    } else if (cordJoked && cordPulls.length >= 8) {
      snapCord();
    }
  }

  /* ---------- the physics panel (terminal: `physics`) ----------
     live sliders for the rope. on purpose, none of this is ever persisted:
     reload the page and the cord is factory-fresh, unbrickable. */
  let physPanel = null;
  const PHYS_ROWS = [
    ["grav", "gravity", -4000, 8000, 50],
    ["damping", "damping", 0.9, 1, 0.001],
    ["wake", "wake radius", 40, 400, 5],
    ["brush", "brush radius", 4, 60, 1],
    ["stretch", "max stretch", 0, 120, 1],
    ["pull", "pull to fire", 4, 80, 1],
    ["segs", "segments", 4, 24, 1],
  ];
  function physApply(key) {
    if (key === "segs") {
      REST = 70 / PH.segs;
      ropeEnd = cordSnapped ? Math.min(3, PH.segs) : PH.segs;
      ropeReset();
    }
    if (!cordDead) ropeWake();
  }
  function physToggle() {
    if (prefersReduced) return "your system asked for reduced motion, so the cord doesn't simulate. sliders would just be lying to you.";
    if (physPanel) { physPanel.remove(); physPanel = null; return false; }
    physPanel = document.createElement("div");
    physPanel.className = "phys-panel";
    const title = document.createElement("p");
    title.className = "phys-title hand";
    title.textContent = "cord physics";
    const x = document.createElement("button");
    x.className = "phys-x linkish mono";
    x.textContent = "×";
    x.setAttribute("aria-label", "close the physics panel");
    x.addEventListener("click", physToggle);
    title.appendChild(x);
    physPanel.appendChild(title);
    const vals = [];
    for (const [key, label, min, max, step] of PHYS_ROWS) {
      const row = document.createElement("label");
      row.className = "phys-row mono";
      const name = document.createElement("span");
      name.textContent = label;
      const val = document.createElement("b");
      val.textContent = String(PH[key]);
      const inp = document.createElement("input");
      inp.type = "range";
      inp.min = min; inp.max = max; inp.step = step;
      inp.value = PH[key];
      inp.addEventListener("input", () => {
        PH[key] = +inp.value;
        val.textContent = String(PH[key]);
        physApply(key);
      });
      vals.push([key, val, inp]);
      row.append(name, val, inp);
      physPanel.appendChild(row);
    }
    const reset = document.createElement("button");
    reset.className = "phys-reset mono";
    reset.textContent = "factory settings";
    reset.addEventListener("click", () => {
      Object.assign(PH, PHYS_DEF);
      for (const [key, val, inp] of vals) { inp.value = PH[key]; val.textContent = String(PH[key]); }
      physApply("segs");
    });
    const note = document.createElement("p");
    note.className = "phys-note mono";
    note.textContent = cordDead
      ? "the cord is duct-taped right now, so it won't move. also: nothing here is saved."
      : "nothing here is saved. reload = factory settings.";
    physPanel.append(reset, note);
    document.body.appendChild(physPanel);
    return true;
  }

  /* ---------- tab title misses you (the favicon takes a nap) ---------- */
  const realTitle = document.title;
  const favicon = $("#favicon");
  const favAwake = favicon ? favicon.href : "";
  // same little "l." but lying down for a nap
  const favAsleep = "data:image/svg+xml," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' +
    '<rect width="64" height="64" rx="14" fill="#f7f3ea"/>' +
    '<rect width="64" height="64" rx="14" fill="none" stroke="#201c17" stroke-opacity=".2" stroke-width="2"/>' +
    '<text x="20" y="46" font-family="Georgia, serif" font-style="italic" font-weight="600" font-size="40" fill="#201c17" transform="rotate(90 30 38)">l</text>' +
    '<text x="40" y="26" font-family="Georgia, serif" font-size="15" fill="#5f5749">z</text>' +
    '<text x="48" y="18" font-family="Georgia, serif" font-size="11" fill="#5f5749">z</text>' +
    "</svg>"
  );
  let hiddenAt = 0;
  let loyaltyNoted = false;
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      hiddenAt = now();
      document.title = "come back :(";
      if (favicon) favicon.href = favAsleep;
    } else {
      document.title = realTitle;
      if (favicon) favicon.href = favAwake;
      if (hiddenAt && now() - hiddenAt > 45 * 60000 && !loyaltyNoted) {
        loyaltyNoted = true;
        toast("you kept this tab open the whole time. loyalty.", 4000);
      }
    }
  });

  /* ---------- you read the whole thing (or speedran it) ---------- */
  // trackpads scroll in many small steps, mice in big chunky ones. anyone
  // scrolling trackpad-style gets a fairer speedrun clock.
  let wheelSeen = 0, wheelSmall = 0;
  addEventListener("wheel", (e) => {
    if (wheelSeen >= 40) return;
    wheelSeen++;
    if (e.deltaMode === 0 && Math.abs(e.deltaY) > 0 && Math.abs(e.deltaY) < 40) wheelSmall++;
  }, { passive: true });
  const padLike = () => wheelSeen >= 5 && wheelSmall / wheelSeen > 0.6;

  let speedStart = now();
  let raceRun = false;        // set by `race` so its finish always celebrates
  let rearmSpeedrun = null;   // the `race` command resets the clock through this
  const foot = $(".foot"), footRead = $("#foot-read");
  if (foot && footRead) {
    const footReadDefault = footRead.textContent;
    const footEnd = $(".spoilers") || foot;
    let revealed = false;
    let io = null;
    // your fastest run, kept in localStorage - a real stat, unlike the physics
    // sliders. the finish shows this best time next to the one you just ran.
    const fmt = (ms) => (ms / 1000).toFixed(2);
    const finishLine = (elapsed, isRace) => {
      const prev = state.raceBest || 0;
      const isRecord = !prev || elapsed < prev;
      if (isRecord) { state.raceBest = elapsed; save(); }
      const lead = isRace
        ? "race complete - your time: " + fmt(elapsed) + "s. "
        : "you speedran my website. your time: " + fmt(elapsed) + "s. ";
      if (isRecord && prev) return lead + "new record, beating your old best of " + fmt(prev) + "s!";
      if (isRecord)         return lead + "that's your first record - the highscore to beat.";
      return lead + "your best is still " + fmt(prev) + "s.";
    };
    const reveal = () => {
      if (revealed) return;
      revealed = true;
      const elapsed = now() - speedStart;
      const isRace = raceRun;
      raceRun = false;
      const limit = padLike() ? 15000 : 9000;
      // a race always celebrates, whatever the time; a passive run only when
      // it's plausibly a speedrun - over ~1.2s (not the browser restoring
      // scroll) and under the window (not someone actually reading)
      if (isRace || (elapsed > 1200 && elapsed < limit)) {
        footRead.textContent = finishLine(elapsed, isRace);
        confetti();
      }
      footRead.hidden = false;
      removeEventListener("scroll", nearBottom);
      io?.disconnect();
    };
    // suspenders: plain scroll math
    const nearBottom = () => {
      if (innerHeight + scrollY >= document.documentElement.scrollHeight - 120) reveal();
    };
    // belt: intersection observer on the very last thing in the footer
    const arm = () => {
      if ("IntersectionObserver" in window) {
        io = new IntersectionObserver((entries) => {
          if (entries.some((e) => e.isIntersecting)) reveal();
        }, { threshold: 0.15 });
        io.observe(footEnd);
      }
      addEventListener("scroll", nearBottom, { passive: true });
    };
    arm();
    rearmSpeedrun = () => {
      io?.disconnect();
      removeEventListener("scroll", nearBottom);
      revealed = false;
      footRead.hidden = true;
      footRead.textContent = footReadDefault;
      speedStart = now();
      arm();
    };
  }

  /* ---------- the race (terminal: `race`) ----------
     a proper starting line for speedrunners: back to the top, scrolling
     locked, one very large checkered flag, three beeps, GO. */
  let racing = false;
  function race() {
    if (racing) return "one race at a time.";
    racing = true;
    scrollTo({ top: 0, behavior: "auto" });
    const keys = ["ArrowDown", "ArrowUp", "PageDown", "PageUp", "Home", "End", " ", "Spacebar"];
    const stopKeys = (e) => { if (keys.includes(e.key)) e.preventDefault(); };
    const stopScroll = (e) => e.preventDefault();
    document.documentElement.style.overflow = "hidden";
    addEventListener("wheel", stopScroll, { passive: false });
    addEventListener("touchmove", stopScroll, { passive: false });
    addEventListener("keydown", stopKeys);
    const unlock = () => {
      document.documentElement.style.overflow = "";
      removeEventListener("wheel", stopScroll);
      removeEventListener("touchmove", stopScroll);
      removeEventListener("keydown", stopKeys);
    };
    const banner = document.createElement("div");
    banner.className = "race-banner";
    banner.innerHTML = '<div class="race-flag"></div><span class="race-count display"></span>';
    const count = banner.querySelector(".race-count");
    document.body.appendChild(banner);
    let n = 3;
    count.textContent = "3";
    blip(520);
    const iv = setInterval(() => {
      n--;
      if (n > 0) {
        count.textContent = String(n);
        blip(520);
        return;
      }
      clearInterval(iv);
      count.textContent = "GO!";
      blip(1040);
      unlock();                 // the page is yours again
      rearmSpeedrun?.();        // and the clock starts NOW
      raceRun = true;           // whatever their time, the finish gets confetti
      banner.classList.add("done");
      setTimeout(() => { banner.remove(); racing = false; }, 900);
    }, 1000);
    return "on your marks…";
  }

  /* ---------- paper-scrap confetti, for the speedrunners ---------- */
  function confetti() {
    if (prefersReduced) return;
    const colors = ["var(--pen)", "var(--red)", "#e8c96f", "var(--ink-soft)"];
    for (let i = 0; i < 60; i++) {
      const c = document.createElement("i");
      c.className = "confetti";
      c.style.left = Math.random() * 100 + "vw";
      c.style.background = colors[i % colors.length];
      c.style.width = (5 + Math.random() * 4).toFixed(1) + "px";
      c.style.height = (8 + Math.random() * 6).toFixed(1) + "px";
      c.style.setProperty("--cx", (Math.random() * 160 - 80).toFixed(0) + "px");
      c.style.setProperty("--rot", (Math.random() * 720 - 360).toFixed(0) + "deg");
      c.style.animationDuration = (1.3 + Math.random() * 1.1).toFixed(2) + "s";
      c.style.animationDelay = (Math.random() * 0.25).toFixed(2) + "s";
      document.body.appendChild(c);
      setTimeout(() => c.remove(), 3000);
    }
  }

  /* ---------- konami → blueprint mode ---------- */
  const SEQ = ["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","b","a"];
  let seqAt = 0;
  const BP_NOTES = [
    { sel: "#hello h1", text: "44rem column. trust me.", dx: 10, dy: -34 },
    { sel: "#outpace", text: "rotate(-0.5deg) - barely, but you feel it", dx: 0, dy: -30 },
    { sel: ".tape", text: "the tape is one rectangle and a dream", dx: 60, dy: -6 },
    { sel: "#guestbook-h", text: "vouch backend: my inbox. verification: my eyeballs", dx: 180, dy: 4 },
    { sel: ".foot", text: "the ghost you saw was real. well. local.", dx: 10, dy: -26 },
  ];
  let bpEls = [];
  let bpCount = 0;
  let bpLive = null;

  function bpPlace() {
    bpEls.forEach((el) => el.remove());
    bpEls = [];
    for (const n of BP_NOTES) {
      const t = document.querySelector(n.sel);
      if (!t) continue;
      const r = t.getBoundingClientRect();
      const el = document.createElement("span");
      el.className = "bp-note";
      el.textContent = n.text;
      el.style.left = window.scrollX + r.left + n.dx + "px";
      el.style.top = window.scrollY + r.top + n.dy + "px";
      document.body.appendChild(el);
      bpEls.push(el);
    }
    // every box confesses its size
    document.querySelectorAll("section, .card, h1, .top, .foot, .spoiler-panel:not([hidden])")
      .forEach((t) => {
        const r = t.getBoundingClientRect();
        if (r.width < 40 || r.height < 14) return;
        const el = document.createElement("span");
        el.className = "bp-dim";
        el.textContent = Math.round(r.width) + " × " + Math.round(r.height);
        el.style.left = Math.max(4, window.scrollX + r.right - 74) + "px";
        el.style.top = window.scrollY + r.top - 9 + "px";
        document.body.appendChild(el);
        bpEls.push(el);
      });
  }

  function bpMeasure(e) {
    if (!bpLive) return;
    const t = document.elementFromPoint(e.clientX, e.clientY);
    if (!t || t === document.documentElement) return;
    const r = t.getBoundingClientRect();
    const cls = typeof t.className === "string" && t.className.split(" ")[0];
    bpLive.textContent =
      t.tagName.toLowerCase() + (cls ? "." + cls : "") + " - " +
      Math.round(r.width) + " × " + Math.round(r.height) + " px";
    bpLive.style.left = Math.min(innerWidth - 190, e.clientX + 14) + "px";
    bpLive.style.top = e.clientY + 18 + "px";
  }

  function blueprint(force) {
    const on = force !== undefined ? force : !document.body.classList.contains("blueprint");
    document.body.classList.toggle("blueprint", on);
    bpEls.forEach((el) => el.remove());
    bpEls = [];
    if (bpLive) { bpLive.remove(); bpLive = null; }
    removeEventListener("pointermove", bpMeasure);
    if (on) {
      bpPlace();
      bpLive = document.createElement("div");
      bpLive.id = "bp-live";
      bpLive.textContent = "hover anything - it will confess its size";
      document.body.appendChild(bpLive);
      addEventListener("pointermove", bpMeasure, { passive: true });
      const lines = [
        "blueprint mode. this is how it looks in my head.",
        "again? ok, architect.",
        "you can just live here at this point.",
      ];
      toast(lines[Math.min(bpCount++, lines.length - 1)]);
      if (!state.konami) { state.konami = true; save(); }
    }
  }
  addEventListener("resize", () => {
    if (document.body.classList.contains("blueprint")) bpPlace();
  });
  document.addEventListener("keydown", (e) => {
    if (e.target instanceof Element && e.target.matches("input, textarea")) return;
    const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    seqAt = k === SEQ[seqAt] ? seqAt + 1 : (k === SEQ[0] ? 1 : 0);
    if (seqAt === SEQ.length) { seqAt = 0; blueprint(); }
  });

  /* ---------- a word to the people in the console ---------- */
  const css1 = "font-family:Georgia,serif;font-size:14px;";
  const css2 = "font-family:monospace;font-size:12px;color:#888;";
  console.log("%coh, hi. you look like someone who reads source code.", css1);
  console.log(
    "%csecrets, since you came all the way down here:\n" +
    "  d            → pencil. draw on the site. it keeps your doodles.\n" +
    "  /            → a terminal. of course there's a terminal.\n" +
    "  ↑↑↓↓←→←→ b a → blueprint mode.\n" +
    "  ctrl+p       → the whole site prints as my résumé.\n" +
    "  race/physics → newer terminal toys. hover the header name, too.\n" +
    "  lucca.*      → yes, there's an api. try lucca.ghost()\n\n" +
    "or press the spoiler button at the very bottom like a quitter.\n" +
    "source: https://github.com/luccahp1/portfolio - handwritten, ghosts included.", css2
  );

  /* ---------- small acknowledgments (each fires once, politely) ---------- */
  let idleTimer, idleNoted = false, copyNoted = false, allNoted = false;
  function armIdle() {
    clearTimeout(idleTimer);
    if (idleNoted || document.hidden) return;
    idleTimer = setTimeout(() => {
      idleNoted = true;
      toast("no rush. i'm a website. i have nowhere to be.", 4000);
    }, 75000);
  }
  ["pointermove", "keydown", "scroll", "pointerdown"].forEach((ev) =>
    addEventListener(ev, armIdle, { passive: true })
  );
  armIdle();

  document.addEventListener("copy", () => {
    if (copyNoted) return;
    copyNoted = true;
    toast("copied. quote me kindly.");
  });

  document.addEventListener("keydown", (e) => {
    if (allNoted || !(e.ctrlKey || e.metaKey) || e.key !== "a") return;
    if (e.target instanceof Element && e.target.matches("input, textarea")) return;
    allNoted = true;
    toast("all of it? flattering.");
  });

  /* ---------- the seasonal margin note ---------- */
  const season = $("#season-note");
  if (season) {
    const m = new Date().getMonth();
    season.textContent =
      m === 11 || m <= 1 ? "the eavestroughs are frozen. the server heats the house."
      : m <= 3 ? "thaw season. peak eavestrough."
      : m <= 7 ? "eavestrough off-season. the fan carries the household."
      : "leaf season. the eavestroughs' super bowl.";
    season.hidden = false;
  }

  /* ---------- courtesy, if your system asked for less motion ---------- */
  if (prefersReduced && fm) {
    const p = document.createElement("p");
    p.className = "mono micro";
    p.textContent = "motion is reduced because your system asked. the ghost respects that.";
    fm.insertAdjacentElement("afterend", p);
  }

  /* ---------- the spoilers ---------- */
  const spBtn = $("#spoiler-btn"), spPanel = $("#spoiler-panel");
  if (spBtn && spPanel) {
    spBtn.addEventListener("click", () => {
      const opening = spPanel.hidden;
      spPanel.hidden = !opening;
      spBtn.setAttribute("aria-expanded", String(opening));
      spBtn.textContent = opening ? "ok, hide them again" : "ok fine - reveal every secret";
      if (opening) {
        spPanel.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth", block: "nearest" });
        if (!state.spoiled) {
          state.spoiled = true;
          save();
          toast("brave. most people like not knowing.");
        }
      }
    });
  }

  /* ---------- the public api (it felt right) ---------- */
  window.lucca = {
    lights: () => { cordDead ? flipLights() : pullCord(); },
    blueprint: () => blueprint(),
    ghost: () => window.__ghost?.play() || "the ghost isn't awake yet. give the page a second.",
    draw: () => window.__pencil?.toggle() || "pencil's still sharpening.",
    terminal: () => window.__term?.open() || "terminal's booting.",
    secrets: () => { spBtn?.click(); return "spoilers, served."; },
    race,
    physics: physToggle,
    rewire,
    forget: () => {
      // the latch matters: without it, the 30s heartbeat and the ghost's
      // pagehide stash would quietly re-save everything we just deleted
      forgotten = true;
      try { localStorage.removeItem(KEY); } catch {}
      toast("done. we've never met. reloading so you can see i mean it…", 3800);
      setTimeout(() => location.reload(), 2200);
      return "memory wiped. reloading as strangers…";
    },
  };

  /* shared bits for the other files */
  window.__site = { state, save, toast, prefersReduced, isTouch, rel, BORN, setName };
})();
