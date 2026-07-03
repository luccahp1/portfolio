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
  function toast(msg, ms = 3200) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    requestAnimationFrame(() => toastEl.classList.add("show"));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("show"), ms);
  }

  /* ---------- greeting: the site knows you ---------- */
  function greetingLine() {
    const h = new Date().getHours();
    const late = h >= 23 || h < 5;
    const v = state.visits;

    if (fresh || v === 1) {
      if (late) return "you're up late. same, honestly.";
      if (h < 12) return "good morning. you're new here.";
      if (h < 18) return "hi. you're new here.";
      return "good evening. you're new here.";
    }
    if (late) return "back again — and at this hour. respect.";
    if (v === 2) return "oh — you came back. hi again.";
    if (v <= 4) return "welcome back. visit #" + v + ".";
    if (v <= 9) return "visit #" + v + ". you basically have a locker here now.";
    return "visit #" + v + ". should i just give you a key?";
  }
  const g = $("#greeting");
  if (g) g.textContent = greetingLine();

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

  function pullCord() {
    setTheme(currentTheme() === "dark" ? "light" : "dark");
    if (!state.cordPulled) {
      state.cordPulled = true;
      save();
      toast(currentTheme() === "dark" ? "there. easier on the eyes." : "and the lights are back.");
    }
  }
  $("#cord")?.addEventListener("click", pullCord);

  /* ---------- tab title misses you ---------- */
  const realTitle = document.title;
  document.addEventListener("visibilitychange", () => {
    document.title = document.hidden ? "come back :(" : realTitle;
  });

  /* ---------- you read the whole thing ---------- */
  const foot = $(".foot"), footRead = $("#foot-read");
  if (foot && footRead && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        footRead.hidden = false;
        io.disconnect();
      }
    }, { threshold: 0.4 });
    io.observe(foot);
  }

  /* ---------- konami → blueprint mode ---------- */
  const SEQ = ["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","b","a"];
  let seqAt = 0;
  const BP_NOTES = [
    { sel: "#hello h1", text: "44rem column. trust me.", dx: 10, dy: -34 },
    { sel: "#outpace", text: "rotate(-0.5deg) — barely, but you feel it", dx: 0, dy: -30 },
    { sel: ".tape", text: "the tape is one rectangle and a dream", dx: 60, dy: -6 },
    { sel: "#guestbook-h", text: "guestbook backend: my inbox", dx: 180, dy: 4 },
    { sel: ".foot", text: "the ghost you saw was real. well. local.", dx: 10, dy: -26 },
  ];
  let bpEls = [];
  function blueprint(force) {
    const on = force !== undefined ? force : !document.body.classList.contains("blueprint");
    document.body.classList.toggle("blueprint", on);
    bpEls.forEach((el) => el.remove());
    bpEls = [];
    if (on) {
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
      toast("blueprint mode. this is how it looks in my head.");
      if (!state.konami) { state.konami = true; save(); }
    }
  }
  document.addEventListener("keydown", (e) => {
    if (e.target.matches("input, textarea")) return;
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
    "source: https://github.com/luccahp1/portfolio — handwritten, ghosts included.", css2
  );

  /* ---------- the public api (it felt right) ---------- */
  window.lucca = {
    lights: pullCord,
    blueprint: () => blueprint(),
    ghost: () => window.__ghost?.play() || "the ghost isn't awake yet. give the page a second.",
    draw: () => window.__pencil?.toggle() || "pencil's still sharpening.",
    terminal: () => window.__term?.open() || "terminal's booting.",
    forget: () => {
      localStorage.removeItem(KEY);
      toast("done. we've never met.");
      return "memory wiped. it was nice knowing you (allegedly).";
    },
  };

  /* shared bits for the other files */
  window.__site = { state, save, toast, prefersReduced, isTouch, rel, BORN };
})();
