"""
EDUDESK feature: ADMIN WEB PANEL at /admin  (add / edit / delete without the browser console).
Run once from the EDUDESK folder:   python apply_admin.py
Safe to re-run. Only admin accounts can open /admin.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent


def write(relative, content):
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"+ {relative}: written")


def patch(filename, replacements, marker):
    path = BASE / filename
    if not path.exists():
        print(f"! {filename}: file not found")
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"- {filename}: already patched, skipped")
        return
    for old, _ in replacements:
        if text.count(old) != 1:
            print(f"! {filename}: expected code not found, nothing changed.\n    looking for: {old[:80]!r}")
            return
    for old, new in replacements:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"+ {filename}: patched")


# ------------------------------------------------------------------ app.py: the /admin page
patch("app.py", [(
    '        session.clear()\n        return redirect(url_for("home"))\n',
    '        session.clear()\n        return redirect(url_for("home"))\n'
    '\n'
    '    @app.get("/admin")\n'
    '    def admin_page():\n'
    '        """Admin panel (HTML). Only admins can open it; the data comes from /api/admin/..."""\n'
    '        user = current_user()\n'
    '        if not user:\n'
    '            return redirect(url_for("login_page", next="/admin"))\n'
    '        if not user.is_admin:\n'
    '            return render_template("404.html", active=""), 404\n'
    '        return render_template("admin.html")\n',
)], "def admin_page")

# ------------------------------------------------------------------ admin.py: list endpoint + link check
patch("admin.py", [
    ('@admin_bp.get("/applications")',
     '@admin_bp.get("/<resource>")\n'
     '@admin_required\n'
     'def list_records(resource):\n'
     '    """All records of one resource (newest first) for the admin panel."""\n'
     '    model = _resource(resource)[0]\n'
     '    rows = model.query.order_by(model.id.desc()).limit(500).all()\n'
     '    return jsonify({"items": [row.to_dict() for row in rows], "count": len(rows)})\n'
     '\n\n'
     '@admin_bp.get("/applications")'),
    ('            setattr(record, field, value.strip())',
     '            if field == "official_url" and value.strip() and not value.strip().lower().startswith(("http://", "https://")):\n'
     '                raise ApiError("official_url must start with http:// or https://", 400)\n'
     '            setattr(record, field, value.strip())'),
], "def list_records")

# ------------------------------------------------------------------ templates/admin.html
write("templates/admin.html", r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Admin · EDUDESK</title>
  <link rel="icon" href="/static/images/favicon.svg">
  <link rel="stylesheet" href="/static/css/style.css">
  <link rel="stylesheet" href="/static/css/responsive.css">
  <link rel="stylesheet" href="/static/css/admin.css">
</head>
<body>
  <header class="admin-top">
    <div class="container admin-bar">
      <a class="admin-brand" href="/">EDUDESK <span>Admin</span></a>
      <span class="muted small">{{ user.email if user else "" }}</span>
      <span class="admin-spacer"></span>
      <a class="btn btn-ghost btn-sm" href="/dashboard">Dashboard</a>
      <a class="btn btn-ghost btn-sm" href="/logout">Log out</a>
    </div>
  </header>

  <main class="container admin-main">
    <h1>Admin panel</h1>
    <p class="muted">Add, edit or delete content. Changes appear on the website immediately. Only mark data as verified after checking the official source.</p>
    <div class="chips" id="admin-tabs"></div>
    <div class="admin-toolbar">
      <input id="admin-search" type="search" placeholder="Search in this list…" aria-label="Search" autocomplete="off">
      <span id="admin-count" class="muted small"></span>
      <button class="btn btn-primary btn-sm" id="admin-add" type="button">+ Add new</button>
    </div>
    <div id="admin-list"></div>
  </main>

  <div class="toast-root" id="toast-root"></div>
  <script src="/static/js/app.js"></script>
  <script src="/static/js/admin.js"></script>
</body>
</html>
''')

# ------------------------------------------------------------------ static/css/admin.css
write("static/css/admin.css", r'''
/* EDUDESK - admin panel */
.admin-top { background: #fff; border-bottom: 1px solid var(--line, #e5e7f5); position: sticky; top: 0; z-index: 20; }
.admin-bar { display: flex; align-items: center; gap: 12px; padding-top: 12px; padding-bottom: 12px; flex-wrap: wrap; }
.admin-brand { font-weight: 800; text-decoration: none; color: inherit; font-size: 1.1rem; }
.admin-brand span { color: var(--primary, #5b5bd6); }
.admin-spacer { flex: 1; }
.admin-main { padding-top: 24px; padding-bottom: 60px; }
.admin-main .chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }
.admin-toolbar { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-bottom: 14px; }
.admin-toolbar input { flex: 1 1 240px; font: inherit; padding: 10px 14px; border: 1.5px solid var(--line, #e5e7f5); border-radius: 12px; background: #fff; }
.admin-table-wrap { overflow-x: auto; background: #fff; border: 1px solid var(--line, #e5e7f5); border-radius: 14px; }
.admin-table { width: 100%; border-collapse: collapse; font-size: .92rem; }
.admin-table th, .admin-table td { text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--line, #e5e7f5); vertical-align: middle; }
.admin-table th { font-size: .78rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted, #667); background: #f8f9ff; }
.admin-table tr:last-child td { border-bottom: 0; }
.admin-actions { white-space: nowrap; text-align: right; }
.admin-actions .btn { margin-left: 6px; }
#admin-form { display: grid; gap: 12px; }
#admin-form textarea, #admin-form select, #admin-form input:not([type=checkbox]) { width: 100%; font: inherit; padding: 9px 12px; border: 1.5px solid var(--line, #e5e7f5); border-radius: 10px; background: #fff; box-sizing: border-box; }
#admin-form textarea { resize: vertical; }
#admin-form .field { display: grid; gap: 4px; font-weight: 600; font-size: .9rem; }
#admin-form .check { display: flex; align-items: center; gap: 8px; font-weight: 600; font-size: .9rem; }
''')

# ------------------------------------------------------------------ static/js/admin.js
write("static/js/admin.js", r'''
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
''')

print("\nDone. Restart the server (Ctrl+C, then python app.py) and open  /admin  while logged in as admin.")
