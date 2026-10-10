# Executed test report — 10 October 2026

Student: Sohrab, 24P-0604, CS-5B. Source of requirements: Assignment_1.pdf, sections 2–9.

## Actual results

| Check | Result | Scope / evidence |
|---|---|---|
| Original test_api.py | PASS: 10/10 | Automatic mock fallback; initial output misleadingly called it an isolated database |
| Repaired test_api.py --mode mock | PASS: 10/10 | Explicit in-memory mock, Flask test client |
| test_validation.py | PASS: 9/9 test methods | Multiple subcases: malformed JSON, required fields, limits, dates, positions, status, CRUD rereads, 404/405, sanitized 500, static assets |
| Real MySQL test mode | PASS: 10/10 | MySQL Community 8.4.9; unique disposable database created and removed; exit 0 |
| Exported collection via Newman | PASS: 10 requests, 18 assertions, 0 failures | Repeated successfully against real MySQL-backed Flask; actual HTTP, one iteration |
| Browser frontend | PASS with real MySQL | Create, list, full details, edit positions 2→5, close, refresh, delete and blank-form errors; no browser console errors |
| Restart persistence | PASS | Browser-created record and edits survived MySQL shutdown/start; direct SQL confirmed; disposable test DB cleanup confirmed |
| JavaScript syntax | PASS | node --check frontend/script.js |
| Credential-pattern scan | PASS within scan scope | No matches in reachable Git objects or working source; sanitized .git/config, no embedded credential URLs |

## API scenario results

| Scenario | Expected and observed HTTP |
|---|---|
| Create records 1, 2 and 3 | 201, 201, 201 |
| List | 200 |
| Retrieve one | 200 |
| Update | 200 |
| Close | 200 |
| Delete | 200 |
| Retrieve deleted ID | 404 |
| Invalid payload | 400 |

The ten scenarios now pass in both explicit mock mode and real MySQL mode. Newman repeated them against the normal Flask server and real MySQL storage. Browser-created record #6 was edited from 2 to 5 positions, closed, verified through SQL, verified after a MySQL restart, and deleted through the browser. The deleted record subsequently returned HTTP 404. No mock injection was used for these new checks.

MySQL Community 8.4.9 was installed from Oracle's package through winget; its installer hash and executable Authenticode signature were verified. New loopback instance: 127.0.0.1:3307. New data directory: ignored .local/mysql-data. The private app account has CRUD rights on research_portal and setup/CRUD rights only on the test-database naming pattern. The setup script generated credentials without printing them. Initial schema and optional seed both executed successfully. Database shutdown/start/status were executed; data persisted. The .venv was created and requirements installed successfully.

Python 3.12; Flask 3.1.3, Flask-CORS 6.0.5, mysql-connector-python 26.7.0, python-dotenv 1.2.4. VS Code configuration is parsed and its equivalent commands executed; F5/task clicks in the VS Code UI remain unverified because native app controls are unavailable. No video has been recorded; available browser controls do not expose recording.

Reproduce with README's isolated Windows setup and `python backend/test_api.py --mode mysql`. Mock results from the first audit remain historical context and are not substituted for these real runs.

## Security scope

The owner confirmed old-token revocation in chat. The compromised config was not extracted; clean origin/tracking were written. Original ZIP remains unchanged and must not be redistributed. Scanning checked common GitHub-token, credential-URL and private-key patterns across all reachable objects, plus working files; this is not proof that every conceivable secret format is absent. No shared history was rewritten. Secure Git Credential Manager push dry-run succeeded. See handover for the final pushed SHA.
