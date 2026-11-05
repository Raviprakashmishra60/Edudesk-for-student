"""
EDUDESK - Full-stack Student Education Platform
Flask + SQLAlchemy + SQLite
"""

import os
from datetime import datetime, date
from functools import wraps

from flask import (
    Flask, render_template, request, jsonify, session,
    redirect, url_for, flash, abort
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "edudesk-dev-secret-change-in-production")
_basedir = os.path.abspath(os.path.dirname(__file__))
_default_db = "sqlite:///" + os.path.join(_basedir, "edudesk.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", _default_db)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ============================================================
# MODELS
# ============================================================

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="user", lazy=True)
    saved_services = db.relationship("SavedService", backref="user", lazy=True)
    questions = db.relationship("Question", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    required_documents = db.Column(db.Text)
    application_steps = db.Column(db.Text)
    important_dates = db.Column(db.String(300))
    official_website = db.Column(db.String(300))
    is_demo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "eligibility": self.eligibility,
            "required_documents": self.required_documents,
            "application_steps": self.application_steps,
            "important_dates": self.important_dates,
            "official_website": self.official_website,
            "is_demo": self.is_demo,
        }


class Scholarship(db.Model):
    __tablename__ = "scholarships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(150))
    course = db.Column(db.String(100))
    class_level = db.Column(db.String(50))
    state = db.Column(db.String(80))
    category = db.Column(db.String(50))  # General / SC / ST / OBC / EWS
    family_income_max = db.Column(db.String(50))
    marks_min = db.Column(db.String(50))
    provider_type = db.Column(db.String(50))  # Government / Private
    eligibility = db.Column(db.Text)
    benefit = db.Column(db.String(200))
    last_date = db.Column(db.String(100))
    documents = db.Column(db.Text)
    official_link = db.Column(db.String(300))
    is_demo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "course": self.course,
            "class_level": self.class_level,
            "state": self.state,
            "category": self.category,
            "family_income_max": self.family_income_max,
            "marks_min": self.marks_min,
            "provider_type": self.provider_type,
            "eligibility": self.eligibility,
            "benefit": self.benefit,
            "last_date": self.last_date,
            "documents": self.documents,
            "official_link": self.official_link,
            "is_demo": self.is_demo,
        }


class College(db.Model):
    __tablename__ = "colleges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(150))
    state = db.Column(db.String(80))
    city = db.Column(db.String(80))
    courses = db.Column(db.Text)
    college_type = db.Column(db.String(50))  # Government / Private
    entrance_exam = db.Column(db.String(100))
    fees_range = db.Column(db.String(100))
    eligibility = db.Column(db.Text)
    admission_process = db.Column(db.Text)
    official_website = db.Column(db.String(300))
    is_demo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "state": self.state,
            "city": self.city,
            "courses": self.courses,
            "college_type": self.college_type,
            "entrance_exam": self.entrance_exam,
            "fees_range": self.fees_range,
            "eligibility": self.eligibility,
            "admission_process": self.admission_process,
            "official_website": self.official_website,
            "is_demo": self.is_demo,
        }


class Exam(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))  # Engineering, Medical, etc.
    eligibility = db.Column(db.Text)
    registration_process = db.Column(db.Text)
    documents = db.Column(db.Text)
    official_website = db.Column(db.String(300))
    important_dates = db.Column(db.String(300))
    is_demo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "eligibility": self.eligibility,
            "registration_process": self.registration_process,
            "documents": self.documents,
            "official_website": self.official_website,
            "important_dates": self.important_dates,
            "is_demo": self.is_demo,
        }


class Deadline(db.Model):
    __tablename__ = "deadlines"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    date = db.Column(db.String(50))
    description = db.Column(db.Text)
    official_url = db.Column(db.String(300))
    is_demo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "date": self.date,
            "description": self.description,
            "official_url": self.official_url,
            "is_demo": self.is_demo,
        }


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    student_name = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    status = db.Column(db.String(50), default="Not Started")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_name": self.student_name,
            "title": self.title,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class SavedService(db.Model):
    __tablename__ = "saved_services"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "question_text": self.question_text,
            "answer_text": self.answer_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class StudyMaterial(db.Model):
    """AKTU / engineering syllabus study materials — real curriculum structure."""
    __tablename__ = "study_materials"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    subject_code = db.Column(db.String(50))
    university = db.Column(db.String(100), default="AKTU")
    branch = db.Column(db.String(100))  # Common / CSE / AI etc.
    semester = db.Column(db.String(50))
    unit_number = db.Column(db.Integer)
    unit_title = db.Column(db.String(200))
    topics = db.Column(db.Text)  # bullet topics
    key_concepts = db.Column(db.Text)
    important_questions = db.Column(db.Text)
    study_tips = db.Column(db.Text)
    recommended_books = db.Column(db.Text)
    resources = db.Column(db.Text)  # free links NPTEL etc.
    category = db.Column(db.String(80))  # Mathematics / Artificial Intelligence
    difficulty = db.Column(db.String(40))

    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "subject_code": self.subject_code,
            "university": self.university,
            "branch": self.branch,
            "semester": self.semester,
            "unit_number": self.unit_number,
            "unit_title": self.unit_title,
            "topics": self.topics,
            "key_concepts": self.key_concepts,
            "important_questions": self.important_questions,
            "study_tips": self.study_tips,
            "recommended_books": self.recommended_books,
            "resources": self.resources,
            "category": self.category,
            "difficulty": self.difficulty,
        }


# ============================================================
# HELPERS
# ============================================================

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Authentication required"}), 401
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None


# Rule-based Ask EDUDESK assistant
def ask_assistant(question: str) -> dict:
    q = question.lower().strip()
    source = "general_guidance"
    answer = ""

    # Keyword rules (demo knowledge base)
    rules = [
        (
            ["matrix", "matrices", "eigen", "cayley"],
            "AKTU Engineering Mathematics-I (BAS103) Unit 1 covers Matrices: elementary transformations, rank, inverse, linear systems, Cayley-Hamilton, eigen values/vectors, Hermitian matrices. Practice rank by row operations and Cayley-Hamilton for inverse. See Study Materials → Maths-I Unit 1 on EDUDESK.",
            "edudesk_db",
        ),
        (
            ["fourier", "beta", "gamma", "complex variable"],
            "These topics appear in AKTU Engineering Mathematics-II (and related papers): Fourier series, Beta/Gamma functions, complex integration & residues. Open Study Materials on EDUDESK for unit-wise topics, key concepts and important question types. Confirm exact unit mapping on aktu.ac.in for your batch.",
            "edudesk_db",
        ),
        (
            ["partial differential", "pde", "heat equation", "wave equation"],
            "AKTU Mathematics-IV typically includes PDEs and applications (wave, heat, Laplace) plus statistical techniques. Use EDUDESK Study Materials → Maths-IV units. Always verify with the official BAS303/BAS403 syllabus PDF.",
            "edudesk_db",
        ),
        (
            ["artificial intelligence", "minimax", "alpha-beta", "a* search", "bayesian network"],
            "AKTU Artificial Intelligence units usually cover: intelligent agents, uninformed/informed search (BFS, DFS, A*), adversarial search (Minimax, Alpha-Beta), knowledge representation (FOL, resolution), uncertainty & learning, and applications (NLP, expert systems). Open Study Materials → Artificial Intelligence on EDUDESK for unit guides.",
            "edudesk_db",
        ),
        (
            ["bas103", "engineering mathematics"],
            "Engineering Mathematics-I (BAS103) at AKTU is commonly structured as: Unit1 Matrices, Unit2 Differential Calculus-I, Unit3 Differential Calculus-II, Unit4 Multiple Integration, Unit5 Vector Calculus. Full unit guides with tips and books are under Study Materials on EDUDESK. Download your session PDF from aktu.ac.in.",
            "edudesk_db",
        ),
        (
            ["document", "documents", "scholarship"],
            "Common documents for most scholarships include: Aadhaar card, income certificate, "
            "caste certificate (if applicable), mark sheets (10th/12th), bank passbook, "
            "passport-size photo, and domicile certificate. Always check the official notification "
            "for the exact list — requirements vary by scheme.",
            "edudesk_db",
        ),
        (
            ["jee", "form", "document"],
            "For JEE Main registration, typically you need: Class 10 & 12 mark sheets, "
            "Aadhaar or other ID, passport photo, signature image, and category certificate if applicable. "
            "Photo and signature must meet NTA size/format guidelines. Verify on jeemain.nta.nic.in.",
            "official_source",
        ),
        (
            ["btech", "admission", "apply"],
            "BTech admission usually happens via entrance exams (JEE Main / state CETs) or management quota. "
            "Steps: 1) Appear for required exam 2) Register for counselling 3) Choose colleges 4) Document verification "
            "5) Fee payment. Check the specific college or state counselling portal for exact process.",
            "general_guidance",
        ),
        (
            ["cse", "it", "difference"],
            "CSE (Computer Science & Engineering) focuses more on software, algorithms, theory and core computing. "
            "IT (Information Technology) emphasizes applications, networks, databases and business systems. "
            "Both open similar career paths; CSE is often slightly more theory-heavy. Choose based on interest.",
            "general_guidance",
        ),
        (
            ["after 12th", "what should i do", "career"],
            "After 12th you can: pursue engineering (JEE), medical (NEET), pure sciences, commerce (CA/CS), "
            "design, law, or skill-based courses. Map your interests + strengths, research entrance exams, "
            "and shortlist colleges. Use EDUDESK Exam Center and College Finder for structured exploration.",
            "general_guidance",
        ),
        (
            ["eligibility", "scholarship"],
            "Scholarship eligibility often depends on: family income limit, category (SC/ST/OBC/EWS), "
            "marks percentage, course/stream, and domicile state. Use the Scholarship Finder filters "
            "and then verify on the official portal — demo data here is illustrative only.",
            "edudesk_db",
        ),
        (
            ["income certificate", "how to get"],
            "Income certificate is usually issued by the Tehsildar / Revenue department of your district. "
            "Apply online via your state e-district portal or offline at the local office with proof of income "
            "(salary slips, ITR, or affidavit). Validity is often 1 year — check local rules.",
            "general_guidance",
        ),
        (
            ["neet", "document"],
            "NEET registration typically needs: Class 10 & 12 certificates, photo, signature, "
            "Aadhaar/ID proof, and category certificate if applicable. Follow NTA photo specifications. "
            "Confirm on the official NEET website before applying.",
            "official_source",
        ),
    ]

    matched = False
    best_score = 0
    for keywords, ans, src in rules:
        score = sum(1 for k in keywords if k in q)
        need = 1 if len(keywords) == 1 else min(2, len(keywords))
        if score >= need and score > best_score:
            answer = ans
            source = src
            matched = True
            best_score = score

    if not matched:
        # Broader single-keyword fallbacks
        fallbacks = [
            ("scholarship", "Browse Scholarships on EDUDESK, filter by course/state/income, and always verify eligibility and deadlines on the official website. Demo data is labelled clearly."),
            ("college", "Use College Finder to search by course, state, city and fees. Check official college websites for current admission rules."),
            ("exam", "Visit Exam Center for eligibility, documents and official links. Dates change yearly — always confirm on the official exam portal."),
            ("document", "Document requirements vary. Common ones: Aadhaar, mark sheets, income/caste certificates, photos. Use Document Center for size/format guidance."),
            ("deadline", "See Deadlines section for demo reminders. Never rely solely on third-party dates; verify official notifications."),
            ("loan", "Education loans are offered by banks and schemes like Vidya Lakshmi. Eligibility depends on course, co-applicant income and collateral. Visit bank portals for current rates."),
            ("internship", "Look for internships on official college placement cells, government portals (e.g. NATS), and company career pages. Keep resume and ID documents ready."),
        ]
        for key, ans in fallbacks:
            if key in q:
                answer = ans
                source = "edudesk_db"
                matched = True
                break

    if not matched:
        answer = (
            "I can help with scholarships, admissions, exams, documents and career guidance. "
            "Try asking more specifically, e.g. “What documents are required for scholarship?” "
            "or “How can I apply for BTech admission?”. For current rules and deadlines, always verify on official websites."
        )
        source = "general_guidance"

    disclaimer = (
        "\n\n⚠️ This is general guidance based on common practices and EDUDESK demo data. "
        "Always verify current rules, eligibility and deadlines on the official notification or website."
    )

    return {
        "answer": answer + disclaimer,
        "source": source,
        "source_label": {
            "general_guidance": "General guidance",
            "edudesk_db": "Information from EDUDESK database",
            "official_source": "Based on typical official requirements (verify officially)",
        }.get(source, "General guidance"),
    }


# ============================================================
# PAGE ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template("index.html", user=get_current_user())


@app.route("/services")
def services_page():
    return render_template("services.html", user=get_current_user())


@app.route("/scholarships")
def scholarships_page():
    return render_template("scholarships.html", user=get_current_user())


@app.route("/colleges")
def colleges_page():
    return render_template("colleges.html", user=get_current_user())


@app.route("/exams")
def exams_page():
    return render_template("exams.html", user=get_current_user())


@app.route("/ask")
def ask_page():
    return render_template("ask.html", user=get_current_user())


@app.route("/documents")
def documents_page():
    return render_template("documents.html", user=get_current_user())


@app.route("/study")
def study_page():
    return render_template("study.html", user=get_current_user())


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=get_current_user())


@app.route("/login", methods=["GET"])
def login_page():
    if get_current_user():
        return redirect(url_for("dashboard"))
    return render_template("login.html", user=None)


@app.route("/register", methods=["GET"])
def register_page():
    if get_current_user():
        return redirect(url_for("dashboard"))
    return render_template("register.html", user=None)


# ============================================================
# AUTH API
# ============================================================

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    session["user_id"] = user.id
    session["user_name"] = user.name
    return jsonify({"message": "Registered successfully", "user": user.to_dict()}), 201


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user.id
    session["user_name"] = user.name
    return jsonify({"message": "Logged in", "user": user.to_dict()})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/api/me")
def api_me():
    user = get_current_user()
    if not user:
        return jsonify({"user": None})
    return jsonify({"user": user.to_dict()})


# ============================================================
# SERVICES API
# ============================================================

@app.route("/api/services")
def api_services():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    query = Service.query
    if category:
        query = query.filter(Service.category.ilike(f"%{category}%"))
    if q:
        query = query.filter(
            db.or_(
                Service.title.ilike(f"%{q}%"),
                Service.description.ilike(f"%{q}%"),
                Service.category.ilike(f"%{q}%"),
            )
        )
    items = query.order_by(Service.title).all()
    return jsonify({"services": [s.to_dict() for s in items], "count": len(items)})


@app.route("/api/services/<int:sid>")
def api_service_detail(sid):
    s = Service.query.get_or_404(sid)
    return jsonify(s.to_dict())


# ============================================================
# SCHOLARSHIPS API
# ============================================================

@app.route("/api/scholarships")
def api_scholarships():
    q = request.args.get("q", "").strip().lower()
    course = request.args.get("course", "").strip()
    state = request.args.get("state", "").strip()
    category = request.args.get("category", "").strip()
    provider_type = request.args.get("provider_type", "").strip()
    class_level = request.args.get("class_level", "").strip()

    query = Scholarship.query
    if course:
        query = query.filter(Scholarship.course.ilike(f"%{course}%"))
    if state:
        query = query.filter(Scholarship.state.ilike(f"%{state}%"))
    if category:
        query = query.filter(Scholarship.category.ilike(f"%{category}%"))
    if provider_type:
        query = query.filter(Scholarship.provider_type.ilike(f"%{provider_type}%"))
    if class_level:
        query = query.filter(Scholarship.class_level.ilike(f"%{class_level}%"))
    if q:
        query = query.filter(
            db.or_(
                Scholarship.name.ilike(f"%{q}%"),
                Scholarship.provider.ilike(f"%{q}%"),
                Scholarship.eligibility.ilike(f"%{q}%"),
            )
        )
    items = query.order_by(Scholarship.name).all()
    return jsonify({"scholarships": [s.to_dict() for s in items], "count": len(items)})


@app.route("/api/scholarships/<int:sid>")
def api_scholarship_detail(sid):
    s = Scholarship.query.get_or_404(sid)
    return jsonify(s.to_dict())


# ============================================================
# COLLEGES API
# ============================================================

@app.route("/api/colleges")
def api_colleges():
    q = request.args.get("q", "").strip().lower()
    course = request.args.get("course", "").strip()
    state = request.args.get("state", "").strip()
    city = request.args.get("city", "").strip()
    college_type = request.args.get("college_type", "").strip()
    entrance = request.args.get("entrance_exam", "").strip()

    query = College.query
    if course:
        query = query.filter(College.courses.ilike(f"%{course}%"))
    if state:
        query = query.filter(College.state.ilike(f"%{state}%"))
    if city:
        query = query.filter(College.city.ilike(f"%{city}%"))
    if college_type:
        query = query.filter(College.college_type.ilike(f"%{college_type}%"))
    if entrance:
        query = query.filter(College.entrance_exam.ilike(f"%{entrance}%"))
    if q:
        query = query.filter(
            db.or_(
                College.name.ilike(f"%{q}%"),
                College.location.ilike(f"%{q}%"),
                College.courses.ilike(f"%{q}%"),
            )
        )
    items = query.order_by(College.name).all()
    return jsonify({"colleges": [c.to_dict() for c in items], "count": len(items)})


@app.route("/api/colleges/<int:cid>")
def api_college_detail(cid):
    c = College.query.get_or_404(cid)
    return jsonify(c.to_dict())


# ============================================================
# EXAMS API
# ============================================================

@app.route("/api/exams")
def api_exams():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    query = Exam.query
    if category:
        query = query.filter(Exam.category.ilike(f"%{category}%"))
    if q:
        query = query.filter(
            db.or_(
                Exam.name.ilike(f"%{q}%"),
                Exam.eligibility.ilike(f"%{q}%"),
            )
        )
    items = query.order_by(Exam.name).all()
    return jsonify({"exams": [e.to_dict() for e in items], "count": len(items)})


@app.route("/api/exams/<int:eid>")
def api_exam_detail(eid):
    e = Exam.query.get_or_404(eid)
    return jsonify(e.to_dict())


# ============================================================
# DEADLINES API
# ============================================================

@app.route("/api/deadlines")
def api_deadlines():
    items = Deadline.query.order_by(Deadline.id).all()
    return jsonify({"deadlines": [d.to_dict() for d in items], "count": len(items)})


# ============================================================
# ASK API
# ============================================================

@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.get_json() or {}
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Question is required"}), 400
    if len(question) > 1000:
        return jsonify({"error": "Question too long"}), 400

    result = ask_assistant(question)

    # Optionally store question
    user = get_current_user()
    rec = Question(
        user_id=user.id if user else None,
        question_text=question,
        answer_text=result["answer"],
    )
    db.session.add(rec)
    db.session.commit()

    return jsonify({
        "question": question,
        "answer": result["answer"],
        "source": result["source"],
        "source_label": result["source_label"],
        "id": rec.id,
    })


# ============================================================
# APPLICATIONS API
# ============================================================

@app.route("/api/applications", methods=["GET"])
def api_applications_list():
    user = get_current_user()
    if user:
        apps = Application.query.filter_by(user_id=user.id).order_by(Application.updated_at.desc()).all()
    else:
        # Guest: return empty or session-based; keep simple — empty
        apps = []
    return jsonify({"applications": [a.to_dict() for a in apps], "count": len(apps)})


@app.route("/api/applications", methods=["POST"])
def api_applications_create():
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    student_name = (data.get("student_name") or "").strip()
    category = (data.get("category") or "").strip()
    status = (data.get("status") or "Not Started").strip()

    valid_statuses = ["Not Started", "Documents Ready", "Applied", "Under Review", "Approved", "Rejected"]
    if status not in valid_statuses:
        status = "Not Started"
    if not title or not student_name:
        return jsonify({"error": "title and student_name are required"}), 400

    user = get_current_user()
    app_obj = Application(
        user_id=user.id if user else None,
        student_name=student_name,
        title=title,
        category=category or "General",
        status=status,
    )
    db.session.add(app_obj)
    db.session.commit()
    return jsonify(app_obj.to_dict()), 201


@app.route("/api/applications/<int:aid>", methods=["PATCH"])
def api_applications_update(aid):
    app_obj = Application.query.get_or_404(aid)
    user = get_current_user()
    if user and app_obj.user_id and app_obj.user_id != user.id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    if "title" in data:
        app_obj.title = data["title"].strip()
    if "student_name" in data:
        app_obj.student_name = data["student_name"].strip()
    if "category" in data:
        app_obj.category = data["category"].strip()
    if "status" in data:
        valid = ["Not Started", "Documents Ready", "Applied", "Under Review", "Approved", "Rejected"]
        if data["status"] in valid:
            app_obj.status = data["status"]
    app_obj.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(app_obj.to_dict())


@app.route("/api/applications/<int:aid>", methods=["DELETE"])
def api_applications_delete(aid):
    app_obj = Application.query.get_or_404(aid)
    user = get_current_user()
    if user and app_obj.user_id and app_obj.user_id != user.id:
        return jsonify({"error": "Forbidden"}), 403
    db.session.delete(app_obj)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ============================================================
# PROFILE + SAVED SERVICES API
# ============================================================

@app.route("/api/profile", methods=["GET", "PATCH"])
@login_required
def api_profile():
    user = get_current_user()
    if request.method == "GET":
        return jsonify({"user": user.to_dict()})

    data = request.get_json() or {}
    if "name" in data:
        name = str(data.get("name") or "").strip()
        if not name:
            return jsonify({"error": "Name cannot be empty"}), 400
        user.name = name
        session["user_name"] = name

    if "email" in data:
        email = str(data.get("email") or "").strip().lower()
        if not email:
            return jsonify({"error": "Email cannot be empty"}), 400
        existing = User.query.filter(User.email == email, User.id != user.id).first()
        if existing:
            return jsonify({"error": "Email already registered"}), 409
        user.email = email

    if "password" in data:
        password = str(data.get("password") or "")
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        user.set_password(password)

    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user.to_dict()})


@app.route("/api/saved-services", methods=["GET", "POST"])
@login_required
def api_saved_services():
    user = get_current_user()

    if request.method == "GET":
        rows = SavedService.query.filter_by(user_id=user.id).order_by(SavedService.created_at.desc()).all()
        service_ids = [row.service_id for row in rows]
        services = Service.query.filter(Service.id.in_(service_ids)).all() if service_ids else []
        by_id = {service.id: service for service in services}
        return jsonify({
            "saved_services": [by_id[row.service_id].to_dict() for row in rows if row.service_id in by_id],
            "count": len(rows),
        })

    data = request.get_json() or {}
    try:
        service_id = int(data.get("service_id"))
    except (TypeError, ValueError):
        return jsonify({"error": "service_id must be an integer"}), 400

    if not Service.query.get(service_id):
        return jsonify({"error": "Service not found"}), 404
    if SavedService.query.filter_by(user_id=user.id, service_id=service_id).first():
        return jsonify({"message": "Service already saved"}), 200

    row = SavedService(user_id=user.id, service_id=service_id)
    db.session.add(row)
    db.session.commit()
    return jsonify({"message": "Service saved", "service_id": service_id}), 201


@app.route("/api/saved-services/<int:service_id>", methods=["DELETE"])
@login_required
def api_saved_service_delete(service_id):
    user = get_current_user()
    row = SavedService.query.filter_by(user_id=user.id, service_id=service_id).first()
    if not row:
        return jsonify({"error": "Saved service not found"}), 404
    db.session.delete(row)
    db.session.commit()
    return jsonify({"message": "Service removed"})


@app.route("/api/health")
def api_health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "ok", "database": "ok"})
    except Exception:
        return jsonify({"status": "error", "database": "unavailable"}), 503


# ============================================================
# STUDY MATERIALS API
# ============================================================

@app.route("/api/study")
def api_study():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    subject = request.args.get("subject", "").strip()
    query = StudyMaterial.query
    if category:
        query = query.filter(StudyMaterial.category.ilike(f"%{category}%"))
    if subject:
        query = query.filter(StudyMaterial.subject.ilike(f"%{subject}%"))
    if q:
        query = query.filter(
            db.or_(
                StudyMaterial.subject.ilike(f"%{q}%"),
                StudyMaterial.unit_title.ilike(f"%{q}%"),
                StudyMaterial.topics.ilike(f"%{q}%"),
                StudyMaterial.subject_code.ilike(f"%{q}%"),
            )
        )
    items = query.order_by(StudyMaterial.category, StudyMaterial.subject, StudyMaterial.unit_number).all()
    return jsonify({"materials": [m.to_dict() for m in items], "count": len(items)})


@app.route("/api/study/<int:mid>")
def api_study_detail(mid):
    m = StudyMaterial.query.get_or_404(mid)
    return jsonify(m.to_dict())


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found"}), 404
    return render_template("404.html", user=get_current_user()), 404


@app.errorhandler(500)
def server_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Internal server error"}), 500
    return render_template("500.html", user=get_current_user()), 500


# ============================================================
# INIT + SEED
# ============================================================

def init_db():
    db.create_all()
    from database.seed import seed_all, seed_study_materials
    if Service.query.count() == 0:
        seed_all(db)
    # Always ensure study materials exist (real syllabus content)
    if StudyMaterial.query.count() == 0:
        seed_study_materials(db)


@app.cli.command("init-db")
def init_db_command():
    """Initialize database and seed demo data."""
    init_db()
    print("Database initialized and seeded.")


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)