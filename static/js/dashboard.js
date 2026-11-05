/* Dashboard: stats, application tracker (add / edit status / delete / history), deadlines, saved services, questions. */
const STATUS_ORDER = [
  "Not Started",
  "Documents Ready",
  "Applied",
  "Under Review",
  "Approved",
  "Rejected",
];
const PROFILE_KEY = "edudesk_profile";
let applications = [];
let categories = [];
let deadlineData = { reminders: [], upcoming: [], past: [] };
let deadlineTab = "reminders";

const statusClass = (status) =>
  `s-${status.toLowerCase().replace(/\s+/g, "-")}`;
const optionList = (values, selected) =>
  values
    .map(
      (v) => `<option ${v === selected ? "selected" : ""}>${esc(v)}</option>`,
    )
    .join("");

/* ---------- render pieces ---------- */
function renderProgress(counts, total) {
  const box = $("#progress");
  if (!total) {
    box.innerHTML = emptyState(
      "No applications yet",
      "Add your first application to see your progress here.",
      '<button class="btn btn-primary btn-sm" id="progress-add">+ Add Application</button>',
    );
    $("#progress-add").addEventListener("click", () => openApplicationForm());
    return;
  }
  box.innerHTML = STATUS_ORDER.map((status) => {
    const count = counts[status] || 0;
    return `<div class="bar-row ${status === "Approved" ? "approved" : status === "Rejected" ? "rejected" : ""}">
      <span>${esc(status)}</span><div class="bar-track"><div class="bar-fill" style="width:${Math.round((count / total) * 100)}%"></div></div><b>${count}</b></div>`;
  }).join("");
}

function renderApplications() {
  const list = $("#app-list");
  if (!applications.length) {
    list.innerHTML = emptyState(
      "Nothing tracked yet",
      "Track scholarships, admission forms and exams so you never miss a step.",
      '<button class="btn btn-primary btn-sm" id="list-add">+ Add Application</button>',
    );
    $("#list-add").addEventListener("click", () => openApplicationForm());
    return;
  }
  list.innerHTML = applications
    .map(
      (app) => `
    <div class="app-item" data-id="${app.id}">
      <div class="app-main"><div><div class="app-title">${esc(app.title)}</div>
        <div class="app-sub">${esc(app.student_name)} · ${esc(app.category)} · updated ${esc(formatDate(app.updated_at.slice(0, 10)))}</div>
        ${app.notes ? `<div class="app-sub">📝 ${esc(app.notes)}</div>` : ""}</div>
        <span class="status-pill ${statusClass(app.status)}">${esc(app.status)}</span></div>
      <div class="app-controls">
        <select data-status aria-label="Change status">${optionList(STATUS_ORDER, app.status)}</select>
        <button class="btn btn-ghost btn-sm" data-history>History</button>
        <button class="btn btn-ghost btn-sm" data-edit>Edit</button>
        <button class="btn btn-danger btn-sm" data-delete>Delete</button>
      </div></div>`,
    )
    .join("");
}

function renderDeadlines() {
  const items = deadlineData[deadlineTab] || [];
  const box = $("#deadline-list");
  const emptyText = {
    reminders: "No deadlines in the next 7 days.",
    upcoming: "No later deadlines.",
    past: "No past deadlines.",
  }[deadlineTab];
  box.innerHTML = items.length
    ? items
        .map(
          (d) => `
    <div class="deadline-item ${d.days_left < 0 ? "past" : ""}">
      <span class="d-left">${d.days_left < 0 ? `${-d.days_left} days ago` : d.days_left === 0 ? "Today" : `in ${d.days_left} days`}</span>
      <div class="d-date">${esc(formatDate(d.date))}</div><b>${esc(d.title)}</b>
      <p>${esc(d.description)}</p>
      <span class="badge ${d.is_verified ? "badge-official" : "badge-demo"}">${esc(d.label)}</span>
      ${d.official_url ? officialLink(d.official_url, "Official site") : ""}
    </div>`,
        )
        .join("")
    : `<p class="muted small">${emptyText}</p>`;
}

/* ---------- loading ---------- */
async function loadSummary() {
  const summary = await api("/api/dashboard");
  $("#stat-apps").textContent = summary.applications_total;
  $("#stat-saved").textContent = summary.saved_total;
  $("#stat-deadlines").textContent = summary.upcoming_deadlines.length;
  $("#stat-questions").textContent = summary.questions_total;
  if (summary.user)
    $("#welcome").textContent = `Welcome, ${summary.user.name.split(" ")[0]}!`;
  else $("#welcome").textContent = "Welcome, Student!";
  renderProgress(summary.applications_by_status, summary.applications_total);
}
async function loadApplications() {
  applications = (await api("/api/applications")).items;
  renderApplications();
}
async function loadDeadlines() {
  deadlineData = await api("/api/deadlines");
  renderDeadlines();
}
async function loadSaved() {
  const data = await api("/api/saved");
  $("#saved-list").innerHTML = data.items.length
    ? `<ul class="plain-list">${data.items
        .map(
          (
            s,
          ) => `<li><a href="/services?open=${s.id}"><b>${esc(s.title)}</b></a> <span class="muted small">· ${esc(s.category)}</span>
        <button class="icon-btn" data-unsave="${s.id}" aria-label="Remove ${esc(s.title)}">✕</button></li>`,
        )
        .join("")}</ul>`
    : '<p class="muted small">Tap ♡ on any service to save it here.</p><a class="btn btn-soft btn-sm" href="/services">Browse services</a>';
}
async function loadQuestions() {
  const data = await api("/api/questions/recent");
  $("#question-list").innerHTML = data.items.length
    ? data.items
        .map(
          (q) =>
            `<li><a href="/ask?q=${encodeURIComponent(q.text)}">${esc(q.text)}</a></li>`,
        )
        .join("")
    : '<li class="muted small">No questions yet. <a href="/ask">Ask EDUDESK</a></li>';
}
async function loadMatches() {
  let profile = {};
  try {
    profile = JSON.parse(localStorage.getItem(PROFILE_KEY) || "{}");
  } catch (error) {
    /* ignore */
  }
  const hasProfile = Object.keys(profile).length > 0;
  const data = await api(`/api/scholarships?${new URLSearchParams(profile)}`);
  $("#stat-matches").textContent = data.count;
  $("#match-link").textContent = hasProfile
    ? "View matches"
    : "Set your details";
}

async function refreshAll() {
  const jobs = [
    loadSummary(),
    loadApplications(),
    loadDeadlines(),
    loadSaved(),
    loadQuestions(),
    loadMatches(),
  ];
  const results = await Promise.allSettled(jobs);
  const failed = results.find((r) => r.status === "rejected");
  if (failed) toast(failed.reason.message, "error");
}

/* ---------- add / edit form ---------- */
function openApplicationForm(app = null) {
  const guestName = document.body.dataset.user || "";
  const body = openModal(
    app ? "Edit application" : "Add application",
    `
    <form id="app-form" class="auth-form" novalidate>
      <label class="field">Student name<input name="student_name" maxlength="80" value="${esc(app ? app.student_name : guestName)}" required></label>
      <label class="field">Application title<input name="title" maxlength="150" placeholder="e.g. NSP scholarship form" value="${esc(app ? app.title : "")}" required></label>
      <label class="field">Category<select name="category">${optionList([...categories, "Other"], app ? app.category : "Other")}</select></label>
      <label class="field">Status<select name="status">${optionList(STATUS_ORDER, app ? app.status : "Not Started")}</select></label>
      <label class="field">Notes (optional)<input name="notes" maxlength="500" value="${esc(app ? app.notes : "")}"></label>
      <p class="form-error" id="app-error" role="alert" hidden></p>
      <button class="btn btn-primary" type="submit">${app ? "Save changes" : "Add application"}</button>
    </form>`,
  );
  $("#app-form", body).addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = $("button[type=submit]", event.target),
      errorBox = $("#app-error", body);
    const payload = Object.fromEntries(new FormData(event.target).entries());
    if (!payload.student_name.trim() || !payload.title.trim()) {
      errorBox.textContent = "Student name and title are required.";
      errorBox.hidden = false;
      return;
    }
    errorBox.hidden = true;
    setBusy(button, true, "Saving…");
    try {
      await api(app ? `/api/applications/${app.id}` : "/api/applications", {
        method: app ? "PATCH" : "POST",
        body: payload,
      });
      closeModal();
      toast(app ? "Application updated." : "Application added.", "success");
      refreshAll();
    } catch (error) {
      errorBox.textContent = error.message;
      errorBox.hidden = false;
      setBusy(button, false);
    }
  });
}

async function showHistory(app) {
  try {
    const data = await api(`/api/applications/${app.id}/history`);
    openModal(
      `History: ${app.title}`,
      `<ul class="timeline">${data.history
        .map(
          (h) =>
            `<li><b>${esc(h.status)}</b><small>${esc(new Date(h.changed_at + "Z").toLocaleString("en-IN"))}${h.note ? " · " + esc(h.note) : ""}</small></li>`,
        )
        .join("")}</ul>`,
    );
  } catch (error) {
    toast(error.message, "error");
  }
}

function confirmDelete(app) {
  const body = openModal(
    "Delete application?",
    `<p>“${esc(app.title)}” and its history will be removed. This cannot be undone.</p>
    <div class="modal-actions"><button class="btn btn-danger" id="confirm-delete">Yes, delete</button><button class="btn btn-ghost" data-close>Cancel</button></div>`,
  );
  $("#confirm-delete", body).addEventListener("click", async (event) => {
    setBusy(event.target, true, "Deleting…");
    try {
      await api(`/api/applications/${app.id}`, { method: "DELETE" });
      closeModal();
      toast("Application deleted.", "success");
      refreshAll();
    } catch (error) {
      toast(error.message, "error");
      setBusy(event.target, false);
    }
  });
}

/* ---------- events ---------- */
["#add-app-top", "#add-app-quick", "#add-app-panel"].forEach((selector) =>
  $(selector).addEventListener("click", () => openApplicationForm()),
);

$("#app-list").addEventListener("click", (event) => {
  const row = event.target.closest(".app-item");
  if (!row) return;
  const app = applications.find((a) => a.id === Number(row.dataset.id));
  if (!app) return;
  if (event.target.closest("[data-edit]")) openApplicationForm(app);
  if (event.target.closest("[data-history]")) showHistory(app);
  if (event.target.closest("[data-delete]")) confirmDelete(app);
});
$("#app-list").addEventListener("change", async (event) => {
  const select = event.target.closest("[data-status]");
  if (!select) return;
  const id = Number(select.closest(".app-item").dataset.id);
  select.disabled = true;
  try {
    await api(`/api/applications/${id}`, {
      method: "PATCH",
      body: { status: select.value },
    });
    toast("Status updated.", "success");
    await refreshAll();
  } catch (error) {
    toast(error.message, "error");
    await loadApplications();
  }
});
$("#deadline-tabs").addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (!chip) return;
  deadlineTab = chip.dataset.tab;
  $$("#deadline-tabs .chip").forEach((c) =>
    c.classList.toggle("active", c === chip),
  );
  renderDeadlines();
});
$("#saved-list").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-unsave]");
  if (!button) return;
  try {
    await api(`/api/saved/${button.dataset.unsave}`, { method: "DELETE" });
    await Promise.all([loadSaved(), loadSummary()]);
  } catch (error) {
    toast(error.message, "error");
  }
});

(async function init() {
  try {
    categories = (await api("/api/meta")).service_categories;
  } catch (error) {
    categories = [];
  }
  await refreshAll();
})();
