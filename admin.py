"""
Admin API - for a future admin panel. Every route requires a logged-in user with is_admin = True.

Make someone an admin (run once, in the project folder):
    flask --app app make-admin      (it asks for the account email)
"""
from datetime import date

from flask import Blueprint, jsonify

from models import (APPLICATION_STATUSES, EXAM_CATEGORIES, SERVICE_CATEGORIES, AktuPaper, Application, College, Deadline, Exam,
                    Scholarship, Service, db)
from utils import ApiError, admin_required, get_json_body

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

# resource name -> (model, text fields, list fields, required fields)
RESOURCES = {
    "services": (Service, ["title", "category", "description", "eligibility", "important_dates", "official_url", "assistance_note"],
                 ["documents", "steps"], ["title", "category", "description"]),
    "scholarships": (Scholarship, ["name", "provider", "type", "description", "eligibility", "benefit", "last_date", "official_url"],
                     ["documents", "courses", "levels", "states", "categories"], ["name", "provider", "type"]),
    "colleges": (College, ["name", "city", "state", "type", "description", "fee_band", "eligibility", "admission_process", "official_url"],
                 ["courses", "entrance_exams"], ["name", "city", "state", "type"]),
    "exams": (Exam, ["name", "category", "description", "eligibility", "registration_process", "important_dates", "official_url"],
              ["documents"], ["name", "category"]),
    "papers": (AktuPaper, ["subject_code", "title", "exam_session", "paper_type", "official_url"], [],
               ["subject_code", "title", "official_url"]),
    "deadlines": (Deadline, ["title", "category", "description", "official_url", "source_label"], [], ["title", "category"]),
}


def _resource(name):
    if name not in RESOURCES:
        raise ApiError("Unknown resource.", 404)
    return RESOURCES[name]


def _apply(record, data, text_fields, list_fields, required, creating):
    for field in text_fields:
        if field in data:
            value = data[field]
            if not isinstance(value, str) or len(value) > 5000:
                raise ApiError(f"{field} must be text (max 5000 characters).", 400)
            if field == "official_url" and value.strip() and not value.strip().lower().startswith(("http://", "https://")):
                raise ApiError("official_url must start with http:// or https://", 400)
            setattr(record, field, value.strip())
    for field in list_fields:
        if field in data:
            value = data[field]
            if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                raise ApiError(f"{field} must be a list of text values.", 400)
            setattr(record, field, [v.strip() for v in value if v.strip()])
    if isinstance(record, Deadline):
        if "date" in data:
            try:
                record.date = date.fromisoformat(data["date"])
            except (TypeError, ValueError):
                raise ApiError("date must look like YYYY-MM-DD.", 400)
        if "is_verified" in data:
            record.is_verified = bool(data["is_verified"])
        if creating and not record.date:
            raise ApiError("date is required.", 400)
    if "is_demo" in data and hasattr(record, "is_demo"):
        record.is_demo = bool(data["is_demo"])
    for field in required:
        if not getattr(record, field, None):
            raise ApiError(f"{field} is required.", 400)


@admin_bp.post("/<resource>")
@admin_required
def create_record(resource):
    model, text_fields, list_fields, required = _resource(resource)
    record = model()
    _apply(record, get_json_body(), text_fields, list_fields, required, creating=True)
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@admin_bp.patch("/<resource>/<int:record_id>")
@admin_required
def update_record(resource, record_id):
    model, text_fields, list_fields, required = _resource(resource)
    record = db.session.get(model, record_id)
    if not record:
        raise ApiError("Record not found.", 404)
    _apply(record, get_json_body(), text_fields, list_fields, required, creating=False)
    db.session.commit()
    return jsonify(record.to_dict())


@admin_bp.delete("/<resource>/<int:record_id>")
@admin_required
def delete_record(resource, record_id):
    model = _resource(resource)[0]
    record = db.session.get(model, record_id)
    if not record:
        raise ApiError("Record not found.", 404)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"ok": True})


@admin_bp.get("/<resource>")
@admin_required
def list_records(resource):
    """All records of one resource (newest first) for the admin panel."""
    model = _resource(resource)[0]
    rows = model.query.order_by(model.id.desc()).limit(500).all()
    return jsonify({"items": [row.to_dict() for row in rows], "count": len(rows)})


@admin_bp.get("/applications")
@admin_required
def all_applications():
    """Admins can view every student's applications (read-only)."""
    rows = Application.query.order_by(Application.updated_at.desc()).limit(500).all()
    return jsonify({"items": [a.to_dict() for a in rows], "count": len(rows)})
