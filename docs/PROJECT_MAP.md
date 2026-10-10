# Project map

| Demonstration component | Open | What to show |
|---|---|---|
| Running backend | backend/app.py and terminal | Flask on port 5000; startup alone does not verify MySQL |
| Frontend | http://localhost:5000 | List, View, Create, Edit, Close, Delete |
| REST API and validation | backend/routes/opportunities.py | Five routes, status codes, bound SQL parameters |
| Database connection | backend/db.py and config.py | Environment variable names; keep real .env hidden |
| Database fields | database/schema.sql | ID, all nine user fields and constraints |
| Optional demo data | database/seed.sql | Two harmless examples |
| Frontend requests | frontend/script.js | fetch API, form validation and messages |
| Page and styles | frontend/index.html and style.css | Three views and simple styling |
| API requests/responses | postman/Research_Opportunity_Portal.postman_collection.json | Import into Postman; run in order |
| Test execution | backend/test_api.py and test_validation.py | Explicit test mode, honest results |
| Git history | Source Control / terminal | git log --oneline; repository link in README |
| VS Code controls | .vscode/tasks.json, launch.json, extensions.json | Run tasks and F5 |
| Recording | docs/DEMO_VIDEO_SCRIPT.md | Prepared tabs and timed narration |

Suggested editor tab order: app.py → frontend/script.js → routes/opportunities.py → schema.sql → collection → README. Keep database passwords, Git credentials and private windows out of the recording.

Local setup: `scripts/local_mysql.py`; full launcher: `START_PORTAL.cmd` / `scripts/start_portal.py`. VS Code tasks include Start portal and Start/Stop/Status local MySQL.
