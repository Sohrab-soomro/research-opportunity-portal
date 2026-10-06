# REST API Testing & Verification Report

**Course:** Computer Networks (CN) — Fall 2026  
**Assignment:** Assignment #01 — University Research Opportunity Portal  
**Student:** Sohrab (24P-0604, CS-5B)  

---

## 1. Summary of Test Execution

All 10 required operations were verified against the Flask REST API. Each test checks HTTP status codes, request/response headers, JSON body structure, and data validation rules.

| Test # | Operation | HTTP Method | Endpoint | Expected Status | Actual Status | Result |
|:---:|:---|:---:|:---|:---:|:---:|:---:|
| 1 | Create Opportunity 1 (5G Networks) | `POST` | `/api/opportunities` | 201 Created | 201 Created | **PASS** |
| 2 | Create Opportunity 2 (Smart Irrigation) | `POST` | `/api/opportunities` | 201 Created | 201 Created | **PASS** |
| 3 | Create Opportunity 3 (Phishing Detection) | `POST` | `/api/opportunities` | 201 Created | 201 Created | **PASS** |
| 4 | Retrieve All Opportunities | `GET` | `/api/opportunities` | 200 OK | 200 OK | **PASS** |
| 5 | Retrieve Single Opportunity by ID | `GET` | `/api/opportunities/:id` | 200 OK | 200 OK | **PASS** |
| 6 | Update Opportunity (Title, Positions, Deadline) | `PUT` | `/api/opportunities/:id` | 200 OK | 200 OK | **PASS** |
| 7 | Close Opportunity (`Open` → `Closed`) | `PUT` | `/api/opportunities/:id` | 200 OK | 200 OK | **PASS** |
| 8 | Delete Opportunity | `DELETE` | `/api/opportunities/:id` | 200 OK | 200 OK | **PASS** |
| 9 | Retrieve Deleted Opportunity | `GET` | `/api/opportunities/:id` | 404 Not Found | 404 Not Found | **PASS** |
| 10 | Submit Invalid / Missing Fields | `POST` | `/api/opportunities` | 400 Bad Request | 400 Bad Request | **PASS** |

---

## 2. Detailed Verification by Scenario

### Test 1–3: Create Three Opportunities (`POST /api/opportunities`)
- **Input:** Complete JSON objects containing title, description, area, faculty, department, skills, positions, deadline, and status.
- **Verification:** Database stores record, assigns auto-increment ID, returns HTTP `201 Created`, and echoes created object.

### Test 4: Retrieve All Opportunities (`GET /api/opportunities`)
- **Input:** No body required.
- **Verification:** Returns HTTP `200 OK`, JSON array containing all opportunities, sorted newest first (`ORDER BY id DESC`).

### Test 5: Retrieve One Opportunity (`GET /api/opportunities/:id`)
- **Input:** Target opportunity ID.
- **Verification:** Returns HTTP `200 OK` and specific record matching the requested ID.

### Test 6: Update Opportunity (`PUT /api/opportunities/:id`)
- **Input:** JSON payload with updated available positions, deadline, and skills.
- **Verification:** Existing record is merged, updated in database, and returned with HTTP `200 OK`.

### Test 7: Change Status from Open to Closed (`PUT /api/opportunities/:id`)
- **Input:** `{"status": "Closed"}`
- **Verification:** Status successfully changes to `Closed`. Returns HTTP `200 OK`.

### Test 8: Delete Opportunity (`DELETE /api/opportunities/:id`)
- **Input:** Target opportunity ID.
- **Verification:** Opportunity is removed from database. Returns HTTP `200 OK` with confirmation message.

### Test 9: Request Deleted Opportunity (`GET /api/opportunities/:id`)
- **Input:** ID of previously deleted opportunity.
- **Verification:** Returns HTTP `404 Not Found` with `{"error": "Research opportunity not found"}`.

### Test 10: Input Validation (`POST /api/opportunities`)
- **Input:** Empty title, negative available positions, invalid date format, invalid status.
- **Verification:** Request is rejected before database insertion. Returns HTTP `400 Bad Request` with array of validation error messages.

---

## 3. How to Run Tests

### Via CLI Automated Script:
```bash
cd backend
python test_api.py
```

### Via Postman Collection:
1. Open Postman.
2. Click **Import** and select `postman/Research_Opportunity_Portal.postman_collection.json`.
3. Run the collection using Postman Collection Runner.
