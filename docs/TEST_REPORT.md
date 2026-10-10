# Executed test report — 10 October 2026

Student: Sohrab, 24P-0604, CS-5B. Source of requirements: Assignment_1.pdf, sections 2–9.

## Actual results

| Check | Result | Scope / evidence |
|---|---|---|
| Original test_api.py | PASS: 10/10 | Automatic mock fallback; initial output misleadingly called it an isolated database |
| Repaired test_api.py --mode mock | PASS: 10/10 | Explicit in-memory mock, Flask test client |
| test_validation.py | PASS: 9/9 test methods | Multiple subcases: malformed JSON, required fields, limits, dates, positions, status, CRUD rereads, 404/405, sanitized 500, static assets |
| Real MySQL test mode | UNVERIFIED | Execution attempted; connection failed with InterfaceError (exit 2); no mock fallback |
| Exported collection via Newman | PASS: 10 requests, 18 assertions, 0 failures | Actual HTTP requests to Flask on localhost:5000 with mock storage, one iteration |
| Browser frontend | PASS with mock storage | Create, list, full details, edit positions 2→5, close, refresh, delete and blank-form errors; console error list empty |
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

The same ten scenarios passed in the Python mock suite and the exported Postman collection. These are **not evidence of MySQL persistence**. The browser operated the actual UI; it did not use a hard-coded frontend dataset. Test-only storage was injected in a scratch server outside the repository. Normal app.py always uses MySQL.

Python audit runtime: 3.12. Installed application dependencies: Flask 3.1.3, Flask-CORS 6.0.5, mysql-connector-python 26.7.0, python-dotenv 1.2.4. Requirements retain their existing minimum-version policy. Normal Windows setup uses a project .venv; the audit used isolated workspace packages. VS Code JSON was inspected and parsed, but tasks/F5 were not clicked in VS Code. Installation and MySQL setup must still be verified on a machine with a running MySQL service.

## Finish real verification

Follow README setup, configure MySQL locally, and run `python backend/test_api.py --mode mysql`. This creates/drops only a uniquely named disposable database. Require 10/10 and exit 0. Then run normal Flask, repeat frontend operations and run the Postman collection against that MySQL-backed server. Update this report with actual outcomes. No video has been recorded by this audit.

## Security scope

The owner confirmed old-token revocation in chat. The compromised config was not extracted; clean origin/tracking were written. Original ZIP remains unchanged and must not be redistributed. Scanning checked common GitHub-token, credential-URL and private-key patterns across all reachable objects, plus working files; this is not proof that every conceivable secret format is absent. No shared history was rewritten. Secure Git Credential Manager push dry-run succeeded. See handover for the final pushed SHA.
