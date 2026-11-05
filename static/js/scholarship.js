/* Scholarship Finder: filters, cards, "Check Eligibility" (uses POST /api/scholarships/<id>/check). */
const form = $("#scholarship-filters"),
  grid = $("#scholarship-grid"),
  countLabel = $("#scholarship-count");
const scholarshipCache = new Map();
const COURSES = ["B.Tech", "B.Sc", "B.A.", "B.Com", "Diploma", "MBBS"];
const PROFILE_KEY = "edudesk_profile"; // remembered in this browser so the dashboard can show matches

function readProfile() {
  const data = Object.fromEntries(new FormData(form).entries());
  Object.keys(data).forEach((key) => {
    if (data[key] === "") delete data[key];
  });
  return data;
}

function scholarshipCard(item) {
  return `<article class="card item-card">
    <div class="card-top"><span class="badge ${item.type === "Government" ? "badge-gov" : "badge-private"}">${esc(item.type)}</span>${demoBadge(item.is_demo)}</div>
    <h3 class="card-title">${esc(item.name)}</h3>
    <p class="card-desc">${esc(item.provider)}</p>
    <div class="card-meta">
      <span><b>Eligibility:</b> ${esc(item.eligibility)}</span>
      <span><b>Approx. benefit:</b> ${esc(item.benefit)}</span>
      <span><b>Last date:</b> ${esc(item.last_date)}</span>
    </div>
    <div class="card-actions">
      <button class="btn btn-primary btn-sm" data-check="${item.id}">Check Eligibility</button>
      <button class="btn btn-soft btn-sm" data-details="${item.id}">Details</button>
      ${helpButton(item.name)}
    </div></article>`;
}

async function loadScholarships() {
  showSkeletons(grid);
  const params = new URLSearchParams(readProfile());
  try {
    const data = await api(`/api/scholarships?${params}`);
    data.items.forEach((item) => scholarshipCache.set(item.id, item));
    countLabel.textContent = data.count
      ? `${data.count} scholarship${data.count === 1 ? "" : "s"} match your filters (demo data)`
      : "";
    grid.innerHTML = data.count
      ? data.items.map(scholarshipCard).join("")
      : emptyState(
          "No scholarships match",
          "Try removing a filter such as income or marks, or choose “Any”.",
          '<button class="btn btn-primary btn-sm" id="empty-reset">Reset filters</button>',
        );
    $("#empty-reset")?.addEventListener("click", () => {
      form.reset();
      loadScholarships();
    });
    localStorage.setItem(PROFILE_KEY, JSON.stringify(readProfile()));
  } catch (error) {
    grid.innerHTML = errorState(error.message);
    countLabel.textContent = "";
  }
}

function detailsHtml(item) {
  return `<div class="tags"><span class="badge ${item.type === "Government" ? "badge-gov" : "badge-private"}">${esc(item.type)}</span>${demoBadge(item.is_demo)}</div>
    <p style="margin-top:12px"><b>Provider:</b> ${esc(item.provider)}</p>
    ${textBlock("Eligibility (demo)", item.eligibility)}
    ${textBlock("Approximate benefit", item.benefit)}
    ${textBlock("Last date", item.last_date)}
    ${listBlock("Documents", item.documents)}
    <p class="muted small" style="margin-top:14px">${esc(DEMO_NOTE)}</p>`;
}

async function getScholarship(id) {
  if (scholarshipCache.has(id)) return scholarshipCache.get(id);
  const item = await api(`/api/scholarships/${id}`);
  scholarshipCache.set(id, item);
  return item;
}

async function showDetails(id) {
  try {
    const item = await getScholarship(id);
    const body = openModal(
      item.name,
      detailsHtml(item) +
        `<div class="modal-actions">${officialLink(item.official_url, "Apply on official site")}
      <button class="btn btn-soft btn-sm" id="d-track">+ Track this</button>
      <button class="btn btn-primary btn-sm" id="d-check">Check Eligibility</button>${helpButton(item.name)}</div>`,
    );
    $("#d-track", body).addEventListener("click", () =>
      addToTracker(item.name, "Scholarships"),
    );
    $("#d-check", body).addEventListener("click", () => showCheck(id));
  } catch (error) {
    toast(error.message, "error");
  }
}

async function showCheck(id) {
  let item;
  try {
    item = await getScholarship(id);
  } catch (error) {
    return toast(error.message, "error");
  }
  const saved = readProfile();
  const body = openModal(
    `Check eligibility: ${item.name}`,
    `
    <p class="muted">Enter your details. We compare them with this scholarship's <b>demo</b> criteria.</p>
    <form id="check-form" class="form-row" style="grid-template-columns:repeat(2,1fr)">
      <label class="field">Course<select name="course"><option value="">Select</option>${COURSES.map((v) => `<option ${saved.course === v ? "selected" : ""}>${v}</option>`).join("")}</select></label>
      <label class="field">Class / level<select name="level"><option value="">Select</option>${["10th", "12th", "Undergraduate", "Postgraduate"].map((v) => `<option ${saved.level === v ? "selected" : ""}>${v}</option>`).join("")}</select></label>
      <label class="field">State<select name="state"><option value="">Select</option>${STATES.map((v) => `<option ${saved.state === v ? "selected" : ""}>${esc(v)}</option>`).join("")}</select></label>
      <label class="field">Category<select name="category"><option value="">Select</option>${["General", "EWS", "OBC", "SC", "ST"].map((v) => `<option ${saved.category === v ? "selected" : ""}>${v}</option>`).join("")}</select></label>
      <label class="field">Family income (₹ / year)<input name="income" type="number" min="0" value="${esc(saved.income || "")}"></label>
      <label class="field">Marks (%)<input name="marks" type="number" min="0" max="100" value="${esc(saved.marks || "")}"></label>
      <div style="grid-column:1/-1"><button class="btn btn-primary" type="submit">Check</button></div>
    </form>
    <p class="form-error" id="check-error" hidden></p><div id="check-result"></div>`,
  );
  $("#check-form", body).addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = $("button[type=submit]", event.target),
      errorBox = $("#check-error", body),
      result = $("#check-result", body);
    const payload = Object.fromEntries(new FormData(event.target).entries());
    Object.keys(payload).forEach((key) => {
      if (payload[key] === "") delete payload[key];
    });
    errorBox.hidden = true;
    setBusy(button, true, "Checking…");
    try {
      const data = await api(`/api/scholarships/${id}/check`, {
        method: "POST",
        body: payload,
      });
      result.innerHTML = `<div class="verdict ${data.eligible ? "ok" : "no"}">${esc(data.verdict)}</div>
        ${data.checks.map((c) => `<div class="check-row ${c.passed ? "pass" : "fail"}"><span class="mark">${c.passed ? "✓" : "✗"}</span><span><b>${esc(c.criterion)}:</b> ${esc(c.message)}</span></div>`).join("")}
        <p class="muted small">${esc(data.note)}</p>
        <div class="modal-actions">${officialLink(item.official_url, "Verify on official site")}${helpButton(item.name)}</div>`;
    } catch (error) {
      errorBox.textContent = error.message;
      errorBox.hidden = false;
      result.innerHTML = "";
    } finally {
      setBusy(button, false);
    }
  });
}

grid.addEventListener("click", (event) => {
  const check = event.target.closest("[data-check]"),
    details = event.target.closest("[data-details]");
  if (check) showCheck(Number(check.dataset.check));
  if (details) showDetails(Number(details.dataset.details));
});
form.addEventListener("submit", (event) => {
  event.preventDefault();
  loadScholarships();
});
form.addEventListener("change", loadScholarships);
form.addEventListener(
  "input",
  debounce((event) => {
    if (event.target.type === "number") loadScholarships();
  }, 400),
);
$("#scholarship-reset").addEventListener("click", () =>
  setTimeout(() => {
    localStorage.removeItem(PROFILE_KEY);
    loadScholarships();
  }, 0),
);

(async function init() {
  fillSelect(form.elements.course, COURSES);
  try {
    // restore the last filters used in this browser
    const saved = JSON.parse(localStorage.getItem(PROFILE_KEY) || "{}");
    Object.entries(saved).forEach(([key, value]) => {
      if (form.elements[key]) form.elements[key].value = value;
    });
  } catch (error) {
    /* ignore broken saved data */
  }
  await loadScholarships();
  openFromUrl(showDetails);
})();
