# University Research Opportunity Portal

Sohrab | **24P-0604** | **CS-5B** | Fall 2026 | Computer Networks | Assignment #01

Repository: https://github.com/Sohrab-soomro/research-opportunity-portal

Faculty can create, retrieve, edit, close and delete research opportunities in one place. The frontend reads all application data through Flask REST endpoints; production storage is MySQL. This preserves the existing Python, HTML, CSS and JavaScript implementation.

## Verification and submission status

Read [the actual test report](docs/TEST_REPORT.md) and [requirement audit](docs/ASSIGNMENT_AUDIT.md). Real MySQL 8.4.9 integration, browser CRUD, restart persistence and the Postman collection have now been verified. Mock tests remain available for isolated logic checks. A real video is still required; a script does not satisfy this requirement.

## Requirements

Python 3.10+, MySQL Server 8+, VS Code (recommended), Git and Postman. MySQL must be running and the configured account must have access to the database. Optional Newman execution needs Node.js/npm. The stack uses Flask, Flask-CORS, mysql-connector-python and python-dotenv.

## Ready on this computer

MySQL 8.4.9 and the project `.venv` are installed. The app uses MySQL on **127.0.0.1:3307** and Flask on **http://localhost:5000**. Double-click `START_PORTAL.cmd`, or run the VS Code task **Start portal (MySQL + Flask + browser)**. This starts the project database if necessary, starts Flask, and opens the browser. If Flask is already running, it opens the existing app.

Database files and admin configuration are in ignored `.local/`; the generated app password is in ignored `backend/.env`. Neither is shipped or pushed. The database uses a restricted app account; integration privileges apply only to uniquely named test databases. No system MySQL service or firewall rule was created. Keep `.local/` to retain your local data. `Stop local MySQL` shuts it down safely; it does not delete data.

## Reproduce this isolated Windows setup on another computer

Install MySQL 8.4 from Oracle (or `winget install --id Oracle.MySQL --exact --source winget`), create `.venv`, and install backend requirements as below. Before creating a `.env` file, run:

```powershell
.\.venv\Scripts\python.exe scripts/local_mysql.py setup
.\.venv\Scripts\python.exe backend/test_api.py --mode mysql
.\.venv\Scripts\python.exe scripts/start_portal.py
```

Setup generates private random credentials, creates only a new project data directory/database, and loads two demo rows. It refuses to overwrite an existing `.local/` or `.env`. It expects `C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe`; for another installation set the `MYSQLD_PATH` environment variable first. Port 3307 must be free. These setup/start/stop/status operations were executed successfully during this audit.

For an existing separately managed MySQL server, use the manual steps below instead. Those steps default to port 3306; keep DB_PORT consistent with your server.

## Windows PowerShell setup (existing MySQL server)

Open this repository folder in VS Code, then run from its root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
Copy-Item backend/.env.example backend/.env
```

Create the environment file only if it does not already exist. Edit `backend/.env` locally with your own MySQL connection settings (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `FLASK_PORT`). Never commit it or include it in a submission. Defaults are localhost:3306, database research_portal, and Flask port 5000. No activation or execution-policy changes are needed when using the explicit Python path above.

Open MySQL Workbench and execute `database/schema.sql`, or start the MySQL client from the repository root:

```powershell
mysql -u root -p
```

At the **MySQL prompt**, run:

```sql
SOURCE database/schema.sql;
-- Optional: adds two demo rows every time it is run
SOURCE database/seed.sql;
```

The schema now creates missing tables without dropping existing data. It does not migrate an older incompatible table; back up and inspect such a table before changing it. Seed data is optional and is loaded by the frontend through the API.

Start Flask from the repository root:

```powershell
.\.venv\Scripts\python.exe backend/app.py
```

Open **http://localhost:5000**. Keep the server terminal open. The frontend is served by Flask and requires no separate build. Press Ctrl+C to stop. Do not open the HTML with Live Server on a different port; use Flask's URL.

## Project structure and navigation

```text
.vscode/                  Run, test, browser, Git and debug configurations
backend/app.py            Flask server, frontend serving, JSON errors
backend/config.py         Local environment configuration
backend/db.py             MySQL connection helper
backend/routes/           Five API routes, validation and parameterized SQL
backend/test_api.py       Ten API scenarios; explicit mock/MySQL mode
backend/test_database.py  Disposable database lifecycle
backend/test_validation.py Additional validation/error regression tests
backend/.env.example     Placeholder configuration
backend/requirements.txt Python dependencies
frontend/                 index.html, style.css, script.js
database/schema.sql       Non-destructive schema setup
database/seed.sql         Optional demo rows
scripts/                  Local MySQL setup/start/stop and full app launcher
START_PORTAL.cmd          Double-click launcher for this Windows setup
postman/                  Exported executable collection
docs/                     Audit, report, quick start, map
TEST_REPORT.md            Link to current verified report
```

Use Terminal → Run Task for **Start Flask**, **Test API (mock)**, **Test API (MySQL)**, **Test validation**, **Open frontend** or **Git status**. F5 starts the `Flask portal` debug configuration. Create `.venv` first. See [project map](docs/PROJECT_MAP.md) and [quick start](docs/QUICK_START.md).

## REST API

Base URL: `http://localhost:5000`. JSON responses contain `data` and `message` on success or `error` (and validation `details`) on failure.

| Method | Path | Purpose | Status codes |
|---|---|---|---|
| POST | /api/opportunities | Create | 201, 400, 500 |
| GET | /api/opportunities | List all | 200, 500 |
| GET | /api/opportunities/:id | Full details | 200, 404, 500 |
| PUT | /api/opportunities/:id | Update fields or close | 200, 400, 404, 500 |
| DELETE | /api/opportunities/:id | Delete | 200, 404, 500 |

Create example:

```json
{
  "research_title": "SDN Flow Optimization",
  "research_description": "Compare routing strategies in a simulated network.",
  "research_area": "Computer Networks",
  "faculty_name": "Demo Faculty",
  "department": "Computer Science",
  "required_skills": "Python, Mininet",
  "available_positions": 3,
  "application_deadline": "2026-12-25",
  "status": "Open"
}
```

IDs are generated by MySQL. All six text fields are required and trimmed. Text lengths are checked against schema limits (description: 65,535 UTF-8 bytes); positions must be a positive integer no greater than 2,147,483,647; deadline must be a real YYYY-MM-DD date in MySQL's supported year range; status must be Open or Closed (defaults to Open on creation). PUT accepts a subset such as `{"status":"Closed"}` and preserves other fields. Empty or unrecognized-only updates are rejected. Malformed/non-object JSON returns 400. Past dates are allowed because the assignment does not forbid them. SQL parameters are bound separately. Database failure responses and logs do not include connector error details; debug mode is off.

## Postman

1. Start the real application with MySQL configured, preferably against disposable demo data.
2. Import `postman/Research_Opportunity_Portal.postman_collection.json`.
3. Keep collection `baseUrl` set to `http://localhost:5000`.
4. Run the entire collection in its saved order, once. The first three requests capture their generated IDs. Subsequent requests retrieve, update, close, delete, request the deleted ID (404), and send invalid data (400).
5. Inspect actual responses and assertion results. The run leaves two created test records; delete those through the UI when finished.

Optional command-line execution:

```powershell
npx --yes newman run postman/Research_Opportunity_Portal.postman_collection.json
```

## Automated tests

```powershell
.\.venv\Scripts\python.exe backend/test_api.py --mode mock
.\.venv\Scripts\python.exe -m unittest discover -s backend -p test_validation.py -v
.\.venv\Scripts\python.exe backend/test_api.py --mode mysql
```

Mock mode never contacts MySQL. MySQL mode requires credentials with CREATE DATABASE and DROP DATABASE privileges, creates a unique `research_portal_test_<random>` database, exercises the API, and drops only that database in cleanup. It does not use or reset `DB_NAME`. There is no fallback: unavailable MySQL produces exit code 2, failed assertions exit 1, success exits 0. If the process is forcibly killed, a uniquely named test database may remain; inspect it before manually removing it. Regression tests always use mock storage.

## Troubleshooting

- Missing module: install requirements using the same `.venv` interpreter as the task/debug configuration.
- `mysql` not found: use MySQL Workbench or add the installed MySQL bin directory to PATH.
- HTTP 500/database error: confirm MySQL is running, schema exists, local `.env` credentials and privileges are correct. A Flask startup message alone does not prove a database connection.
- Port 5000 occupied: stop the old server or change FLASK_PORT and the Postman baseUrl/browser URL together.
- Browser cannot connect: start Flask, use its exact URL, and check the terminal.
- MySQL tests fail to connect: fix local MySQL setup; do not describe mock tests as integration results.
most 60 seconds and include the recording or a genuine accessible video link. Use the supplied registration format:
**24P-0604 Sohrab CS-5B.zip**. The assignment's filename example is `P24 0000 NAME CLASS.zip`; the provided student identifier is preserved rather than silently reformatted. Confirm any instructor-specific filename interpretation before submission.
