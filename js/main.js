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
  function save() {
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
  // toast(msg, ms, at) — pass at = { el, fixed?, ax?, dy?, shift? } and the note
  // appears near where the thing actually happened, slightly crooked on purpose.
  function toast(msg, ms = 3200, at) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      document.body.appendChild(toastEl);
    }
    toastEl.classList.remove("show");
    toastEl.classList.toggle("anchored", !!(at && at.el));
    toastEl.style.cssText = "";
    toastEl.style.setProperty("--toast-rot", (Math.random() * 5 - 2.5).toFixed(1) + "deg");
    if (at && at.el) {
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
        ? "it's this site's birthday. born today, actually. no gifts — a vouch, maybe."
        : "it's this site's birthday — " + age + " today. no gifts. vouches accepted.";
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
    if (late) return "back again — and at this hour. respect.";
    if (v === 2) return "oh — you came back. hi again.";
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

  // a very small, very quiet "click". a lamp should sound like something.
  let actx;
  function click() {
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const o = actx.createOscillator(), gn = actx.createGain();
      o.type = "triangle";
      o.frequency.value = currentTheme() === "dark" ? 620 : 880;
      gn.gain.setValueAtTime(0.06, actx.currentTime);
      gn.gain.exponentialRampToValueAtTime(0.0001, actx.currentTime + 0.07);
      o.connect(gn).connect(actx.destination);
      o.start();
      o.stop(actx.currentTime + 0.08);
    } catch {}
  }

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
  const cordBtn = $("#cord");
  // lamp commentary happens at the lamp, not across the room
  const cordAt = () => ({ el: cordBtn, fixed: true, dy: 104, shift: "-78%" });

  // the cord idles with a tiny sway. bat it back and forth — consecutive
  // passes hit harder, and it takes a while to calm back down.
  let swingM = 0, swingTimer, lastEnter = 0;
  function setSwing() {
    if (!cordBtn) return;
    const amp = Math.min(1.1 + swingM * 3.2, 24);
    const spd = Math.max(1.8 - swingM * 0.14, 0.65);
    cordBtn.style.setProperty("--amp", amp.toFixed(1) + "deg");
    cordBtn.style.setProperty("--spd", spd.toFixed(2) + "s");
  }
  function nudgeSwing(strength) {
    if (prefersReduced) return;
    swingM = Math.min(swingM + strength, 7);
    setSwing();
    clearInterval(swingTimer);
    swingTimer = setInterval(() => {
      swingM *= 0.72;
      if (swingM < 0.15) { swingM = 0; clearInterval(swingTimer); }
      setSwing();
    }, 700);
  }
  setSwing();
  cordBtn?.addEventListener("pointerenter", () => {
    const t = now();
    nudgeSwing(t - lastEnter < 2500 ? 1.6 : 0.7);
    lastEnter = t;
  });

  function snapCord() {
    cordSnapped = true;
    swingM = 0;
    setSwing();
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
      document.documentElement.classList.add("flicker");
      setTimeout(() => document.documentElement.classList.remove("flicker"), 950);
    }
    toast("annnd it snapped. lights are stuck like this now. hope it was worth it.", 4200, cordAt());
    setTimeout(() => {
      cordSnapped = false;
      cordPulls = [];
      cordBtn.classList.remove("snapped");
      cordBtn.classList.add("repaired");   // the tape stays. a reminder.
      toast("fixed it. that was my last cord, so.", 3800, cordAt());
    }, 9000);
  }

  function pullCord() {
    if (cordSnapped) return;
    nudgeSwing(1.2);   // a yank counts as a shove
    setTheme(currentTheme() === "dark" ? "light" : "dark");
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
  cordBtn?.addEventListener("click", pullCord);

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
  const loadedAt = now();
  const foot = $(".foot"), footRead = $("#foot-read");
  if (foot && footRead) {
    let revealed = false;
    const reveal = () => {
      if (revealed) return;
      revealed = true;
      const elapsed = now() - loadedAt;
      // under 1.2s isn't a speedrun — that's the browser restoring your scroll
      if (elapsed > 1200 && elapsed < 9000) {
        footRead.textContent =
          "you speedran my website. bottom in " + (elapsed / 1000).toFixed(2) + "s. record pace.";
        confetti();
      }
      footRead.hidden = false;
      removeEventListener("scroll", nearBottom);
    };
    // belt: intersection observer on the very last thing in the footer
    const footEnd = $(".spoilers") || foot;
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((entries) => {
        if (entries.some((e) => e.isIntersecting)) { reveal(); io.disconnect(); }
      }, { threshold: 0.15 });
      io.observe(footEnd);
    }
    // suspenders: plain scroll math
    const nearBottom = () => {
      if (innerHeight + scrollY >= document.documentElement.scrollHeight - 120) reveal();
    };
    addEventListener("scroll", nearBottom, { passive: true });
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
    { sel: "#outpace", text: "rotate(-0.5deg) — barely, but you feel it", dx: 0, dy: -30 },
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
      t.tagName.toLowerCase() + (cls ? "." + cls : "") + " — " +
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
      bpLive.textContent = "hover anything — it will confess its size";
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
    "  lucca.*      → yes, there's an api. try lucca.ghost()\n\n" +
    "or press the spoiler button at the very bottom like a quitter.\n" +
    "source: https://github.com/luccahp1/portfolio — handwritten, ghosts included.", css2
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
      spBtn.textContent = opening ? "ok, hide them again" : "ok fine — reveal every secret";
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
    lights: pullCord,
    blueprint: () => blueprint(),
    ghost: () => window.__ghost?.play() || "the ghost isn't awake yet. give the page a second.",
    draw: () => window.__pencil?.toggle() || "pencil's still sharpening.",
    terminal: () => window.__term?.open() || "terminal's booting.",
    secrets: () => { spBtn?.click(); return "spoilers, served."; },
    forget: () => {
      localStorage.removeItem(KEY);
      toast("done. we've never met.");
      return "memory wiped. it was nice knowing you (allegedly).";
    },
  };

  /* shared bits for the other files */
  window.__site = { state, save, toast, prefersReduced, isTouch, rel, BORN, setName };
})();
