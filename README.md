# EDUDESK — Everything Students Need. In One Desk.

**From doubt to application — everything in one desk.**

EDUDESK is a full-stack student education platform built with **HTML + CSS + JavaScript + Python Flask + SQLite**.

**Problem:** Students struggle to find education information, understand forms, prepare documents and track multiple applications.
**Solution:** EDUDESK brings services, scholarships, colleges, exams, deadlines, document tools, an education assistant and an application tracker into one platform.

> ⚠️ **Data rule:** all records are **demo data**. Official websites are real so students can verify, but amounts, dates, fees and eligibility are intentionally general. Every demo item is labelled *"Demo data — verify on the official website."* No real deadlines are claimed.

---

## 1. Features

| Area | What works |
|---|---|
| Home | Hero, problem/solution/USP, category grid, dashboard preview |
| Services | 18 demo services, search (e.g. "BTech scholarship"), 12 category filters, details modal, save ♡, track, WhatsApp help |
| Scholarship Finder | Filters: course, class, state, category, income, marks, Govt/Private. **Check Eligibility** compares your details with demo criteria |
| College Finder | 12 demo colleges; search + filters: course, state, city, type, entrance exam, fee band. View Details modal |
| Exam Center | 10 exams, 5 categories, eligibility, registration, documents, official links (no invented dates) |
| Ask EDUDESK | `POST /api/ask` rule-based assistant. Answers are labelled **General guidance**, **From EDUDESK database**, **Official source**. AI-ready provider design |
| Document Center | In-browser image resize/compress (target KB), image→PDF, PDF merge, PDF split, PDF compress, file-size checker, photo/signature guide. **Files never leave your device** |
| AKTU 1st Year Study Hub | `/aktu`: 10 common first-year subjects, unit-wise syllabus, revision notes, important questions (short / long / numerical), search and category filter. Syllabus follows the **AKTU 2022-23 scheme**; notes and questions are original study aids, not AKTU papers. AKTU has also announced a revised first-year scheme for session 2026-27, so confirm your batch's scheme on aktu.ac.in |
| Application Tracker | Add / edit / change status / delete / view history (Not Started → Documents Ready → Applied → Under Review → Approved/Rejected) |
| Dashboard | Welcome, stat cards, progress bars, quick actions, deadlines (reminders / upcoming / past), saved services, recent questions |
| Accounts | Register / login / logout with hashed passwords. **Login is optional** — guests can use the tracker and their data moves to their account when they sign up |
| WhatsApp | "Need Help?" buttons build a pre-filled `wa.me` message per service/scholarship/exam |
| Admin-ready | Protected admin API (`/api/admin/...`) for services, scholarships, colleges, exams, deadlines, and viewing applications |
| Errors | 404 / 500 pages, JSON API errors, form validation, empty/loading/error states |

## 2. Technology stack

- **Frontend:** HTML5, CSS3, vanilla JavaScript (no framework), mobile-first responsive design
- **Backend:** Python 3, Flask, Flask-SQLAlchemy
- **Database:** SQLite (`edudesk.db`), PostgreSQL-ready through `DATABASE_URL`
- **PDF tools:** [pdf-lib](https://pdf-lib.js.org/) loaded from cdnjs (only the Document Center's PDF tools need internet)

## 3. Folder structure

```
EDUDESK/
├── app.py                # Flask app: pages, security headers, error handlers, CLI
├── api.py                # REST API (/api/...)
├── admin.py              # Admin-only API (/api/admin/...)
├── models.py             # SQLAlchemy models (9 tables + application_history)
├── assistant.py          # Ask EDUDESK (rule-based, AI-ready)
├── utils.py              # validation, login helpers, guest ownership, search ranking
├── requirements.txt
├── .env.example          # copy to .env
├── .gitignore
├── edudesk.db            # created automatically on first run
├── database/
│   └── seed.py           # demo data (auto-loaded on first run)
├── templates/            # base.html + one file per page, 404.html, 500.html
└── static/
    ├── css/  style.css, dashboard.css, responsive.css
    ├── js/   app.js (shared), services.js, scholarship.js, colleges.js, exams.js,
    │         ask.js, auth.js, dashboard.js, documents.js
    └── images/ favicon.svg
```

## 4. Installation and running

**Mac / Linux**
```bash
cd EDUDESK
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # optional but recommended: set SECRET_KEY
python app.py
```

**Windows**
```bat
cd EDUDESK
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## 5. Database initialization

Nothing to do: on first start the app creates `edudesk.db`, all tables and loads the demo data.
Manual options:
```bash
python database/seed.py            # load demo data if the database is empty
python database/seed.py --reset    # DELETE everything and recreate demo data (also deletes users!)
python database/seed.py --aktu     # load AKTU study material (edit database/aktu_*.py first)
```

To use PostgreSQL later: `pip install psycopg2-binary`, then set `DATABASE_URL=postgresql://user:pass@host:5432/edudesk` in `.env`.

## 6. Secrets and security

- Passwords are hashed (Werkzeug). Plain passwords are never stored.
- `SECRET_KEY` comes from `.env`; if missing, a random key is created once in `.secret_key` (git-ignored).
- All SQL goes through SQLAlchemy (parameterised → no SQL injection). Inputs are validated on the server.
- Output is HTML-escaped in the frontend; a Content-Security-Policy and other security headers are sent.
- Write requests need an `X-Requested-With` header (CSRF protection); login attempts are rate-limited in memory.
- Uploaded documents never reach the server: the Document Center works entirely in the browser.
- Admin APIs require a logged-in user with `is_admin = True`.

Create an admin (after registering on the website):
```bash
flask --app app make-admin       # asks for the account email
```

## 7. API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/services?q=&category=` | list/search services |
| GET | `/api/services/<id>` | one service |
| GET | `/api/scholarships?course=&level=&state=&category=&income=&marks=&type=&q=` | filter scholarships |
| GET | `/api/scholarships/<id>` | one scholarship |
| POST | `/api/scholarships/<id>/check` | eligibility check (JSON profile) |
| GET | `/api/colleges?q=&course=&state=&city=&type=&exam=&fees=` | filter colleges |
| GET | `/api/colleges/<id>` | one college |
| GET | `/api/exams?q=&category=` | list exams |
| GET | `/api/exams/<id>` | one exam |
| GET | `/api/deadlines` | reminders / upcoming / past |
| POST | `/api/ask` | `{ "question": "..." }` → labelled answer sections |
| GET | `/api/questions/recent` | your recent questions |
| GET / POST | `/api/applications` | list / create |
| PATCH / DELETE | `/api/applications/<id>` | update / delete |
| GET | `/api/applications/<id>/history` | status history |
| GET / POST / DELETE | `/api/saved`, `/api/saved/<service_id>` | saved services |
| GET | `/api/aktu/subjects?q=&category=`, `/api/aktu/subjects/<code>` | AKTU study hub (list / one subject with units) |
| GET | `/api/dashboard`, `/api/meta`, `/api/me` | dashboard numbers, filter options, current user |
| POST | `/api/register`, `/api/login`, `/api/logout` | accounts |
| POST/PATCH/DELETE | `/api/admin/<services\|scholarships\|colleges\|exams\|deadlines>[/<id>]` | admin only |
| GET | `/api/admin/applications` | admin only |

Write requests must send the header `X-Requested-With: EDUDESK` and `Content-Type: application/json`.

## 8. How to add data

1. **Edit `database/seed.py`** (lists `SERVICES`, `SCHOLARSHIPS`, `COLLEGES`, `EXAMS`, `DEADLINES`), then run `python database/seed.py --reset`.
2. **Use the admin API** (log in as admin first), e.g. from the browser console on the site:
```js
await api("/api/admin/services", { method: "POST", body: {
  title: "My new service", category: "Scholarships", description: "…",
  documents: ["Aadhaar"], steps: ["Step one"], official_url: "https://example.gov.in" } });
```
Only mark a deadline `is_verified: true` after checking it on the official source.

## 9. Connect an AI model later

Open `assistant.py`: write a class that extends `AssistantProvider`, implement `answer(question, context)` (the context already contains matched knowledge-base text and database records), add it to `PROVIDERS`, set `ASSISTANT_PROVIDER=yourname` and keep the API key in `.env`.

## 10. Future improvements

- Admin web panel using the existing admin API
- Email/SMS deadline reminders; calendar export
- Email verification and password reset
- Server-side pagination and full-text search (PostgreSQL)
- AI answers grounded on the database + official documents (RAG)
- Hindi and regional-language interface
- Verified data import pipeline with source links and "last verified" dates
- OCR-based document checker; secure optional document vault
- Automated tests (pytest) and Docker deployment
# Edudesk-for-student
