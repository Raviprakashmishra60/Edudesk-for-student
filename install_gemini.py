#!/usr/bin/env python3
from pathlib import Path
import getpass, os, re, sys

ROOT = Path(__file__).resolve().parent
assistant = ROOT / "assistant.py"
if not assistant.exists():
    sys.exit("ERROR: Copy this installer beside app.py and assistant.py in your EDUDESK folder.")

source = assistant.read_text(encoding="utf-8")
if "class AssistantProvider:" not in source:
    sys.exit("ERROR: AssistantProvider class not found. No files changed.")

if "class GeminiProvider(AssistantProvider):" not in source:
    if "from dotenv import load_dotenv" not in source:
        source = source.replace("import os", "import os\nimport json\nfrom dotenv import load_dotenv\n\nload_dotenv()", 1)

    gemini_class = """


class GeminiProvider(AssistantProvider):
    name = "gemini"

    def answer(self, question, context):
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")

        data = {
            "knowledge_base": context.get("entry"),
            "database_matches": context.get("items", [])
        }
        context_text = json.dumps(data, ensure_ascii=False, default=str)

        instructions = (
            "You are EDUDESK AI, an educational assistant for Indian students. "
            "Help with scholarships, admissions, colleges, exams, documents, AKTU, "
            "B.Tech, internships and careers. Explain in simple English, Hindi or Hinglish. "
            "Give practical step-by-step answers. Use supplied EDUDESK context when relevant. "
            "Never invent deadlines, fees, eligibility or official rules. If information is "
            "missing, say so. Tell students to verify changing information on official websites. "
            "Do not claim demo data is officially verified."
        )
        prompt = (
            instructions + "\\n\\nEDUDESK CONTEXT:\\n" + context_text +
            "\\n\\nSTUDENT QUESTION:\\n" + question
        )

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model, contents=prompt)
        answer_text = (response.text or "").strip()
        if not answer_text:
            raise RuntimeError("Gemini returned an empty response.")

        return {
            "sections": [{
                "label": "EDUDESK AI Answer",
                "kind": "general",
                "text": answer_text
            }],
            "disclaimer": DISCLAIMER,
            "provider": self.name
        }

"""
    marker = re.search(r"(?m)^PROVIDERS\\s*=", source)
    if not marker:
        sys.exit("ERROR: PROVIDERS registry not found. No files changed.")
    source = source[:marker.start()] + gemini_class + "\\n" + source[marker.start():]

source = re.sub(
    r"(?m)^PROVIDERS\\s*=\\s*\\{[^\\n]*\\}",
    'PROVIDERS = {"rules": RuleBasedProvider, "gemini": GeminiProvider}',
    source, count=1
)
if '"gemini": GeminiProvider' not in source:
    sys.exit("ERROR: Could not update provider registry.")

assistant.write_text(source, encoding="utf-8")
print("Updated assistant.py")

env_path = ROOT / ".env"
env = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
api_key = getpass.getpass("Paste Gemini API key (hidden input): ").strip()
settings = {
    "ASSISTANT_PROVIDER": "gemini",
    "GEMINI_API_KEY": api_key,
    "GEMINI_MODEL": "gemini-flash-latest"
}
for name, value in settings.items():
    if not value and name == "GEMINI_API_KEY":
        continue
    line = f"{name}={value}"
    pattern = rf"(?m)^{re.escape(name)}=.*$"
    env = re.sub(pattern, lambda _: line, env) if re.search(pattern, env) else env.rstrip() + ("\\n" if env.strip() else "") + line + "\\n"
env_path.write_text(env, encoding="utf-8")
try:
    env_path.chmod(0o600)
except OSError:
    pass

gitignore = ROOT / ".gitignore"
ignored = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
if ".env" not in ignored.splitlines():
    gitignore.write_text(ignored.rstrip() + ("\\n" if ignored.strip() else "") + ".env\\n", encoding="utf-8")

requirements = ROOT / "requirements.txt"
req = requirements.read_text(encoding="utf-8") if requirements.exists() else ""
for package in ("google-genai", "python-dotenv"):
    if not re.search(rf"(?im)^\\s*{re.escape(package)}(?:[<=>~!].*)?$", req):
        req = req.rstrip() + ("\\n" if req.strip() else "") + package + "\\n"
requirements.write_text(req, encoding="utf-8")

print("\\nSetup files updated. Next run:")
print("  python -m pip install -r requirements.txt")
print("  python -m py_compile assistant.py")
print("  flask --app app run --port 5001")
