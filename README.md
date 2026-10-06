# University Research Opportunity Portal

## Student Information

- **Student Name:** Sohrab
- **Registration / Roll No:** 24P-0604
- **Class:** CS-5B
- **Semester:** Fall 2026
- **Course:** Computer Networks (CN)
- **Assignment:** Assignment #01
- **Date:** 07/10/2026
- **GitHub Repository:** https://github.com/Sohrab-soomro/research-opportunity-portal
- **Submission Type:** Complete Project (Backend, Frontend, Database, Postman, Tests)

---

## Description

Research opportunities at the university are currently shared through emails, WhatsApp groups and noticeboards, so students miss them and faculty find them hard to manage.
This web application gives faculty members one place to **post, view, update, close and delete** research opportunities.

It consists of:

- a **REST API** built with Python (Flask),
- a **MySQL** database that stores every opportunity,
- a simple **HTML / CSS / JavaScript** frontend that talks to the API using `fetch()` (no hard-coded data).

## Technologies

- Python 3 + Flask (backend REST API)
- Flask-CORS
- MySQL 8 (database) + `mysql-connector-python`
- HTML, CSS, JavaScript (frontend)
- Postman (API testing)

## Features

**Backend (REST API)**

| Operation | Method & Endpoint | Success | Errors |
|---|---|---|---|
| Create an opportunity | `POST /api/opportunities` | 201 Created | 400, 500 |
| Get all opportunities | `GET /api/opportunities` | 200 OK | 500 |
| Get one opportunity | `GET /api/opportunities/:id` | 200 OK | 404, 500 |
| Update an opportunity (also used to close it) | `PUT /api/opportunities/:id` | 200 OK | 400, 404, 500 |
| Delete an opportunity | `DELETE /api/opportunities/:id` | 200 OK | 404, 500 |

- Input validation (required fields, positive number of positions, valid date, status must be `Open` or `Closed`).
- Clean JSON responses for every result, e.g. `{"message": "...", "data": {...}}` or `{"error": "..."}`.
- Database errors are logged on the server and return a simple `500` message (no stack traces to users).

**Frontend**

1. Displays all research opportunities in a table (loaded from the API).
2. Shows complete details of a selected opportunity (**View**).
3. Form to create a new opportunity (**+ New Opportunity**).
4. Edit form that loads the existing data and saves changes (**Edit**).
5. **Close** button that changes the status from Open to Closed in the database.
6. **Delete** button with a confirmation dialog.
7. Success and error messages (including "server not reachable" and "not found").
8. Basic validation of required form fields before sending the request.

## Project Structure

```
research-opportunity-portal/
├── backend/
│   ├── app.py                  # Starts Flask, serves the frontend, JSON error handlers
│   ├── config.py               # Reads database settings from the .env file
│   ├── db.py                   # Opens a MySQL connection
│   ├── routes/
│   │   ├── __init__.py
│   │   └── opportunities.py    # The 5 REST API endpoints + validation
│   ├── test_api.py             # Automated API test suite (10 test cases)
│   ├── requirements.txt        # Python packages
│   └── .env.example            # Template for your own .env file
├── frontend/
│   ├── index.html              # Page layout (list, details, form)
│   ├── style.css               # Styling
│   └── script.js               # API calls and page logic
├── database/
│   └── schema.sql              # Creates the database, table and sample rows
├── postman/
│   └── Research_Opportunity_Portal.postman_collection.json
├── README.md
└── .gitignore
```

## Requirements

Install these first:

- **Python 3.10 or newer** — https://www.python.org/downloads/ (tick "Add Python to PATH" on Windows)
- **MySQL Server 8.0 or newer** (MySQL Workbench or the MySQL command line is helpful)
- **Postman** — https://www.postman.com/downloads/
- A web browser (Chrome, Edge or Firefox)

## Database Setup

1. **Install MySQL** and make sure the MySQL server is running. Remember your MySQL username and password.
2. **Create the database using `schema.sql`.** Choose one option:
   - *Command line* (run from the project folder):
     ```bash
     mysql -u root -p < database/schema.sql
     ```
   - *MySQL Workbench*: File → Open SQL Script → select `database/schema.sql` → click the ⚡ Execute button.

   This creates the database `research_portal`, the table `opportunities`, and 2 sample rows.
   > Running `schema.sql` again resets the table (it drops and recreates it).
3. **Configure environment variables.** Go to the `backend` folder, copy `.env.example` to a new file named `.env`:
   - Windows: `copy .env.example .env`
   - macOS / Linux: `cp .env.example .env`

   Open `.env` and put in your own MySQL password:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=research_portal
   FLASK_PORT=5000
   ```
   The `.env` file is listed in `.gitignore`, so your password is never uploaded to GitHub.

## Backend Setup

Open a terminal in the `backend` folder:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

- **Windows (Command Prompt):** `venv\Scripts\activate`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
  (if blocked, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`)
- **macOS / Linux:** `source venv/bin/activate`

Install the packages and start the server:

```bash
pip install -r requirements.txt
python app.py
```

You should see `Running on http://127.0.0.1:5000`. Keep this terminal open.

## Frontend Setup

The Flask backend also serves the frontend, so nothing extra is needed:

1. Start the backend (see above).
2. Open **http://localhost:5000** in your browser.

(Opening `frontend/index.html` directly also works while the backend is running, because CORS is enabled and the page then calls `http://localhost:5000`.)

## API Endpoints

Base URL: `http://localhost:5000`

### 1. Create — `POST /api/opportunities`

Request body:
```json
{
  "research_title": "Congestion Control in 5G Networks",
  "research_description": "Compare TCP congestion control algorithms over simulated 5G links.",
  "research_area": "Computer Networks",
  "faculty_name": "Dr. Sana Ahmed",
  "department": "Computer Science",
  "required_skills": "C++, ns-3, TCP/IP",
  "available_positions": 2,
  "application_deadline": "2026-12-01",
  "status": "Open"
}
```
`status` is optional when creating (defaults to `Open`).
Response `201 Created`:
```json
{ "message": "Research opportunity created successfully", "data": { "id": 3, "...": "..." } }
```

### 2. Get all — `GET /api/opportunities`
Response `200 OK`: `{ "message": "...", "count": 3, "data": [ {...}, {...} ] }`

### 3. Get one — `GET /api/opportunities/:id`
`200 OK` with the opportunity, or `404 Not Found`: `{ "error": "Research opportunity not found" }`

### 4. Update — `PUT /api/opportunities/:id`
Send the fields you want to change (any or all of them). Example — close an opportunity:
```json
{ "status": "Closed" }
```
`200 OK` with the updated record, `400` for invalid data, `404` if the ID does not exist.

### 5. Delete — `DELETE /api/opportunities/:id`
`200 OK`: `{ "message": "Research opportunity deleted successfully", "data": { "id": 3 } }`, or `404`.

### Validation rules (400 Bad Request)
- `research_title`, `research_description`, `research_area`, `faculty_name`, `department`, `required_skills` must not be empty
- `available_positions` must be a whole number greater than 0
- `application_deadline` must be a valid date in `YYYY-MM-DD` format
- `status` must be `Open` or `Closed`
- The request body must be valid JSON

Example 400 response:
```json
{ "error": "Invalid input", "details": ["research_title is required", "status must be either 'Open' or 'Closed'"] }
```

## API Testing

### Option A — Automated CLI Test Suite
An automated test script is provided in `backend/test_api.py`. It runs all 10 verification scenarios against the Flask API:
```bash
cd backend
python test_api.py
```
This tests all CRUD endpoints, response codes (201, 200, 400, 404), data validation, and status transitions.

### Option B — Postman Collection Testing

1. Start the backend (`python app.py`).
2. Open Postman → **Import** → select `postman/Research_Opportunity_Portal.postman_collection.json`.
3. The collection uses the variable `baseUrl = http://localhost:5000`.
4. Run the requests **in order** (or click the collection → **Run** to use the Collection Runner):

| # | Request | Expected |
|---|---|---|
| 1–3 | Create Opportunity 1, 2, 3 | 201 Created (IDs are saved automatically) |
| 4 | Get All Opportunities | 200 OK |
| 5 | Get One Opportunity by ID | 200 OK |
| 6 | Update Opportunity | 200 OK |
| 7 | Close Opportunity (Open → Closed) | 200 OK, `status: "Closed"` |
| 8 | Delete Opportunity | 200 OK |
| 9 | Get Deleted Opportunity | 404 Not Found |
| 10 | Create with Invalid Data | 400 Bad Request |

Each request has a small test script that checks the status code, so the Runner shows pass/fail for every step.

## Troubleshooting

- **"Cannot connect to the server"** in the browser → the backend is not running; start it with `python app.py`.
- **"A database error occurred"** → MySQL is not running, or the values in `backend/.env` are wrong, or `schema.sql` was not run.
- **`ModuleNotFoundError`** → activate the virtual environment and run `pip install -r requirements.txt` again.
