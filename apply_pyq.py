"""
Adds "Previous Year Papers" (PYQ links) to EDUDESK.
Run once from the EDUDESK folder:   python apply_pyq.py
Safe to re-run: it skips files that are already patched.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent


def patch(filename, replacements, marker):
    path = BASE / filename
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"- {filename}: already patched, skipped")
        return
    for old, new in replacements:
        if text.count(old) != 1:
            print(f"! {filename}: could not find the expected code block:\n    {old[:70]!r}\n  Nothing changed in this file.")
            return
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"+ {filename}: patched")


MODEL = '''

class AktuPaper(db.Model, Serializable):
    """A previous-year question paper (stored as a link, not a file)."""
    __tablename__ = "aktu_papers"
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    exam_session = db.Column(db.String(30), default="")
    paper_type = db.Column(db.String(30), default="Theory")
    official_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
'''
mp = BASE / "models.py"
if "class AktuPaper" not in mp.read_text(encoding="utf-8"):
    mp.write_text(mp.read_text(encoding="utf-8").rstrip() + "\n" + MODEL, encoding="utf-8")
    print("+ models.py: AktuPaper model added")
else:
    print("- models.py: already patched, skipped")

patch("api.py", [
    ("AktuSubject, Application, ApplicationHistory,", "AktuPaper, AktuSubject, Application, ApplicationHistory,"),
    ('    data["units"] = [unit.to_dict() for unit in subject.units]\n    return jsonify(data)',
     '    data["units"] = [unit.to_dict() for unit in subject.units]\n'
     '    codes = [c for c in (subject.code, subject.alt_code) if c]\n'
     '    papers = AktuPaper.query.filter(AktuPaper.subject_code.in_(codes)).order_by(AktuPaper.exam_session.desc(), AktuPaper.id).all()\n'
     '    data["papers"] = [paper.to_dict() for paper in papers]\n'
     '    return jsonify(data)'),
], "AktuPaper")

patch("admin.py", [
    ("from models import (APPLICATION_STATUSES, EXAM_CATEGORIES, SERVICE_CATEGORIES, Application,",
     "from models import (APPLICATION_STATUSES, EXAM_CATEGORIES, SERVICE_CATEGORIES, AktuPaper, Application,"),
    ('    "deadlines": (Deadline,',
     '    "papers": (AktuPaper, ["subject_code", "title", "exam_session", "paper_type", "official_url"], [],\n'
     '               ["subject_code", "title", "official_url"]),\n'
     '    "deadlines": (Deadline,'),
], "AktuPaper")

JS = next((p for p in (BASE / "static" / "js" / "aktu_subject.js", BASE / "aktu_subject.js") if p.exists()), None)
if JS:
    text = JS.read_text(encoding="utf-8")
    if "renderPapers" in text:
        print("- aktu_subject.js: already patched, skipped")
    else:
        func = '''function renderPapers(papers) {
  if (!papers || !papers.length) return "";
  return `<h3 style="margin-top:28px">Previous year papers</h3><ul class="ref-list">${papers.map((p) =>
    `<li><a href="${esc(safeUrl(p.official_url))}" target="_blank" rel="noopener noreferrer">${esc(p.title)}</a>
      <span class="muted small">${[p.exam_session, p.paper_type].filter(Boolean).map(esc).join(" · ")}</span></li>`).join("")}</ul>
    <p class="muted small">Links open the original source. Always verify on the official AKTU website.</p>`;
}

function renderLabs(labs) {'''
        old1, old2 = "function renderLabs(labs) {", "    ${renderLabs(data.labs)}"
        if text.count(old1) == 1 and text.count(old2) == 1:
            text = text.replace(old1, func).replace(old2, "    ${renderPapers(data.papers)}\n    ${renderLabs(data.labs)}")
            JS.write_text(text, encoding="utf-8")
            print(f"+ {JS.name}: patched")
        else:
            print("! aktu_subject.js: expected code not found, nothing changed")
else:
    print("! aktu_subject.js not found (expected in static/js/)")

print("\nDone. Restart the server: python app.py")