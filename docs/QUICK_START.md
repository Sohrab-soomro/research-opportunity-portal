# Quick start on this computer

Setup is complete: MySQL 8.4.9, database, private credentials and Python .venv are ready.

1. Open this repository folder in VS Code.
2. Run **Start portal (MySQL + Flask + browser)** from Terminal → Run Task, or double-click `START_PORTAL.cmd`.
3. Use http://localhost:5000. MySQL listens only on 127.0.0.1:3307.
4. Run **Test API (MySQL)** to repeat all ten real integration scenarios. Test databases are created and removed automatically.
5. Run **Stop local MySQL** only after using the app; run **Start local MySQL** to resume.

Existing data survives restarts in `.local/mysql-data`. Keep `.local` and `backend/.env` private; neither belongs in a ZIP or Git. A fresh extracted ZIP requires the reproducible setup in [README](../README.md), because it correctly excludes credentials, runtime and data.

All database, browser and Newman checks now pass. The remaining submission requirement is a genuine video of at most 60 seconds.
