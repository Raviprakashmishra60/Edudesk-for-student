/* EDUDESK admin panel: add / edit / delete services, scholarships, colleges, exams, deadlines and AKTU papers.
   Uses the admin API (/api/admin/...). Helpers (api, esc, openModal, toast ...) come from app.js. */
const SERVICE_CATS = ["Scholarships", "College Admissions", "Entrance Exams", "Competitive Exams", "Government Education Schemes",
  "Certificates", "Document Services", "Internships", "Career Guidance", "Courses", "Education Loans", "Counselling"];
const EXAM_CATS = ["Engineering", "Medical", "University Entrance", "Government Exams", "Competitive Exams"];

const fText = (name, label, extra = {}) => ({ name, label, type: "text", ...extra });
const fArea = (name, label, extra = {}) => ({ name, label, type: "textarea", ...extra });
const fList = (name, label, def = []) => ({ name, label: `${label} (one per line)`, type: "list", def });
const fPick = (name, label, options) => ({ name, label, type: "select", options });
const fLink = (name = "official_url", label = "Official website link", extra = {}) => ({ name, label, type: "url", ...extra });
const fDemo = { name: "is_demo", label: "This is demo / unverified data", type: "checkbox" };

const RESOURCES = {
  services: { label: "Services", name: "title", sub: (r) => r.category, fields: [
    fText("title", "Title", { required: true }), fPick("category", "Category", SERVICE_CATS), fArea("description", "Description", { required: true }),
    fArea("eligibility", "Eligibility"), fText("important_dates", "Important dates"), fText("assistance_note", "Assistance note"), fLink(),
    fList("documents", "Required documents"), fList("steps", "Application steps"), fDemo] },
  scholarships: { label: "Scholarships", name: "name", sub: (r) => `${r.provider} · ${r.type}`, fields: [
    fText("name", "Name", { required: true }), fText("provider", "Provider", { required: true }), fPick("type", "Type", ["Government", "Private"]),
    fArea("description", "Description"), fArea("eligibility", "Eligibility"), fText("benefit", "Approx. benefit"), fText("last_date", "Last date"), fLink(),
    fList("documents", "Documents"), fList("courses", "Courses, or Any", ["Any"]), fList("levels", "Levels: 10th, 12th, Undergraduate, Postgraduate"),
    fList("states", "States, or All India", ["All India"]), fList("categories", "Categories: All, General, EWS, OBC, SC, ST", ["All"]), fDemo] },
  colleges: { label: "Colleges", name: "name", sub: (r) => `${r.city}, ${r.state} · ${r.type}`, fields: [
    fText("name", "Name", { required: true }), fText("city", "City", { required: true }), fText("state", "State", { required: true }),
    fPick("type", "Type", ["Government", "Private", "Deemed"]), fArea("description", "Description"), fPick("fee_band", "Fee band", ["Low", "Medium", "High"]),
    fArea("eligibility", "Eligibility"), fArea("admission_process", "Admission process"), fLink(),
    fList("courses", "Courses"), fList("entrance_exams", "Entrance exams accepted"), fDemo] },
  exams: { label: "Exams", name: "name", sub: (r) => r.category, fields: [
    fText("name", "Name", { required: true }), fPick("category", "Category", EXAM_CATS), fArea("description", "Description"), fArea("eligibility", "Eligibility"),
    fArea("registration_process", "Registration process"), fText("important_dates", "Important dates"), fLink(), fList("documents", "Documents needed"), fDemo] },
  deadlines: { label: "Deadlines", name: "title", sub: (r) => `${r.date} · ${r.category}`, fields: [
    fText("title", "Title", { required: true }), fText("category", "Category", { required: true }), { name: "date", label: "Date", type: "date", required: true },
    fArea("description", "Description"), fLink(), fText("source_label", "Source label", { def: "Added by admin" }),
    { name: "is_verified", label: "Verified on the official source", type: "checkbox" }] },
  papers: { label: "AKTU papers", name: "title", sub: (r) => `${r.subject_code} · ${r.exam_session || ""}`, fields: [
    fText("subject_code", "Subject code (e.g. BAS101)", { required: true }), fText("title", "Title", { required: true }),
    fText("exam_session", "Session (e.g. 2023-24)"), fPick("paper_type", "Type", ["Theory", "Sessional", "Back paper", "Portal"]),
    fLink("official_url", "Link to the paper", { required: true })] },
};

let currentKey = "services", records = [];
const listBox = $("#admin-list"), countLabel = $("#admin-count"), searchBox = $("#admin-search"), tabsBox = $("#admin-tabs");

function renderTabs() {
  tabsBox.innerHTML = Object.entries(RESOURCES).map(([key, r]) =>
    `<button class="chip ${key === currentKey ? "active" : ""}" data-key="${key}" type="button">${esc(r.label)}</button>`).join("");
}

function renderList() {
  const cfg = RESOURCES[currentKey], query = searchBox.value.trim().toLowerCase();
  const shown = records.filter((r) => !query || `${r[cfg.name]} ${cfg.sub(r)}`.toLowerCase().includes(query));
  countLabel.textContent = `${shown.length} of ${records.length}`;
  if (!shown.length) {
    listBox.innerHTML = emptyState(records.length ? "Nothing matches your search" : `No ${cfg.label.toLowerCase()} yet`,
      records.length ? "Try different words." : "Click “Add new” to create the first one.", '<button class="btn btn-primary btn-sm" id="empty-add" type="button">+ Add new</button>');
    return;
  }
  listBox.innerHTML = `<div class="admin-table-wrap"><table class="admin-table"><thead><tr><th>ID</th><th>Name</th><th>Details</th><th></th></tr></thead><tbody>
    ${shown.map((r) => `<tr data-id="${r.id}"><td>${esc(r.id)}</td>
      <td><b>${esc(r[cfg.name])}</b>${r.is_demo ? ' <span class="badge badge-demo">Demo</span>' : ""}</td>
      <td class="muted">${esc(cfg.sub(r))}</td>
      <td class="admin-actions"><button class="btn btn-ghost btn-sm" data-edit type="button">Edit</button><button class="btn btn-danger btn-sm" data-delete type="button">Delete</button></td></tr>`).join("")}
  </tbody></table></div>`;
}

async function loadRecords() {
  listBox.innerHTML = '<p class="muted">Loading…</p>';
  try { records = (await api(`/api/admin/${currentKey}`)).items; renderList(); }
  catch (error) {
    listBox.innerHTML = errorState(error.status === 401 || error.status === 403 ? "Please log in with an admin account." : error.message);
    countLabel.textContent = "";
  }
}

/* ---------- add / edit form ---------- */
function fieldHtml(f, value) {
  const req = f.required ? " required" : "";
  if (f.type === "checkbox") return `<label class="check"><input type="checkbox" name="${f.name}" ${value ? "checked" : ""}> ${esc(f.label)}</label>`;
  let control;
  if (f.type === "list") control = `<textarea name="${f.name}" rows="4">${esc((Array.isArray(value) ? value : []).join("\n"))}</textarea>`;
  else if (f.type === "textarea") control = `<textarea name="${f.name}" rows="3"${req}>${esc(value ?? "")}</textarea>`;
  else if (f.type === "select") {
    const options = !value || f.options.includes(value) ? f.options : [value, ...f.options];
    control = `<select name="${f.name}">${options.map((o) => `<option ${o === (value || f.options[0]) ? "selected" : ""}>${esc(o)}</option>`).join("")}</select>`;
  } else control = `<input name="${f.name}" type="${f.type === "url" ? "text" : f.type}" value="${esc(value ?? "")}"${req}${f.type === "url" ? ' placeholder="https://…"' : ""}>`;
  return `<label class="field">${esc(f.label)}${f.required ? " *" : ""}${control}</label>`;
}

function readForm(formEl) {
  const data = {};
  for (const f of RESOURCES[currentKey].fields) {
    const el = formEl.elements[f.name];
    if (f.type === "checkbox") data[f.name] = el.checked;
    else if (f.type === "list") data[f.name] = el.value.split("\n").map((line) => line.trim()).filter(Boolean);
    else data[f.name] = el.value.trim();
  }
  return data;
}

function validate(data) {
  for (const f of RESOURCES[currentKey].fields) {
    if (f.required && !data[f.name]) return `${f.label} is required.`;
    if (f.type === "url" && data[f.name] && !/^https?:\/\//i.test(data[f.name])) return `${f.label} must start with http:// or https://`;
  }
  return "";
}

function openForm(record = null) {
  const cfg = RESOURCES[currentKey];
  const body = openModal(`${record ? "Edit" : "Add new"} · ${cfg.label}`, `<form id="admin-form" novalidate>
    ${cfg.fields.map((f) => fieldHtml(f, record ? record[f.name] : f.def)).join("")}
    <p class="form-error" id="admin-error" role="alert" hidden></p>
    <button class="btn btn-primary" type="submit">${record ? "Save changes" : "Add"}</button></form>`);
  $("#admin-form", body).addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = $("button[type=submit]", event.target), errorBox = $("#admin-error", body), data = readForm(event.target), problem = validate(data);
    if (problem) { errorBox.textContent = problem; errorBox.hidden = false; return; }
    errorBox.hidden = true; setBusy(button, true, "Saving…");
    try {
      await api(record ? `/api/admin/${currentKey}/${record.id}` : `/api/admin/${currentKey}`, { method: record ? "PATCH" : "POST", body: data });
      closeModal(); toast(record ? "Saved." : "Added.", "success"); await loadRecords();
    } catch (error) { errorBox.textContent = error.message; errorBox.hidden = false; setBusy(button, false); }
  });
}

function confirmDelete(record) {
  const cfg = RESOURCES[currentKey];
  const body = openModal("Delete this record?", `<p>“${esc(record[cfg.name])}” will be removed from the website. This cannot be undone.</p>
    <div class="modal-actions"><button class="btn btn-danger" id="confirm-delete" type="button">Yes, delete</button><button class="btn btn-ghost" data-close type="button">Cancel</button></div>`);
  $("#confirm-delete", body).addEventListener("click", async (event) => {
    setBusy(event.target, true, "Deleting…");
    try { await api(`/api/admin/${currentKey}/${record.id}`, { method: "DELETE" }); closeModal(); toast("Deleted.", "success"); await loadRecords(); }
    catch (error) { toast(error.message, "error"); setBusy(event.target, false); }
  });
}

/* ---------- events ---------- */
tabsBox.addEventListener("click", (event) => {
  const chip = event.target.closest("[data-key]"); if (!chip) return;
  currentKey = chip.dataset.key; searchBox.value = ""; renderTabs(); loadRecords();
});
searchBox.addEventListener("input", debounce(renderList, 150));
$("#admin-add").addEventListener("click", () => openForm());
listBox.addEventListener("click", (event) => {
  if (event.target.closest("#empty-add")) return openForm();
  const row = event.target.closest("tr[data-id]"); if (!row) return;
  const record = records.find((r) => r.id === Number(row.dataset.id)); if (!record) return;
  if (event.target.closest("[data-edit]")) openForm(record);
  if (event.target.closest("[data-delete]")) confirmDelete(record);
});

renderTabs();
loadRecords();
