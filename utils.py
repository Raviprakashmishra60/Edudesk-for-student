"""
Small shared helpers: errors, login checks, guest ownership, input validation, search ranking.
"""
import re
import uuid
from functools import wraps

from flask import request, session
from sqlalchemy import false

from models import AktuProgress, Application, Question, SavedService, User, db


# --------------------------------------------------------------------------
# Errors -> always returned to the frontend as JSON {"error": "..."}
# --------------------------------------------------------------------------
class ApiError(Exception):
    def __init__(self, message, status=400, details=None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.details = details


# --------------------------------------------------------------------------
# Login / guest handling
# --------------------------------------------------------------------------
def current_user():
    """Return the logged-in User or None."""
    user_id = session.get("user_id")
    return db.session.get(User, user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user():
            raise ApiError("Please log in to continue.", 401)
        return view(*args, **kwargs)
    return wrapper


def admin_required(view):
    """Protects admin APIs: must be logged in AND flagged is_admin."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            raise ApiError("Please log in to continue.", 401)
        if not user.is_admin:
            raise ApiError("Admin access required.", 403)
        return view(*args, **kwargs)
    return wrapper


def guest_id(create=False):
    """Guests get a random id stored in their session cookie so they can still use the tracker."""
    gid = session.get("guest_id")
    if not gid and create:
        gid = uuid.uuid4().hex
        session["guest_id"] = gid
    return gid


def owner_filter(model):
    """SQL condition that selects only rows owned by the current user (or current guest)."""
    user = current_user()
    if user:
        return model.user_id == user.id
    gid = guest_id()
    return model.guest_id == gid if gid else false()


def assign_owner(obj):
    user = current_user()
    if user:
        obj.user_id = user.id
    else:
        obj.guest_id = guest_id(create=True)


def claim_guest_data(user):
    """After login/register: move the guest's applications, saved services and questions to the account."""
    gid = session.get("guest_id")
    if not gid:
        return
    for model in (Application, SavedService, Question, AktuProgress):
        model.query.filter_by(guest_id=gid).update({"user_id": user.id, "guest_id": None})
    db.session.commit()


# --------------------------------------------------------------------------
# Input validation
# --------------------------------------------------------------------------
def get_json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError("Send a valid JSON body.", 400)
    return data


def clean_text(data, field, label, max_len=150, required=True, default=""):
    value = data.get(field, default)
    if value is None:
        value = default
    if not isinstance(value, str):
        raise ApiError(f"{label} must be text.", 400)
    value = value.strip()
    if required and not value:
        raise ApiError(f"{label} is required.", 400)
    if len(value) > max_len:
        raise ApiError(f"{label} must be at most {max_len} characters.", 400)
    return value


def clean_choice(data, field, label, choices, default=None):
    value = data.get(field, default)
    if value not in choices:
        raise ApiError(f"{label} must be one of: {', '.join(choices)}.", 400)
    return value


def to_int(value, label):
    """Convert optional query/body values to int. Empty -> None."""
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ApiError(f"{label} must be a number.", 400)


# --------------------------------------------------------------------------
# Search helpers (used by the services/colleges/exams APIs and the assistant)
# --------------------------------------------------------------------------
STOPWORDS = {
    "a", "an", "the", "is", "are", "to", "of", "for", "and", "or", "in", "on", "at", "me", "my", "i",
    "what", "which", "how", "can", "do", "does", "should", "need", "get", "find", "show", "about",
    "required", "require", "with", "from", "between", "difference", "please", "tell", "help",
}
_SHORT_FORMS = ("btech", "mtech", "bsc", "msc", "bcom", "mcom")


def normalize_text(text):
    """Lowercase, make 'B.Tech' / 'b tech' / 'BTech' all become 'btech', remove punctuation."""
    text = (text or "").lower()
    for form in _SHORT_FORMS:
        text = re.sub(rf"\b{form[0]}[\.\s]?{form[1:]}\b", form, text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(query, drop_stopwords=True):
    tokens = []
    for word in normalize_text(query).split():
        if drop_stopwords and word in STOPWORDS:
            continue
        if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]                       # scholarships -> scholarship
        tokens.append(word)
    return tokens


def word_match(blob, token):
    return re.search(rf"\b{re.escape(token)}", blob) is not None


def rank(records, query, text_of):
    """
    Search records by query words.
    Returns (results, exact).  exact=True when every word matched; otherwise the
    partial matches are returned (best first) so the UI can say "showing related results".
    """
    tokens = tokenize(query) or tokenize(query, drop_stopwords=False)
    if not tokens:
        return list(records), True
    scored = []
    for record in records:
        blob = normalize_text(text_of(record))
        hits = sum(1 for token in tokens if word_match(blob, token))
        if hits:
            scored.append((hits, record))
    exact = [record for hits, record in scored if hits == len(tokens)]
    if exact:
        return exact, True
    scored.sort(key=lambda pair: -pair[0])
    return [record for _, record in scored], False
