/* of course there's a terminal. press / */

(function () {
  const site = window.__site;
  if (!site) return;
  const { state, save, rel, BORN, setName } = site;

  const term = document.getElementById("term");
  const body = document.getElementById("term-body");
  const input = document.getElementById("term-input");
  if (!term || !body || !input) return;

  const history = [];
  let hAt = -1;

  /* ---------- output ---------- */
  function line(text, cls) {
    const el = document.createElement("div");
    if (cls) el.className = cls;
    el.textContent = text;
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
  }
  function html(markup) {
    const el = document.createElement("div");
    el.innerHTML = markup;   // static strings only, never user input
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
  }

  /* ---------- open / close ---------- */
  let opened = false;
  function open() {
    term.hidden = false;
    input.focus();
    if (!opened) {
      opened = true;
      line("you found the terminal. type `help` — or don't, i'm a sign not a cop.", "term-dim");
    }
    return "";
  }
  function close() {
    term.hidden = true;
    input.blur();
  }

  document.getElementById("term-btn")?.addEventListener("click", () =>
    term.hidden ? open() : close()
  );
  document.getElementById("open-changelog")?.addEventListener("click", () => {
    open();
    exec("changelog");
  });
  document.addEventListener("keydown", (e) => {
    const inField = e.target instanceof Element && e.target.matches("input, textarea");
    if ((e.key === "/" || e.key === "`") && term.hidden && !inField &&
        !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      open();
    } else if (e.key === "Escape" && !term.hidden) {
      close();
    }
  });

  /* ---------- the filesystem, such as it is ---------- */
  const files = {
    "about.txt":
      "lucca prada. builds small software for real businesses.\n" +
      "likes owning the whole thing: pitch, code, deploy, 2am incident.\n" +
      "believes software should feel like a person made it.",
    "now.txt":
      "building atrio + outpace.\n" +
      "pitching them to a real eavestroughs company on a live call.\n" +
      "feeding the closet server.",
    "secrets.txt":
      "d          pencil mode (c cycles inks)\n" +
      "/          you're soaking in it\n" +
      "konami     blueprints\n" +
      "ctrl+p     the résumé trick\n" +
      "call me x  the site learns your name\n" +
      "lucca.*    the console api\n" +
      "spoilers   the button at the very bottom. i caved. it lists everything.\n" +
      "the tape   it's load-bearing. tug it and see.\n" +
      "one more isn't listed. it finds you.",
  };

  const CHANGELOG = [
    "v1.2 — jul 3 2026 — blueprint mode measures pixels. the cord can snap",
    "        (sparks, flicker, one very sad sound) and gets taped back up.",
    "        the tape is pullable — a small lucca comes to pin things back.",
    "        speedruns get confetti and an official time. the résumé got a",
    "        full rewrite: cat it at resume.html or just ctrl+p.",
    "v1.1 — jul 3 2026 — the site learned names, seasons, and manners.",
    "        favicon naps, lamp sass, three inks, speedrun detection, and —",
    "        fine — a spoiler button that lists every secret. i caved.",
    "v1.0 — jul 2 2026 — site is born. immediately gains object permanence:",
    "        it remembers visits, keeps doodles, and replays your last cursor.",
    "        no frameworks were consulted.",
  ];

  const sections = ["hello", "now", "work", "about", "guestbook", "hi"];

  /* ---------- commands ---------- */
  const commands = {
    help() {
      line("things i answer to:");
      line("  whoami · ls · cat <file> · open <place> · now · uptime");
      line("  lights · ghost · draw · blueprint · changelog · guestbook");
      line("  call me <name> · resume · forget · clear · exit");
      line("some commands aren't listed. that's what makes them commands.", "term-dim");
    },
    whoami() {
      const n = 1000 + (state.firstVisit % 8999);
      line("visitor #" + n + " (self-issued, non-transferable)");
      if (state.name) line("answers to: " + state.name);
      else line("name: unknown. fixable — try: call me maple", "term-dim");
      line("first seen: " + rel(Date.now() - state.firstVisit) + " ago · visits: " + state.visits);
      if (state.spoiled) line("read the spoilers: yes. no judgment. (some judgment.)", "term-dim");
      if (state.prankRm) line("permanent record: attempted `rm -rf /` once. we remember.", "term-dim");
      line("everything above lives in your localStorage, not on a server.", "term-dim");
    },
    hi() {
      line(state.name
        ? "hi, " + state.name + ". always nice when you stop by."
        : "hi. you didn't have to greet a terminal, but you did. noted (favorably).");
    },
    hello() { commands.hi(); },
    ls() {
      line(sections.join("  "));
      line(Object.keys(files).join("  "));
    },
    cat(arg) {
      if (!arg) return line("cat what? try: cat " + Object.keys(files)[0]);
      const f = files[arg.trim()];
      f ? line(f) : line("no such file. `ls` knows what's real.");
    },
    open(arg) {
      const a = (arg || "").trim().toLowerCase();
      const map = { outpace: "#outpace", atrio: "#atrio", server: "#server", site: "#site",
                    guestbook: "#guestbook", work: "#work", about: "#about", now: "#now", top: "#hello" };
      if (a === "github") { window.open("https://github.com/luccahp1", "_blank"); return line("opening github…"); }
      if (a === "email") { location.href = "mailto:luccaprada25@gmail.com"; return line("opening your mail app…"); }
      if (map[a]) { document.querySelector(map[a])?.scrollIntoView({ behavior: "smooth" }); close(); return; }
      line("open what? try: open outpace · atrio · server · github · email");
    },
    now() { line(files["now.txt"]); },
    uptime() {
      const days = Math.max(1, Math.round((Date.now() - BORN.getTime()) / 86400000));
      line("this site: " + days + " day" + (days > 1 ? "s" : "") + " without incident.");
      line("the closet server: probably up. it has never lied to me twice.", "term-dim");
    },
    lights() { window.lucca?.lights(); line("done."); },
    ghost() {
      const r = window.lucca?.ghost();
      line(typeof r === "string" && r !== "…" ? r : "look at the page.", "term-dim");
      if (r === "…") close();
    },
    draw() { close(); window.lucca?.draw(); },
    blueprint() { close(); window.lucca?.blueprint(); },
    changelog() { CHANGELOG.forEach((l) => line(l)); },
    resume() {
      line("fetching the serious version…");
      window.open("resume.html", "_blank");
    },
    guestbook() {
      const entries = document.querySelectorAll("#guestbook .guest-list li");
      const real = [...entries].filter((li) => !li.textContent.includes("nobody yet")).length;
      line("entries: " + real + " (hand-counted, obviously)");
      html('no backend. <a href="mailto:luccaprada25@gmail.com?subject=guestbook">email me</a> ' +
           "and i hand-type your name into the html. 100% uptime since forever.");
    },
    forget() { line(window.lucca?.forget() || "hm."); },
    clear() { body.textContent = ""; },
    exit() { close(); },
    coffee() { line("brewing… no. wait. that's your job. i'm a website."); },
    echo(arg) { line(arg || ""); },
    man(arg) {
      arg === "lucca"
        ? line("LUCCA(1) — builds small software. accepts coffee. see also: hire(1)")
        : line("the manual is the page you're standing on.");
    },
    ping(arg) {
      (arg || "").includes("server")
        ? line("PING closet-server: 1 closet of latency. it says hi.")
        : line("pong. obviously.");
    },
  };

  function exec(raw) {
    const t = raw.trim();
    if (!t) return;
    line("you@luccas-site:~$ " + t, "term-dim");
    const [cmd, ...rest] = t.split(/\s+/);
    const arg = rest.join(" ");

    if (t.toLowerCase().startsWith("call me")) {
      const name = setName(t.slice(7));
      return name
        ? line("ok, " + name + ". i'll remember. (locally. always locally.)")
        : line("call you… nothing? bold. try: call me maple");
    }
    if (t === "sudo hire lucca") {
      line("checking credentials… you seem great.");
      html('ok. it\'s done on my end — yours is one email: ' +
           '<a href="mailto:luccaprada25@gmail.com?subject=let\'s work together">luccaprada25@gmail.com</a>');
      return;
    }
    if (cmd === "sudo") return line("this site trusts you. no sudo needed.");
    if (t.startsWith("rm")) {
      state.prankRm = true; save();
      return line("absolutely not. and yes, this goes on your permanent record (see `whoami`).");
    }
    if (t === "konami") return line("no shortcuts. do the inputs.", "term-dim");

    const fn = commands[cmd.toLowerCase()];
    fn ? fn(arg) : line("`" + cmd + "` not found. try `help`. or coffee.");
  }

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const v = input.value;
      input.value = "";
      if (v.trim()) { history.push(v); hAt = history.length; }
      exec(v);
    } else if (e.key === "ArrowUp") {
      if (hAt > 0) input.value = history[--hAt];
      e.preventDefault();
    } else if (e.key === "ArrowDown") {
      hAt < history.length - 1 ? (input.value = history[++hAt]) : (input.value = "", hAt = history.length);
      e.preventDefault();
    }
  });

  /* clicking anywhere in the terminal focuses the input */
  term.addEventListener("click", () => input.focus());

  window.__term = { open, close };
})();
