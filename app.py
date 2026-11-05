"""
EDUDESK - "Everything Students Need. In One Desk."

Run:  python app.py      ->  http://127.0.0.1:5001
This file creates the Flask app, serves the HTML pages and connects the API blueprints.
"""
import os
import secrets
from datetime import timedelta
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

try:                                    # .env support (optional but recommended)
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from admin import admin_bp
from api import api
from models import (APPLICATION_STATUSES, EXAM_CATEGORIES, SERVICE_CATEGORIES, AktuSubject, Service, User, db)
from utils import ApiError, current_user

BASE_DIR = Path(__file__).resolve().parent


def load_secret_key():
    """Use SECRET_KEY from .env; otherwise create one once and keep it in a git-ignored file."""
    key = os.getenv("SECRET_KEY", "").strip()
    if key and key != "change-me":
        return key
    key_file = BASE_DIR / ".secret_key"
    if not key_file.exists():
        key_file.write_text(secrets.token_hex(32))
    return key_file.read_text().strip()


def database_uri():
    """SQLite by default. Set DATABASE_URL in .env to switch to PostgreSQL later."""
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        return "sqlite:///" + str(BASE_DIR / "edudesk.db")
    return url.replace("postgres://", "postgresql://", 1)


def init_database(app):
    """Create tables and load the demo data the first time the app runs."""
    with app.app_context():
        db.create_all()
        from database.seed import seed_aktu, seed_all
        if Service.query.count() == 0:
            seed_all()                       # also loads the AKTU study content
        elif AktuSubject.query.count() == 0:
            seed_aktu()                      # older databases get the AKTU content added automatically


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=load_secret_key(),
        SQLALCHEMY_DATABASE_URI=database_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "0") == "1",
        PERMANENT_SESSION_LIFETIME=timedelta(days=14),
        MAX_CONTENT_LENGTH=1024 * 1024,          # API bodies are tiny; documents never reach the server
    )
    db.init_app(app)
    app.register_blueprint(api)
    app.register_blueprint(admin_bp)
    register_pages(app)
    register_hooks(app)
    register_error_handlers(app)
    register_cli(app)
    init_database(app)
    return app


# ------------------------------------------------------------------ pages
def register_pages(app):
    @app.context_processor
    def inject_globals():
        return {
            "user": current_user(),
            "whatsapp_number": os.getenv("WHATSAPP_NUMBER", "918604551960"),
            "service_categories": SERVICE_CATEGORIES,
            "exam_categories": EXAM_CATEGORIES,
            "statuses": APPLICATION_STATUSES,
        }

    @app.get("/")
    def home():
        return render_template("index.html", active="home")

    @app.get("/services")
    def services_page():
        return render_template("services.html", active="services")

    @app.get("/scholarships")
    def scholarships_page():
        return render_template("scholarships.html", active="scholarships")

    @app.get("/colleges")
    def colleges_page():
        return render_template("colleges.html", active="colleges")

    @app.get("/exams")
    def exams_page():
        return render_template("exams.html", active="exams")

    @app.get("/aktu")
    def aktu_page():
        return render_template("aktu.html", active="aktu")

    @app.get("/aktu/<code>")
    def aktu_subject_page(code):
        from api import find_aktu_subject
        subject = find_aktu_subject(code)
        if not subject:
            return render_template("404.html", active="aktu"), 404
        return render_template("aktu_subject.html", active="aktu", subject_code=subject.code, subject_name=subject.name)

    @app.get("/ask")
    def ask_page():
        return render_template("ask.html", active="ask")

    @app.get("/documents")
    def documents_page():
        return render_template("documents.html", active="documents")

    @app.get("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html", active="dashboard")

    @app.get("/login")
    def login_page():
        next_url = request.args.get("next", "/dashboard")
        if not next_url.startswith("/") or next_url.startswith("//"):   # block open redirects
            next_url = "/dashboard"
        if current_user():
            return redirect(next_url)
        return render_template("login.html", active="login", next_url=next_url,
                               start_tab="register" if request.args.get("tab") == "register" else "login")

    @app.get("/logout")
    def logout_page():
        session.clear()
        return redirect(url_for("home"))

    @app.get("/admin")
    def admin_page():
        """Admin panel (HTML). Only admins can open it; the data comes from /api/admin/..."""
        user = current_user()
        if not user:
            return redirect(url_for("login_page", next="/admin"))
        if not user.is_admin:
            return render_template("404.html", active=""), 404
        return render_template("admin.html")


# ------------------------------------------------------------------ security hooks
def register_hooks(app):
    @app.before_request
    def require_ajax_header_for_writes():
        """Browsers cannot add this custom header from another website, which blocks CSRF."""
        if request.path.startswith("/api/") and request.method in ("POST", "PATCH", "PUT", "DELETE"):
            if request.headers.get("X-Requested-With") != "EDUDESK":
                raise ApiError("Missing request header.", 403)

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'")
        if request.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response


# ------------------------------------------------------------------ error handling
def register_error_handlers(app):
    def wants_json():
        return request.path.startswith("/api/")

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return jsonify({"error": error.message, "details": error.details}), error.status

    @app.errorhandler(404)
    def not_found(_error):
        if wants_json():
            return jsonify({"error": "Not found."}), 404
        return render_template("404.html", active=""), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        if wants_json():
            return jsonify({"error": "Method not allowed."}), 405
        return render_template("404.html", active=""), 405

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify({"error": "Request too large."}), 413

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()
        if wants_json():
            return jsonify({"error": "Something went wrong on our side. Please try again."}), 500
        return render_template("500.html"), 500          # standalone page (does not touch the database)


# ------------------------------------------------------------------ command line tools
def register_cli(app):
    @app.cli.command("make-admin")
    def make_admin():
        """Usage: flask --app app make-admin  (asks for the email of an existing account)."""
        email = input("Email of the account to make admin: ").strip().lower()
        user = User.query.filter_by(email=email).first()
        if not user:
            print("No account with that email. Register on the website first.")
            return
        user.is_admin = True
        db.session.commit()
        print(f"{user.email} is now an admin.")


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", port=int(os.getenv("PORT", "5000")))
