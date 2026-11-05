EDUDESK Gemini Quick Installer

1. Back up your EDUDESK folder.
2. Extract this ZIP.
3. Copy install_gemini.py into the same folder as app.py and assistant.py.
4. Open Terminal in that folder.
5. Activate your venv if applicable: source venv/bin/activate
6. Run: python install_gemini.py
7. Paste your Gemini API key when prompted (input is hidden).
8. Run:
   python -m pip install -r requirements.txt
   python -m py_compile assistant.py
   flask --app app run --port 5001
9. Open http://127.0.0.1:5001 and test Ask EDUDESK.

IMPORTANT: This is a small installer/patch, NOT the full EDUDESK project ZIP.
It preserves your existing app and patches assistant.py, .env, .gitignore,
and requirements.txt. It does not include your database, templates or static files.
Never commit .env or share your API key.
