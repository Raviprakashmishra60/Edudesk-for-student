"""
EDUDESK database models (Flask-SQLAlchemy).

Every table is a Python class.  Lists (documents, steps, courses ...) are stored in
JSON columns, which work on SQLite today and on PostgreSQL later without changes.
"""
from datetime import date, datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

# ---- Shared constants (used by validation, filters and the UI) ----
SERVICE_CATEGORIES = [
    "Scholarships", "College Admissions", "Entrance Exams", "Competitive Exams",
    "Government Education Schemes", "Certificates", "Document Services",
    "Internships", "Career Guidance", "Courses", "Education Loans", "Counselling",
]
EXAM_CATEGORIES = ["Engineering", "Medical", "University Entrance", "Government Exams", "Competitive Exams"]
APPLICATION_STATUSES = ["Not Started", "Documents Ready", "Applied", "Under Review", "Approved", "Rejected"]
DEMO_NOTE = "Demo data — verify on the official website."


def utcnow():
    """Current UTC time without timezone info (simple for SQLite)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Serializable:
    """Adds .to_dict() so every model can be returned as JSON."""
    hidden_fields = ()

    def to_dict(self):
        data = {}
        for column in self.__table__.columns:
            if column.name in self.hidden_fields:
                continue
            value = getattr(self, column.name)
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            data[column.name] = value
        return data


class User(db.Model, Serializable):
    __tablename__ = "users"
    hidden_fields = ("password_hash",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # never store plain text

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def public_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "is_admin": self.is_admin}


class Service(db.Model, Serializable):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(60), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.Text, default="")
    documents = db.Column(db.JSON, default=list)
    steps = db.Column(db.JSON, default=list)
    important_dates = db.Column(db.String(255), default="Varies every year — verify on the official website.")
    official_url = db.Column(db.String(255))
    assistance_note = db.Column(db.String(255), default="")
    is_demo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class Scholarship(db.Model, Serializable):
    __tablename__ = "scholarships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    provider = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(20), nullable=False, index=True)          # Government / Private
    description = db.Column(db.Text, default="")
    eligibility = db.Column(db.Text, default="")
    benefit = db.Column(db.String(150), default="Varies — check the official notification")
    last_date = db.Column(db.String(80), default="Check official notification")
    documents = db.Column(db.JSON, default=list)
    official_url = db.Column(db.String(255))
    # Structured (demo) criteria used by the filters and "Check Eligibility"
    courses = db.Column(db.JSON, default=list)       # e.g. ["B.Tech", "B.Sc"] or ["Any"]
    levels = db.Column(db.JSON, default=list)        # e.g. ["12th", "Undergraduate"]
    states = db.Column(db.JSON, default=list)        # ["All India"] or state names
    categories = db.Column(db.JSON, default=list)    # ["All"] or ["SC", "ST", ...]
    max_income = db.Column(db.Integer)               # yearly family income limit (None = no limit)
    min_marks = db.Column(db.Integer)                # minimum % marks (None = no limit)
    is_demo = db.Column(db.Boolean, default=True, nullable=False)


class College(db.Model, Serializable):
    __tablename__ = "colleges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(80), nullable=False, index=True)
    state = db.Column(db.String(80), nullable=False, index=True)
    type = db.Column(db.String(30), nullable=False)                      # Government / Private / Deemed
    description = db.Column(db.Text, default="")
    courses = db.Column(db.JSON, default=list)
    entrance_exams = db.Column(db.JSON, default=list)
    fee_band = db.Column(db.String(20), default="Medium")                # Low / Medium / High (indicative)
    eligibility = db.Column(db.Text, default="")
    admission_process = db.Column(db.Text, default="")
    official_url = db.Column(db.String(255))
    is_demo = db.Column(db.Boolean, default=True, nullable=False)


class Exam(db.Model, Serializable):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(60), nullable=False, index=True)
    description = db.Column(db.Text, default="")
    eligibility = db.Column(db.Text, default="")
    registration_process = db.Column(db.Text, default="")
    documents = db.Column(db.JSON, default=list)
    important_dates = db.Column(db.String(255), default="Check the official notification for current dates.")
    official_url = db.Column(db.String(255))
    is_demo = db.Column(db.Boolean, default=True, nullable=False)


class Deadline(db.Model, Serializable):
    __tablename__ = "deadlines"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.Text, default="")
    official_url = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False, nullable=False)   # True only if checked against an official source
    source_label = db.Column(db.String(120), default="Demo data — not a real deadline")


class Application(db.Model, Serializable):
    """One application a student is tracking. Belongs to a user OR to a guest session."""
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    guest_id = db.Column(db.String(40), index=True)
    student_name = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(30), default="Not Started", nullable=False)
    notes = db.Column(db.String(500), default="")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)
    history = db.relationship("ApplicationHistory", backref="application", cascade="all, delete-orphan",
                              order_by="ApplicationHistory.id")


class ApplicationHistory(db.Model, Serializable):
    __tablename__ = "application_history"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False)
    note = db.Column(db.String(200), default="")
    changed_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class SavedService(db.Model, Serializable):
    __tablename__ = "saved_services"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    guest_id = db.Column(db.String(40), index=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    service = db.relationship("Service")


class Question(db.Model, Serializable):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    guest_id = db.Column(db.String(40), index=True)
    text = db.Column(db.String(500), nullable=False)
    answer_summary = db.Column(db.String(300), default="")
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class AktuSubject(db.Model, Serializable):
    """One AKTU B.Tech first-year subject (study hub)."""
    __tablename__ = "aktu_subjects"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)   # e.g. BAS101 (Semester 1 code)
    alt_code = db.Column(db.String(20), index=True)                            # e.g. BAS201 (same subject in Semester 2)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(40), nullable=False, index=True)            # Basic Science / Engineering Science / ...
    credits = db.Column(db.Integer, default=3)
    ltp = db.Column(db.String(12), default="")                                 # lecture-tutorial-practical periods
    objective = db.Column(db.Text, default="")
    syllabus_note = db.Column(db.Text, default="")                             # honest note about how the unit list was prepared
    books = db.Column(db.JSON, default=list)
    labs = db.Column(db.JSON, default=list)                                    # [{"code", "title", "items": [...]}]
    sort_order = db.Column(db.Integer, default=0)
    units = db.relationship("AktuUnit", backref="subject", cascade="all, delete-orphan", order_by="AktuUnit.number")


class AktuUnit(db.Model, Serializable):
    __tablename__ = "aktu_units"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("aktu_subjects.id"), nullable=False, index=True)
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    hours = db.Column(db.Integer, default=8)
    syllabus = db.Column(db.Text, default="")          # topics as listed in the official syllabus
    notes = db.Column(db.JSON, default=list)           # [{"heading": str, "points": [str]}]
    questions = db.Column(db.JSON, default=list)       # [{"kind": short|long|numerical, "text": str, "hint": str}]


class AktuPaper(db.Model, Serializable):
    """A previous-year question paper (stored as a link, not a file)."""
    __tablename__ = "aktu_papers"
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), nullable=False, index=True)       # BAS101 or BAS201 etc.
    title = db.Column(db.String(150), nullable=False)                         # e.g. "Engineering Physics 2023-24 Theory Exam"
    exam_session = db.Column(db.String(30), default="")                       # e.g. 2023-24
    paper_type = db.Column(db.String(30), default="Theory")                   # Theory / Sessional / Back paper
    official_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)


class AktuProgress(db.Model, Serializable):
    """One AKTU unit a student marked as done. Belongs to a user OR to a guest session."""
    __tablename__ = "aktu_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    guest_id = db.Column(db.String(40), index=True)
    subject_code = db.Column(db.String(20), nullable=False, index=True)
    unit_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
