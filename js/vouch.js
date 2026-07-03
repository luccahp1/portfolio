/* the vouch card. no backend — it drafts an email in YOUR mail app,
   and confirmed vouches get hand-typed into the html. verification
   process: my eyeballs. it has never been hacked. */

(function () {
  const site = window.__site;
  if (!site) return;
  const { state, save, toast } = site;

  const wrap = document.getElementById("vouch-wrap");
  const form = document.getElementById("vouch-form");
  const opener = document.getElementById("vouch-btn");
  const nameIn = document.getElementById("v-name");
  const emailIn = document.getElementById("v-email");
  const companyIn = document.getElementById("v-company");
  const roleWrap = document.getElementById("v-role-wrap");
  const roleIn = document.getElementById("v-role");
  const pinImg = document.getElementById("vouch-pin");
  if (!wrap || !form || !opener) return;

  let lastFocus = null;

  function open() {
    lastFocus = document.activeElement;
    wrap.hidden = false;
    // lucca re-pins the card somewhere new each time. of course he does.
    if (pinImg) {
      pinImg.style.left = 30 + Math.random() * 45 + "%";
      pinImg.style.transform = "translateX(-50%) rotate(" + (Math.random() * 22 - 11).toFixed(1) + "deg)";
    }
    form.style.transform = "rotate(" + (Math.random() * 1.6 - 0.8).toFixed(2) + "deg)";
    nameIn?.focus();
  }
  function close() {
    wrap.hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  opener.addEventListener("click", open);
  wrap.querySelectorAll("[data-close]").forEach((el) => el.addEventListener("click", close));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !wrap.hidden) close();
  });

  /* the bonus question. it only exists if you give it a reason to. */
  function syncRole() {
    const hasCompany = companyIn.value.trim().length > 0;
    if (hasCompany && roleWrap.hidden) {
      roleWrap.hidden = false;
    } else if (!hasCompany && !roleIn.value.trim()) {
      roleWrap.hidden = true;
    }
  }
  companyIn?.addEventListener("input", syncRole);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = nameIn.value.trim();
    const email = emailIn.value.trim();
    if (!name || !email) return;
    const company = companyIn.value.trim();
    const role = roleIn.value.trim();

    const body =
      "i vouch for lucca.\n\n" +
      "name: " + name + "\n" +
      "email: " + email + "\n" +
      (company ? "company: " + company + "\n" : "") +
      (role ? "role: " + role + "\n" : "") +
      "\n(sent from the vouch card on lucca's site. hand-type me in.)";

    location.href =
      "mailto:luccaprada25@gmail.com" +
      "?subject=" + encodeURIComponent("i vouch for lucca — " + name) +
      "&body=" + encodeURIComponent(body);

    state.vouched = true;
    save();
    close();
    toast("appreciate you. i'll hand-type you in soon.", 4200, { el: opener, dy: -36 });
  });

  window.__vouch = { open };
})();
