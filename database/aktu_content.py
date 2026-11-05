"""
AKTU B.Tech first-year study content (common to all branches except Agriculture Engineering and Biotechnology).

SOURCE OF SYLLABUS: official "Evaluation Scheme and Syllabi - B.Tech 1st Year", Dr. A.P.J. Abdul Kalam Technical University,
Lucknow (effective from session 2022-23). Unit titles, hours and topic lists follow that document.
NOTES and QUESTIONS are ORIGINAL revision material written for EDUDESK - they are NOT AKTU past papers and are
not guaranteed to appear in exams. Always confirm with the latest syllabus on the AKTU website and your textbooks.

Helper format
    U(number, title, hours, syllabus, notes, questions)
        notes     = [("Heading", ["point", "point", ...]), ...]   (a point starting with "CODE:" is shown as code)
        questions = ["S: short question", "L: long question", "N: numerical question"]
"""

KIND = {"S": "short", "L": "long", "N": "numerical"}


def _question(raw):
    """'N: text || hint' -> {"kind", "text", "hint"} (the hint part is optional)."""
    text, _, hint = raw[2:].partition(" || ")
    return {"kind": KIND[raw[0]], "text": text.strip(), "hint": hint.strip()}


def U(number, title, hours, syllabus, notes, questions):
    return {
        "number": number, "title": title, "hours": hours, "syllabus": syllabus,
        "notes": [{"heading": heading, "points": points} for heading, points in notes],
        "questions": [_question(q) for q in questions],
    }


def SUBJECT(code, alt_code, name, category, credits, ltp, objective, books, units, labs=None, note=""):
    """note = how the unit list was prepared. Leave empty only when it was copied from the official AKTU syllabus."""
    return {"code": code, "alt_code": alt_code, "name": name, "category": category, "credits": credits, "ltp": ltp,
            "objective": objective, "books": books, "units": units, "labs": labs or [], "note": note}


def all_subjects():
    """Return every subject, in the order shown on the website."""
    from database.aktu_science import SUBJECTS as science
    from database.aktu_maths import SUBJECTS as maths
    from database.aktu_engineering import SUBJECTS as engineering
    from database.aktu_humanities import SUBJECTS as humanities
    subjects = science + maths + engineering + humanities
    for subject in subjects:                     # quick safety check while seeding
        assert len(subject["units"]) == 5, f"{subject['code']} must have 5 units"
    return subjects
