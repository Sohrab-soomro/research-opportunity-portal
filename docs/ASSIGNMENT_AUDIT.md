# Assignment requirement audit — 10 October 2026

Source of truth: `Assignment_1.pdf` found in the owner's Downloads directory; all six pages were extracted and read. Sections 2–9 govern this audit. User-requested security and VS Code additions are also included below.

PASS = implemented and verified within the stated scope. PARTIAL = incomplete or partly unverified. MISSING = absent. BROKEN = present but unsafe/nonfunctional for its purpose. UNVERIFIED = environment prevented confirmation. A mock PASS never means real database PASS.

Initial state: clean tracked working tree at `3f57395`, main matching public origin/main, eight existing commits. Ignored PUSH_TO_GITHUB.bat was present and retained locally but excluded from deliverables. Existing app, schema, collection, README, report and DOCX were read; original history and frontend were preserved. No new Git repository was initialized.

| Requirement | Initial | Final | Relevant files | Verification | Fix / remaining action |
|---|---|---|---|---|---|
| Unique auto-generated ID | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Research title | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Research description | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Research area | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Faculty name | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Department | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Required skills | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Available positions | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Application deadline | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| Open/Closed status | Present | PASS | database/schema.sql; backend/routes/opportunities.py | Schema inspection; response assertions | Verified in real MySQL mode |
| POST create (201/400) | Present, mock tests passed | PASS (real MySQL) | backend/routes/opportunities.py; backend/test_api.py | Python suite; Newman actual HTTP | Completed real integration |
| GET all (200) | Present, mock tests passed | PASS (real MySQL) | backend/routes/opportunities.py; backend/test_api.py | Python suite; Newman actual HTTP | Completed real integration |
| GET one (200/404) | Present, mock tests passed | PASS (real MySQL) | backend/routes/opportunities.py; backend/test_api.py | Python suite; Newman actual HTTP | Completed real integration |
| PUT update and close (200/400/404) | Present, mock tests passed | PASS (real MySQL) | backend/routes/opportunities.py; backend/test_api.py | Python suite; Newman actual HTTP | Completed real integration |
| DELETE (200/404) | Present, mock tests passed | PASS (real MySQL) | backend/routes/opportunities.py; backend/test_api.py | Python suite; Newman actual HTTP | Completed real integration |
| Required fields, positive positions, real date, JSON, status | PARTIAL | PASS | backend/routes/opportunities.py; backend/test_validation.py | 9 regression methods plus subcases | Fixed oversized text/INT, date shape/range, unknown-only updates |
| Parameterized SQL and safe errors including 500 | PARTIAL (connector details logged) | PASS | backend/routes/opportunities.py | SQL review; forced connection failure regression | Removed raw connector-error logging |
| Complete safe MySQL setup | BROKEN for repeat use (DROP TABLE) | PASS (executed) | database/schema.sql; database/seed.sql | Schema review | Removed DROP; separated optional seed; setup executed on MySQL |
| Create persistence | UNVERIFIED | PASS | backend/db.py; backend/test_database.py | Real MySQL API suite; SQL readback; restart persistence | None |
| Read persistence | UNVERIFIED | PASS | backend/db.py; backend/test_database.py | Real MySQL API suite; SQL readback; restart persistence | None |
| Update persistence | UNVERIFIED | PASS | backend/db.py; backend/test_database.py | Real MySQL API suite; SQL readback; restart persistence | None |
| Closed-status persistence | UNVERIFIED | PASS | backend/db.py; backend/test_database.py | Real MySQL API suite; SQL readback; restart persistence | None |
| Delete persistence and later 404 | UNVERIFIED | PASS | backend/db.py; backend/test_database.py | Real MySQL API suite; SQL readback; restart persistence | None |
| Frontend: List opportunities | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend: View complete details | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend: Create form | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend: Update form | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend: Close opportunity | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend: Delete with confirmation | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend: Success/error messages | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend: Required-field validation | Present; browser initially unverified | PASS (real MySQL) | frontend/index.html; frontend/script.js; frontend/style.css | Actual browser interaction | Repeated against real MySQL |
| Frontend uses REST, no hard-coded opportunities | Present | PASS | frontend/script.js | Source review and browser→Flask HTTP | None |
| Postman: Create at least three | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| Postman: Retrieve all | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| Postman: Retrieve one saved ID | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| Postman: Update | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| Postman: Close | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| Postman: Delete | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| Postman: Deleted ID → 404 | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| Postman: Invalid data → 400 | Present; execution unverified | PASS (real MySQL) | postman/Research_Opportunity_Portal.postman_collection.json | Newman: 10 requests / 18 assertions pass | Repeated successfully against MySQL-backed application |
| README reproducible Windows setup | PARTIAL (destructive setup; shell mismatch) | PASS (isolated Windows setup) | README.md; docs/QUICK_START.md | New MySQL install, .venv, schema/seed, tests and browser executed | None |
| GitHub complete source/schema/README/collection and link | Present | PASS after verified push; see handover | Repository main; README.md | Anonymous fetch; staged review; final remote SHA check | None after push |
| Meaningful development commits | PASS: 8 existing commits | PASS | Git history | git log; preserved history plus logical repair commits | None |
| No secrets in repository/submission | BROKEN local Git config | PASS within scan scope | Sanitized local Git config; .gitignore; .env.example | Pattern scan; archive exclusion; owner revocation confirmation | Do not share original ZIP; no automatic history rewrite |
| VS Code navigation and debug tasks | MISSING | PARTIAL (created, not UI-executed) |  .vscode/*; docs/PROJECT_MAP.md | JSON parsing and path review | Run tasks/F5 after .venv setup in VS Code |
| Practical <=60-second demo script | PARTIAL (too much typing/speech) | PASS script; actual video MISSING | docs/DEMO_VIDEO_SCRIPT.md; preserved DOCX | Timeline review; prefilled unsent form workflow | Record and verify genuine <=60-second video |
| Final ZIP with all deliverables | PARTIAL | PARTIAL: video MISSING | 24P-0604 Sohrab CS-5B.zip | Extracted package inspection; see handover | Add actual MP4/link, repackage |

Follow-up: MySQL 8.4.9 installed, new isolated local instance configured, all ten real integration scenarios passed, Newman 18/18 passed against MySQL, browser CRUD and restart durability passed. Only actual video remains missing; VS Code UI task/debug clicks remain unverified, although their commands were exercised.
