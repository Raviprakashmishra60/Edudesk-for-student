"""Small helpers that keep the AKTU study-material data files short and readable."""


def S(text, hint=""):
    """Short-answer question."""
    return {"type": "Short", "q": text, "hint": hint}


def L(text, hint=""):
    """Long / descriptive question."""
    return {"type": "Long", "q": text, "hint": hint}


def N(text, hint=""):
    """Numerical / program-writing question."""
    return {"type": "Numerical", "q": text, "hint": hint}


def chapter(title, topics, summary, points, reference, questions):
    return {"title": title, "topics": topics, "summary": summary, "points": points,
            "reference": reference, "questions": questions}


def merge_chapters(first, second, title):
    """Combine two chapter dicts into one (used when a subject has one chapter too many)."""
    return {"title": title, "topics": first["topics"] + second["topics"], "summary": first["summary"] + " " + second["summary"],
            "points": first["points"] + second["points"], "reference": first["reference"] + second["reference"],
            "questions": first["questions"] + second["questions"]}


def to_subject(data, books, hours=0, code_reference=False):
    """
    Turn a subject written in the short 'chapter' format into the Study Hub format used by the database.
    hours = lecture hours per unit (0 = not known, the page then hides it).
    """
    from database.aktu_content import SUBJECT, U       # imported here to avoid a circular import
    units = []
    for number, item in enumerate(data["chapters"], start=1):
        reference = [("CODE: " + line if code_reference else line) for line in item["reference"]]
        notes = [("Overview", [item["summary"]]), ("Key points", item["points"]), ("Quick reference", reference)]
        questions = [f"{q['type'][0]}: {q['q']}" + (f" || {q['hint']}" if q["hint"] else "") for q in item["questions"]]
        units.append(U(number, item["title"], hours, ", ".join(item["topics"]) + ".", notes, questions))
    codes = [part.strip() for part in data["codes"].split("/")]
    return SUBJECT(codes[0], codes[1] if len(codes) > 1 else None, data["name"], data["category"], data["credits"], data["ltp"],
                   data["about"], books, units, note=data["status_note"])
