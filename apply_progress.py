"""
EDUDESK feature: study progress saved in the DATABASE (works on any device after login).
Run once from the EDUDESK folder:   python apply_progress.py
Safe to re-run: files that are already patched are skipped.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent


def find(*names):
    for name in names:
        path = BASE / name
        if path.exists():
            return path
    return None


def patch(path, replacements, marker, label):
    if path is None:
        print(f"! {label}: file not found")
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"- {label}: already patched, skipped")
        return
    for old, _ in replacements:
        if text.count(old) != 1:
            print(f"! {label}: expected code not found, nothing changed.\n    looking for: {old[:80]!r}")
            return
    for old, new in replacements:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"+ {label}: patched")


# ---------------------------------------------------------------- models.py
MODEL = '''

class AktuProgress(db.Model, Serializable):
    """One AKTU unit a student marked as done. Belongs to a user OR to a guest session."""
    __tablename__ = "aktu_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    guest_id = db.Column(db.String(40), index=True)
    subject_code = db.Column(db.String(20), nullable=False, index=True)
    unit_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
'''
models = find("models.py")
if models is None:
    print("! models.py: file not found")
elif "class AktuProgress" in models.read_text(encoding="utf-8"):
    print("- models.py: already patched, skipped")
else:
    models.write_text(models.read_text(encoding="utf-8").rstrip() + "\n" + MODEL, encoding="utf-8")
    print("+ models.py: AktuProgress model added")

# ---------------------------------------------------------------- api.py
API = '''# ============================== AKTU study progress ==============================
@api.get("/aktu/progress")
def get_aktu_progress():
    """{"progress": {"BAS101": [1, 2], ...}} for the logged-in user (or the current guest)."""
    rows = AktuProgress.query.filter(owner_filter(AktuProgress)).all()
    progress = {}
    for row in rows:
        progress.setdefault(row.subject_code, set()).add(row.unit_number)
    return jsonify({"progress": {code: sorted(units) for code, units in progress.items()}})


@api.post("/aktu/progress")
def set_aktu_progress():
    data = get_json_body()
    subject = find_aktu_subject(clean_text(data, "subject_code", "Subject", max_len=20))
    if not subject:
        raise ApiError("Subject not found.", 404)
    unit = to_int(data.get("unit"), "Unit")
    if unit is None or not any(u.number == unit for u in subject.units):
        raise ApiError("Unit not found.", 404)
    done = bool(data.get("done"))
    rows = AktuProgress.query.filter(owner_filter(AktuProgress), AktuProgress.subject_code == subject.code,
                                     AktuProgress.unit_number == unit).all()
    if done and not rows:
        row = AktuProgress(subject_code=subject.code, unit_number=unit)
        assign_owner(row)
        db.session.add(row)
    elif not done:
        for row in rows:
            db.session.delete(row)
    db.session.commit()
    return jsonify({"ok": True, "done": done})


'''
DASH = "# ============================== Dashboard + meta =============================="
patch(find("api.py"), [
    ("AktuSubject, Application, ApplicationHistory,", "AktuProgress, AktuSubject, Application, ApplicationHistory,"),
    (DASH, API + DASH),
], "AktuProgress", "api.py")

# ---------------------------------------------------------------- utils.py (guest progress moves to the account on login)
patch(find("utils.py"), [
    ("from models import Application, Question, SavedService, User, db",
     "from models import AktuProgress, Application, Question, SavedService, User, db"),
    ("for model in (Application, SavedService, Question):", "for model in (Application, SavedService, Question, AktuProgress):"),
], "AktuProgress", "utils.py")

# ---------------------------------------------------------------- static/js/aktu_subject.js
SYNC = '''const SYNC_FLAG = "edudesk_aktu_synced";
/* Progress lives in the database. This browser only keeps a copy (and uploads old local progress once). */
async function syncProgress() {
  try {
    const server = (await api("/api/aktu/progress")).progress || {};
    if (!localStorage.getItem(SYNC_FLAG)) {
      const local = readDone();
      const uploads = [];
      for (const [code, units] of Object.entries(local)) {
        const have = new Set(server[code] || []);
        units.forEach((n) => { if (!have.has(n)) { uploads.push(api("/api/aktu/progress", { method: "POST", body: { subject_code: code, unit: n, done: true } })); server[code] = [...(server[code] || []), n]; } });
      }
      await Promise.allSettled(uploads);
      localStorage.setItem(SYNC_FLAG, "1");
    }
    localStorage.setItem(DONE_KEY, JSON.stringify(server));
    $$(".unit [data-done]").forEach((box) => { box.checked = isDone(Number(box.closest(".unit").dataset.number)); });
    updateProgress();
  } catch (error) { /* offline or error: progress stays in this browser */ }
}

function updateProgress() {'''
patch(find("static/js/aktu_subject.js", "aktu_subject.js"), [
    ("function updateProgress() {", SYNC),
    ("  done ? list.add(number) : list.delete(number);\n",
     "  done ? list.add(number) : list.delete(number);\n"
     '  api("/api/aktu/progress", { method: "POST", body: { subject_code: subject.code, unit: number, done } }).catch(() => {});\n'),
    ("try { renderSubject(await api(`/api/aktu/subjects/${encodeURIComponent(subjectCode)}`)); }",
     "try { renderSubject(await api(`/api/aktu/subjects/${encodeURIComponent(subjectCode)}`)); await syncProgress(); }"),
], "syncProgress", "aktu_subject.js")

# ---------------------------------------------------------------- static/js/aktu.js (subject list shows server progress)
PULL = '''/* Copy progress from the database into this browser so the cards show it on any device. */
async function pullProgress() {
  if (!localStorage.getItem("edudesk_aktu_synced")) return;      // the subject page uploads old local progress first
  try { localStorage.setItem(DONE_KEY, JSON.stringify((await api("/api/aktu/progress")).progress || {})); } catch (error) { /* keep local copy */ }
}

function doneUnits(code) {'''
patch(find("static/js/aktu.js", "aktu.js"), [
    ("function doneUnits(code) {", PULL),
    ('aktuSearch.focus(); });\nloadSubjects();', 'aktuSearch.focus(); });\npullProgress().finally(loadSubjects);'),
], "pullProgress", "aktu.js")

print("\nDone. Restart the server: python app.py   (the new table is created automatically)")
