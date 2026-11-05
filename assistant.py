"""
Ask EDUDESK - the education assistant.

Version 1 is RULE-BASED (no external AI needed):
  1. General guidance  -> hand-written answers in KNOWLEDGE_BASE below
  2. EDUDESK database  -> matching services / scholarships / colleges / exams
  3. Official source   -> official links + a reminder to verify current rules

HOW TO PLUG IN AN AI API LATER
  * Write a class that extends AssistantProvider and implements answer(question, context).
    'context' already contains the matched knowledge-base entry and database records,
    so an AI model can be given those as grounding material.
  * Register it in PROVIDERS and set ASSISTANT_PROVIDER=<name> in .env.
  * Keep the API key in .env (e.g. AI_API_KEY) - never in the code.
"""
import os

from models import AktuSubject, College, Exam, Scholarship, Service
from utils import normalize_text, rank, word_match

DISCLAIMER = ("EDUDESK gives general guidance and demo data. Deadlines, fees, eligibility and rules change "
              "every year - always confirm on the official website or notification before you apply.")

OFFICIAL_TRIGGERS = ["deadline", "last date", "date", "dates", "fee", "fees", "cutoff", "cut off", "notification",
                     "rule", "rules", "eligibility", "eligible", "vacancy", "schedule", "result", "syllabus"]

# Each entry: 'must' = at least one of these words must be in the question,
#             'keywords' = extra words that make the match stronger,
#             'min_keywords' = how many extra words are needed.
KNOWLEDGE_BASE = [
    {
        "id": "greeting", "must": ["hello", "hi", "hey", "namaste"], "keywords": [], "min_keywords": 0,
        "answer": "Hello! I am EDUDESK, your education helper. Ask me about scholarships, admissions, entrance exams, documents or applications.",
        "points": [], "links": [{"label": "Browse services", "url": "/services"}],
    },
    {
        "id": "jee_form_docs", "must": ["jee"], "min_keywords": 1,
        "keywords": ["document", "documents", "form", "apply", "required", "registration", "papers"],
        "answer": "For a JEE application you usually need the items below. The exact list and file sizes are in the official Information Bulletin, so read it before you start.",
        "points": ["Class 10 certificate or marksheet (for name and date of birth)", "Class 12 / qualifying exam details",
                   "Recent passport-size photograph and your signature as image files (size rules are in the bulletin)",
                   "Valid photo ID such as Aadhaar", "Category / EWS / PwD certificate if you claim those benefits",
                   "Your own email ID and mobile number", "A way to pay the fee online"],
        "links": [{"label": "Prepare photo & signature", "url": "/documents"}, {"label": "See exams", "url": "/exams"}],
    },
    {
        "id": "docs_scholarship", "must": ["scholarship", "scholarships"], "min_keywords": 1,
        "keywords": ["document", "documents", "papers", "required", "need", "needed", "certificate"],
        "answer": "Documents differ by scheme, but most scholarship applications ask for a similar core set. Always follow the list on the scheme's official page.",
        "points": ["Aadhaar / photo ID", "Previous year marksheet", "Income certificate (for income-based schemes)",
                   "Caste / category certificate (for category-based schemes)", "Domicile / residence certificate (for state schemes)",
                   "Bank passbook of the student account (Aadhaar-linked if the scheme asks)", "Admission proof, bonafide certificate or fee receipt",
                   "Passport-size photograph"],
        "links": [{"label": "Open Scholarship Finder", "url": "/scholarships"}],
    },
    {
        "id": "btech_admission", "must": ["btech", "engineering"], "min_keywords": 1,
        "keywords": ["admission", "apply", "join", "how", "jee", "college", "process", "get"],
        "answer": "A typical path to B.Tech admission in India looks like this. Confirm every step on the official websites for the current year.",
        "points": ["Check the eligibility for the colleges you want (qualifying exam, subjects, minimum marks)",
                   "Find the entrance exam they accept - for example JEE Main, or a state / university exam",
                   "Register for the exam on its official portal and prepare your documents early",
                   "After results, join the counselling process (central counselling for IITs/NITs/IIITs, state counselling for state colleges)",
                   "Fill your college and branch choices, then complete document verification and fee payment",
                   "Many private universities run their own admission process too - check their official website"],
        "links": [{"label": "Find colleges", "url": "/colleges"}, {"label": "Browse exams", "url": "/exams"}],
    },
    {
        "id": "cse_vs_it", "must": ["cse", "it", "computer science", "information technology"], "min_keywords": 1,
        "keywords": ["difference", "vs", "versus", "compare", "between", "better", "which"],
        "answer": "CSE and IT overlap a lot. In short: CSE leans towards the core of computing, IT leans towards applying computing in real systems.",
        "points": ["CSE: algorithms, operating systems, computer architecture, compilers, theory, programming depth",
                   "IT: networks, databases, web and cloud systems, information security, IT services",
                   "Many colleges teach almost the same first-year subjects for both",
                   "Software jobs are open to both - the college quality, projects and skills matter more than the branch name",
                   "Compare the syllabus and labs of the exact college before choosing"],
        "links": [{"label": "Find colleges", "url": "/colleges"}],
    },
    {
        "id": "after_12th", "must": ["12th", "twelfth", "intermediate", "class 12"], "min_keywords": 1,
        "keywords": ["after", "next", "career", "options", "do", "should", "course", "courses"],
        "answer": "What you can do after 12th depends on your stream and interests. Here are common directions:",
        "points": ["Science (PCM): B.Tech / B.E., B.Sc, BCA, B.Arch, defence entry exams such as NDA",
                   "Science (PCB): MBBS / BDS via NEET, B.Sc Nursing, Pharmacy, Biotechnology",
                   "Commerce: B.Com, BBA, Economics, CA / CS / CMA foundation courses",
                   "Arts / Humanities: BA, Law (CLAT and others), Journalism, Design, Social Sciences",
                   "Any stream: central university admission via CUET, diplomas, skill courses, government exam preparation alongside a degree",
                   "Steps: list your interests, check entrance exams, compare colleges, check scholarships, then talk to a counsellor"],
        "links": [{"label": "Browse exams", "url": "/exams"}, {"label": "Career guidance services", "url": "/services?category=Career%20Guidance"}],
    },
    {
        "id": "exam_form_docs", "must": ["form", "application", "registration"], "min_keywords": 1,
        "keywords": ["document", "documents", "required", "exam", "neet", "cuet", "ssc", "upsc", "papers"],
        "answer": "Most exam application forms ask for the same basics. Check the official notification for exact sizes and formats.",
        "points": ["Scanned photograph and signature in the size and format given in the notification", "Photo ID (Aadhaar or other accepted ID)",
                   "Class 10 / 12 marksheets or certificates", "Category / PwD / EWS certificate if applicable",
                   "Active email ID and mobile number", "Online fee payment option"],
        "links": [{"label": "Prepare photo & signature", "url": "/documents"}, {"label": "See exams", "url": "/exams"}],
    },
    {
        "id": "certificates", "must": ["certificate", "certificates", "domicile", "income certificate", "caste certificate"], "min_keywords": 0,
        "keywords": ["apply", "how", "get", "make"],
        "answer": "Income, caste and domicile certificates are issued by your state government. Most states have an online e-District portal, and you can also apply through a local government office or Common Service Centre.",
        "points": ["Search for your state's e-District / service portal and read the document list there",
                   "Usually needed: Aadhaar, address proof, a self-declaration or affidavit, and supporting papers",
                   "Processing time and validity differ by state - apply well before the scholarship or admission deadline"],
        "links": [{"label": "Certificate services", "url": "/services?category=Certificates"}],
    },
    {
        "id": "loan", "must": ["loan", "loans"], "min_keywords": 0, "keywords": ["education", "study", "apply", "how"],
        "answer": "Education loans are given by banks. The Vidya Lakshmi portal is a common starting point to look at schemes and apply to several banks.",
        "points": ["Keep your admission letter and fee structure ready", "KYC documents and marksheets of the student",
                   "Income proof of the parent / co-applicant", "Compare interest rate, repayment start date and collateral rules across banks",
                   "Check official government interest-subsidy schemes you may qualify for"],
        "links": [{"label": "Education loan services", "url": "/services?category=Education%20Loans"}],
    },
    {
        "id": "track", "must": ["track", "tracker", "tracking", "status"], "min_keywords": 0, "keywords": ["application", "applications"],
        "answer": "Use the EDUDESK Dashboard to track every application from Not Started to Approved or Rejected. You can add, update and delete applications, and each one keeps a status history. You can use it as a guest or create a free account.",
        "points": [], "links": [{"label": "Open Dashboard", "url": "/dashboard"}],
    },
    {
        "id": "photo_signature", "must": ["photo", "signature", "resize", "compress", "pdf"], "min_keywords": 0,
        "keywords": ["size", "kb", "upload", "reduce", "merge"],
        "answer": "The Document Center can resize and compress images, convert images to PDF, and merge, split or shrink PDFs inside your browser. Your files are not uploaded to our server. Always match the exact size shown in the form's notification.",
        "points": [], "links": [{"label": "Open Document Center", "url": "/documents"}],
    },
    {
        "id": "eligibility", "must": ["eligible", "eligibility", "qualify"], "min_keywords": 0, "keywords": ["scholarship", "exam", "college"],
        "answer": "Eligibility usually depends on qualification, marks, age, category, family income and state. The official notification is the final authority.",
        "points": ["Use 'Check Eligibility' on a scholarship card to compare your details with its demo criteria",
                   "Read the eligibility section of the official notification before paying any fee"],
        "links": [{"label": "Scholarship Finder", "url": "/scholarships"}],
    },
    {
        "id": "aktu_syllabus", "must": ["aktu", "syllabus", "subjects"], "min_keywords": 0,
        "keywords": ["first", "year", "btech", "notes", "questions", "unit", "chapter", "semester", "physics", "chemistry", "maths", "mathematics"],
        "answer": "The AKTU Study Hub has the official first-year (common to all branches) syllabus with unit-wise summary notes and important practice questions for every subject. Always cross-check with the latest syllabus on the AKTU website.",
        "points": [], "links": [{"label": "Open AKTU Study Hub", "url": "/aktu"}],
    },
    {
        "id": "internship", "must": ["internship", "internships"], "min_keywords": 0, "keywords": ["how", "find", "apply"],
        "answer": "To find an internship: build a short resume, check official internship portals and company career pages, and apply early. Never pay money to get an internship offer.",
        "points": [], "links": [{"label": "Internship services", "url": "/services?category=Internships"}],
    },
]


def _hit(question, keyword):
    return word_match(question, normalize_text(keyword))


def best_knowledge_entry(question):
    """Pick the knowledge-base entry that matches the question best (first one wins ties)."""
    best, best_score = None, 0
    for entry in KNOWLEDGE_BASE:
        if not any(_hit(question, word) for word in entry["must"]):
            continue
        extra = sum(1 for word in entry["keywords"] if _hit(question, word))
        if extra < entry.get("min_keywords", 0):
            continue
        score = 1 + extra
        if score > best_score:
            best, best_score = entry, score
    return best


def search_database(question, limit=5):
    """Find records in the EDUDESK database that match the question."""
    found = []
    sources = [
        ("Service", "/services", Service.query.all(),
         lambda r: f"{r.title} {r.category} {r.description} {r.eligibility}",
         lambda r: (r.title, r.category)),
        ("Scholarship", "/scholarships", Scholarship.query.all(),
         lambda r: f"{r.name} {r.provider} {r.type} {r.description} {r.eligibility} {' '.join(r.courses or [])}",
         lambda r: (r.name, f"{r.provider} - {r.type}")),
        ("College", "/colleges", College.query.all(),
         lambda r: f"{r.name} {r.city} {r.state} {r.type} {' '.join(r.courses or [])} {' '.join(r.entrance_exams or [])}",
         lambda r: (r.name, f"{r.city}, {r.state}")),
        ("AKTU Subject", "/aktu", AktuSubject.query.all(),
         lambda r: f"{r.code} {r.alt_code or ''} {r.name} " + " ".join(f"{u.title} {u.syllabus}" for u in r.units),
         lambda r: (r.name, f"{r.code} - first year")),
        ("Exam", "/exams", Exam.query.all(),
         lambda r: f"{r.name} {r.category} {r.description} {r.eligibility}",
         lambda r: (r.name, r.category)),
    ]
    for kind, page, records, text_of, label_of in sources:
        results, exact = rank(records, question, text_of)
        if not exact:
            continue                       # in the assistant we only trust full matches
        for record in results[:2]:
            title, subtitle = label_of(record)
            url = f"/aktu/{record.code}" if kind == "AKTU Subject" else f"{page}?open={record.id}"
            found.append({"type": kind, "id": record.id, "title": title, "summary": subtitle,
                          "url": url, "official_url": getattr(record, "official_url", None)})
    return found[:limit]


class AssistantProvider:
    """Base class. Extend it to connect an AI model (see the note at the top of this file)."""
    name = "base"

    def answer(self, question, context):
        raise NotImplementedError


class RuleBasedProvider(AssistantProvider):
    name = "rules"

    def answer(self, question, context):
        sections = []
        entry, items = context["entry"], context["items"]

        if entry:
            sections.append({"label": "General guidance", "kind": "general", "text": entry["answer"],
                             "points": entry["points"], "links": entry["links"]})

        if items:
            sections.append({"label": "From EDUDESK database", "kind": "database",
                             "text": "These records in EDUDESK match your question (demo data - verify on the official website):",
                             "items": [{k: v for k, v in item.items() if k != "official_url"} for item in items]})

        official_links = [{"label": f"Official site - {item['title']}", "url": item["official_url"]}
                          for item in items if item.get("official_url")]
        asks_current_info = any(_hit(context["normalized"], word) for word in OFFICIAL_TRIGGERS)
        if official_links or asks_current_info:
            text = ("Deadlines, fees and rules change often. Please verify the latest details in the official notification "
                    "before you apply.")
            sections.append({"label": "Official source", "kind": "official", "text": text, "links": official_links[:4]})

        if not sections:
            sections.append({"label": "General guidance", "kind": "general",
                             "text": "I could not find an exact answer yet. Try asking about scholarships, admissions, entrance exams, "
                                     "documents or career options - or browse the directories below.",
                             "points": ["Example: What documents are required for scholarship?", "Example: How can I apply for BTech admission?",
                                        "Example: What should I do after 12th?"],
                             "links": [{"label": "Services", "url": "/services"}, {"label": "Scholarships", "url": "/scholarships"},
                                       {"label": "Exams", "url": "/exams"}]})
        return {"sections": sections, "disclaimer": DISCLAIMER, "provider": self.name}


PROVIDERS = {"rules": RuleBasedProvider}


def get_provider():
    return PROVIDERS.get(os.getenv("ASSISTANT_PROVIDER", "rules"), RuleBasedProvider)()


def answer_question(question):
    normalized = normalize_text(question)
    context = {"normalized": normalized, "entry": best_knowledge_entry(normalized), "items": search_database(question)}
    return get_provider().answer(question, context)
