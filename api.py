"""
EDUDESK REST API (all routes start with /api and return JSON).
"""
import re
import time
from datetime import date

from flask import Blueprint, jsonify, request, session

from assistant import answer_question
from models import (APPLICATION_STATUSES, EXAM_CATEGORIES, SERVICE_CATEGORIES, AktuPaper, AktuProgress, AktuSubject, Application, ApplicationHistory,
                    College, Deadline, Exam, Question, SavedService, Scholarship, Service, User, db)
from utils import (ApiError, assign_owner, claim_guest_data, clean_choice, clean_text, current_user, get_json_body,
                   login_required, owner_filter, rank, to_int)

api = Blueprint("api", __name__, url_prefix="/api")

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_login_attempts = {}          # simple in-memory brute-force guard: {key: [timestamps]}
MAX_ATTEMPTS, LOCK_SECONDS = 5, 300


def lists_contain(values, wanted):
    """True if the list is empty / has 'Any' / 'All' / 'All India' or contains the wanted value."""
    values = values or []
    lowered = [str(v).lower() for v in values]
    if not lowered or any(v in ("any", "all", "all india") for v in lowered):
        return True
    return str(wanted).lower() in lowered


# ============================== Services ==============================
@api.get("/services")
def list_services():
    category = request.args.get("category", "").strip()
    query = request.args.get("q", "").strip()
    stmt = Service.query
    if category:
        stmt = stmt.filter(Service.category == category)
    services = stmt.order_by(Service.category, Service.title).all()
    exact = True
    if query:
        services, exact = rank(services, query,
                               lambda s: f"{s.title} {s.category} {s.description} {s.eligibility} {' '.join(s.documents or [])}")
    return jsonify({"items": [s.to_dict() for s in services], "count": len(services), "exact": exact})


@api.get("/services/<int:service_id>")
def get_service(service_id):
    service = db.session.get(Service, service_id)
    if not service:
        raise ApiError("Service not found.", 404)
    return jsonify(service.to_dict())


# ============================== Scholarships ==============================
def scholarship_checks(scholarship, profile):
    """
    Compare a student profile with a scholarship's (demo) criteria.
    Returns a list of {criterion, passed, message}. Only supplied profile values are checked.
    """
    checks = []
    if profile.get("course"):
        ok = lists_contain(scholarship.courses, profile["course"])
        checks.append({"criterion": "Course", "passed": ok,
                       "message": f"Open to: {', '.join(scholarship.courses or ['Any'])}"})
    if profile.get("level"):
        ok = lists_contain(scholarship.levels, profile["level"])
        checks.append({"criterion": "Class / level", "passed": ok,
                       "message": f"Open to: {', '.join(scholarship.levels or ['Any'])}"})
    if profile.get("state"):
        ok = lists_contain(scholarship.states, profile["state"])
        checks.append({"criterion": "State", "passed": ok,
                       "message": f"Open to: {', '.join(scholarship.states or ['All India'])}"})
    if profile.get("category"):
        ok = lists_contain(scholarship.categories, profile["category"])
        checks.append({"criterion": "Category", "passed": ok,
                       "message": f"Open to: {', '.join(scholarship.categories or ['All'])}"})
    if profile.get("income") is not None:
        ok = scholarship.max_income is None or profile["income"] <= scholarship.max_income
        limit = f"up to Rs {scholarship.max_income:,} per year" if scholarship.max_income else "no income limit listed"
        checks.append({"criterion": "Family income", "passed": ok, "message": f"Demo criteria: {limit}"})
    if profile.get("marks") is not None:
        ok = scholarship.min_marks is None or profile["marks"] >= scholarship.min_marks
        need = f"at least {scholarship.min_marks}%" if scholarship.min_marks else "no minimum marks listed"
        checks.append({"criterion": "Marks", "passed": ok, "message": f"Demo criteria: {need}"})
    if profile.get("type"):
        ok = scholarship.type == profile["type"]
        checks.append({"criterion": "Government / Private", "passed": ok, "message": f"This is a {scholarship.type} scholarship"})
    return checks


def profile_from_args(source):
    """Read the optional filters from query string or JSON body."""
    income = to_int(source.get("income"), "Family income")
    marks = to_int(source.get("marks"), "Marks")
    if marks is not None and not 0 <= marks <= 100:
        raise ApiError("Marks must be between 0 and 100.", 400)
    if income is not None and income < 0:
        raise ApiError("Family income cannot be negative.", 400)
    profile = {key: (str(source.get(key) or "").strip()) for key in ("course", "level", "state", "category", "type")}
    profile = {key: value for key, value in profile.items() if value}
    profile["income"], profile["marks"] = income, marks
    return profile


@api.get("/scholarships")
def list_scholarships():
    profile = profile_from_args(request.args)
    query = request.args.get("q", "").strip()
    scholarships = Scholarship.query.order_by(Scholarship.name).all()
    if query:
        scholarships, _ = rank(scholarships, query, lambda s: f"{s.name} {s.provider} {s.description} {s.eligibility}")
    items = [s for s in scholarships if all(c["passed"] for c in scholarship_checks(s, profile))]
    return jsonify({"items": [s.to_dict() for s in items], "count": len(items)})


@api.get("/scholarships/<int:scholarship_id>")
def get_scholarship(scholarship_id):
    scholarship = db.session.get(Scholarship, scholarship_id)
    if not scholarship:
        raise ApiError("Scholarship not found.", 404)
    return jsonify(scholarship.to_dict())


@api.post("/scholarships/<int:scholarship_id>/check")
def check_scholarship(scholarship_id):
    scholarship = db.session.get(Scholarship, scholarship_id)
    if not scholarship:
        raise ApiError("Scholarship not found.", 404)
    profile = profile_from_args(get_json_body())
    checks = scholarship_checks(scholarship, profile)
    if not checks:
        raise ApiError("Enter at least one detail (course, state, income ...) to check eligibility.", 400)
    passed = all(c["passed"] for c in checks)
    verdict = ("Looks like a match based on the demo criteria." if passed
               else "Some demo criteria do not match your details.")
    return jsonify({"eligible": passed, "verdict": verdict, "checks": checks,
                    "note": "Demo data — verify on the official website before applying."})


# ============================== Colleges ==============================
@api.get("/colleges")
def list_colleges():
    args = request.args
    colleges = College.query.order_by(College.name).all()
    if args.get("q", "").strip():
        colleges, _ = rank(colleges, args["q"], lambda c: f"{c.name} {c.city} {c.state} {' '.join(c.courses or [])}")
    if args.get("course"):
        colleges = [c for c in colleges if lists_contain(c.courses, args["course"]) and c.courses]
    if args.get("state"):
        colleges = [c for c in colleges if c.state.lower() == args["state"].lower()]
    if args.get("city"):
        colleges = [c for c in colleges if c.city.lower() == args["city"].lower()]
    if args.get("type"):
        colleges = [c for c in colleges if c.type.lower() == args["type"].lower()]
    if args.get("exam"):
        colleges = [c for c in colleges if str(args["exam"]).lower() in [e.lower() for e in (c.entrance_exams or [])]]
    if args.get("fees"):
        colleges = [c for c in colleges if c.fee_band.lower() == args["fees"].lower()]
    return jsonify({"items": [c.to_dict() for c in colleges], "count": len(colleges)})


@api.get("/colleges/<int:college_id>")
def get_college(college_id):
    college = db.session.get(College, college_id)
    if not college:
        raise ApiError("College not found.", 404)
    return jsonify(college.to_dict())


# ============================== Exams ==============================
@api.get("/exams")
def list_exams():
    category = request.args.get("category", "").strip()
    query = request.args.get("q", "").strip()
    stmt = Exam.query
    if category:
        stmt = stmt.filter(Exam.category == category)
    exams = stmt.order_by(Exam.name).all()
    if query:
        exams, _ = rank(exams, query, lambda e: f"{e.name} {e.category} {e.description} {e.eligibility}")
    return jsonify({"items": [e.to_dict() for e in exams], "count": len(exams)})


@api.get("/exams/<int:exam_id>")
def get_exam(exam_id):
    exam = db.session.get(Exam, exam_id)
    if not exam:
        raise ApiError("Exam not found.", 404)
    return jsonify(exam.to_dict())


# ============================== Deadlines ==============================
def deadline_dict(deadline, today):
    data = deadline.to_dict()
    data["days_left"] = (deadline.date - today).days
    data["label"] = "Verified from official source" if deadline.is_verified else "Demo data — not a real deadline"
    return data


@api.get("/deadlines")
def list_deadlines():
    today = date.today()
    stmt = Deadline.query
    if request.args.get("category"):
        stmt = stmt.filter(Deadline.category == request.args["category"])
    rows = [deadline_dict(d, today) for d in stmt.order_by(Deadline.date).all()]
    return jsonify({
        "today": today.isoformat(),
        "reminders": [d for d in rows if 0 <= d["days_left"] <= 7],      # happening within a week
        "upcoming": [d for d in rows if d["days_left"] > 7],
        "past": sorted([d for d in rows if d["days_left"] < 0], key=lambda d: d["days_left"], reverse=True),
    })


# ============================== Ask EDUDESK ==============================
@api.post("/ask")
def ask():
    question = clean_text(get_json_body(), "question", "Question", max_len=500)
    if len(question) < 3:
        raise ApiError("Please type a longer question.", 400)
    result = answer_question(question)
    record = Question(text=question, answer_summary=result["sections"][0]["text"][:300])
    assign_owner(record)
    db.session.add(record)
    db.session.commit()
    return jsonify(result)


@api.get("/questions/recent")
def recent_questions():
    rows = Question.query.filter(owner_filter(Question)).order_by(Question.id.desc()).limit(8).all()
    return jsonify({"items": [q.to_dict() for q in rows]})


# ============================== Applications ==============================
def get_owned_application(application_id):
    application = Application.query.filter(Application.id == application_id, owner_filter(Application)).first()
    if not application:
        raise ApiError("Application not found.", 404)
    return application


def add_history(application, note=""):
    db.session.add(ApplicationHistory(application=application, status=application.status, note=note))


@api.get("/applications")
def list_applications():
    rows = Application.query.filter(owner_filter(Application)).order_by(Application.updated_at.desc()).all()
    return jsonify({"items": [a.to_dict() for a in rows], "count": len(rows), "statuses": APPLICATION_STATUSES})


@api.post("/applications")
def create_application():
    data = get_json_body()
    user = current_user()
    application = Application(
        student_name=clean_text(data, "student_name", "Student name", 80, required=not user, default=user.name if user else ""),
        title=clean_text(data, "title", "Title", 150),
        category=clean_choice(data, "category", "Category", SERVICE_CATEGORIES + ["Other"], default="Other"),
        status=clean_choice(data, "status", "Status", APPLICATION_STATUSES, default="Not Started"),
        notes=clean_text(data, "notes", "Notes", 500, required=False),
    )
    assign_owner(application)
    db.session.add(application)
    add_history(application, "Application added")
    db.session.commit()
    return jsonify(application.to_dict()), 201


@api.patch("/applications/<int:application_id>")
def update_application(application_id):
    application = get_owned_application(application_id)
    data = get_json_body()
    old_status = application.status
    if "student_name" in data:
        application.student_name = clean_text(data, "student_name", "Student name", 80)
    if "title" in data:
        application.title = clean_text(data, "title", "Title", 150)
    if "category" in data:
        application.category = clean_choice(data, "category", "Category", SERVICE_CATEGORIES + ["Other"])
    if "notes" in data:
        application.notes = clean_text(data, "notes", "Notes", 500, required=False)
    if "status" in data:
        application.status = clean_choice(data, "status", "Status", APPLICATION_STATUSES)
    if application.status != old_status:
        add_history(application, f"Status changed from {old_status}")
    db.session.commit()
    return jsonify(application.to_dict())


@api.delete("/applications/<int:application_id>")
def delete_application(application_id):
    db.session.delete(get_owned_application(application_id))
    db.session.commit()
    return jsonify({"ok": True})


@api.get("/applications/<int:application_id>/history")
def application_history(application_id):
    application = get_owned_application(application_id)
    return jsonify({"application": application.to_dict(), "history": [h.to_dict() for h in application.history]})


# ============================== Saved services ==============================
@api.get("/saved")
def list_saved():
    rows = SavedService.query.filter(owner_filter(SavedService)).order_by(SavedService.id.desc()).all()
    return jsonify({"service_ids": [r.service_id for r in rows], "items": [r.service.to_dict() for r in rows]})


@api.post("/saved")
def save_service():
    service_id = to_int(get_json_body().get("service_id"), "Service id")
    if not service_id or not db.session.get(Service, service_id):
        raise ApiError("Service not found.", 404)
    exists = SavedService.query.filter(SavedService.service_id == service_id, owner_filter(SavedService)).first()
    if not exists:
        row = SavedService(service_id=service_id)
        assign_owner(row)
        db.session.add(row)
        db.session.commit()
    return jsonify({"ok": True, "saved": True}), 201


@api.delete("/saved/<int:service_id>")
def unsave_service(service_id):
    SavedService.query.filter(SavedService.service_id == service_id, owner_filter(SavedService)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"ok": True, "saved": False})


# ============================== AKTU Study Hub ==============================
def aktu_summary(subject):
    data = subject.to_dict()
    for heavy in ("objective", "books", "labs"):
        data.pop(heavy, None)
    data["unit_count"] = len(subject.units)
    data["question_count"] = sum(len(unit.questions or []) for unit in subject.units)
    data["unit_titles"] = [unit.title for unit in subject.units]
    return data


@api.get("/aktu/subjects")
def list_aktu_subjects():
    category = request.args.get("category", "").strip()
    query = request.args.get("q", "").strip()
    subjects = AktuSubject.query.order_by(AktuSubject.sort_order).all()
    if category:
        subjects = [s for s in subjects if s.category == category]
    if query:
        subjects, _ = rank(subjects, query, lambda s: f"{s.code} {s.alt_code or ''} {s.name} {s.category} " +
                           " ".join(f"{u.title} {u.syllabus}" for u in s.units))
    return jsonify({"items": [aktu_summary(s) for s in subjects], "count": len(subjects)})


def find_aktu_subject(code):
    code = (code or "").strip().upper()
    return AktuSubject.query.filter((AktuSubject.code == code) | (AktuSubject.alt_code == code)).first()


@api.get("/aktu/subjects/<code>")
def get_aktu_subject(code):
    subject = find_aktu_subject(code)
    if not subject:
        raise ApiError("Subject not found.", 404)
    data = subject.to_dict()
    data["units"] = [unit.to_dict() for unit in subject.units]
    codes = [c for c in (subject.code, subject.alt_code) if c]
    papers = AktuPaper.query.filter(AktuPaper.subject_code.in_(codes)).order_by(AktuPaper.exam_session.desc(), AktuPaper.id).all()
    data["papers"] = [paper.to_dict() for paper in papers]
    return jsonify(data)


# ============================== AKTU study progress ==============================
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


# ============================== Dashboard + meta ==============================
@api.get("/dashboard")
def dashboard_summary():
    today = date.today()
    applications = Application.query.filter(owner_filter(Application)).all()
    by_status = {status: 0 for status in APPLICATION_STATUSES}
    for application in applications:
        by_status[application.status] = by_status.get(application.status, 0) + 1
    upcoming = Deadline.query.filter(Deadline.date >= today).order_by(Deadline.date).limit(5).all()
    return jsonify({
        "user": current_user().public_dict() if current_user() else None,
        "applications_total": len(applications),
        "applications_by_status": by_status,
        "saved_total": SavedService.query.filter(owner_filter(SavedService)).count(),
        "questions_total": Question.query.filter(owner_filter(Question)).count(),
        "upcoming_deadlines": [deadline_dict(d, today) for d in upcoming],
    })


@api.get("/meta")
def meta():
    """Option lists used to fill the filter dropdowns."""
    colleges = College.query.all()
    scholarships = Scholarship.query.all()
    scholarship_states = sorted({s for sch in scholarships for s in (sch.states or []) if s.lower() != "all india"})
    return jsonify({
        "service_categories": SERVICE_CATEGORIES,
        "exam_categories": EXAM_CATEGORIES,
        "statuses": APPLICATION_STATUSES,
        "college_states": sorted({c.state for c in colleges}),
        "college_cities": sorted({c.city for c in colleges}),
        "college_courses": sorted({course for c in colleges for course in (c.courses or [])}),
        "college_exams": sorted({exam for c in colleges for exam in (c.entrance_exams or [])}),
        "scholarship_states": scholarship_states,
    })


# ============================== Accounts ==============================
def _attempt_key(email):
    return f"{request.remote_addr}:{email}"


def _check_lock(key):
    now = time.time()
    recent = [t for t in _login_attempts.get(key, []) if now - t < LOCK_SECONDS]
    _login_attempts[key] = recent
    if len(recent) >= MAX_ATTEMPTS:
        raise ApiError("Too many failed attempts. Please try again in a few minutes.", 429)


@api.post("/register")
def register():
    data = get_json_body()
    name = clean_text(data, "name", "Name", 80)
    email = clean_text(data, "email", "Email", 120).lower()
    password = data.get("password", "")
    if len(name) < 2:
        raise ApiError("Name must be at least 2 characters.", 400)
    if not EMAIL_PATTERN.match(email):
        raise ApiError("Enter a valid email address.", 400)
    if not isinstance(password, str) or not 8 <= len(password) <= 72:
        raise ApiError("Password must be 8 to 72 characters.", 400)
    if not (re.search(r"[A-Za-z]", password) and re.search(r"\d", password)):
        raise ApiError("Password must contain at least one letter and one number.", 400)
    if User.query.filter_by(email=email).first():
        raise ApiError("An account with this email already exists. Please log in.", 409)
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    claim_guest_data(user)                       # keep what the guest already did
    session.clear()
    session["user_id"] = user.id
    session.permanent = True
    return jsonify({"user": user.public_dict()}), 201


@api.post("/login")
def login():
    data = get_json_body()
    email = clean_text(data, "email", "Email", 120).lower()
    password = data.get("password", "")
    key = _attempt_key(email)
    _check_lock(key)
    user = User.query.filter_by(email=email).first()
    if not user or not isinstance(password, str) or not user.check_password(password):
        _login_attempts.setdefault(key, []).append(time.time())
        raise ApiError("Invalid email or password.", 401)
    _login_attempts.pop(key, None)
    claim_guest_data(user)
    session.clear()
    session["user_id"] = user.id
    session.permanent = True
    return jsonify({"user": user.public_dict()})


@api.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@api.get("/me")
def me():
    user = current_user()
    return jsonify({"user": user.public_dict() if user else None})
