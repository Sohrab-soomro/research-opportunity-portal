# Quick start (Windows / VS Code)

1. Open the `research-opportunity-portal` folder in VS Code.
2. In its terminal: `python -m venv .venv` then `.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt`.
3. Copy `backend/.env.example` to `backend/.env` if absent; configure your local MySQL account.
4. In MySQL Workbench, run `database/schema.sql`; optionally run `database/seed.sql` once.
5. Terminal → Run Task → Start Flask. Open http://localhost:5000 or run Open frontend.
6. Run Test API (mock) for logic; run Test API (MySQL) for real integration in a disposable database.

Current audit machine: MySQL unavailable. Finish real integration before recording or submission. Full instructions and troubleshooting: [README](../README.md).
