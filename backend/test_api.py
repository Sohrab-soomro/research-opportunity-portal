"""
University Research Opportunity Portal - Automated API Test Runner
Tests all 10 required CRUD, status, and validation scenarios.

Usage:
    cd backend
    python test_api.py
"""
import sys
import os
from datetime import datetime, date

# Ensure backend root is in import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import json
import app as portal_app
import routes.opportunities as opp_module

# Lightweight DB fallback mock in case MySQL service is offline during local test
class MockCursor:
    def __init__(self, db_store):
        self.db_store = db_store
        self.lastrowid = None
        self._fetched = []
        self._row_index = 0

    def execute(self, query, params=None):
        query = query.strip()
        params = params or ()

        if query.upper().startswith("INSERT INTO OPPORTUNITIES"):
            new_id = self.db_store["next_id"]
            self.db_store["next_id"] += 1
            row = {
                "id": new_id,
                "research_title": params[0],
                "research_description": params[1],
                "research_area": params[2],
                "faculty_name": params[3],
                "department": params[4],
                "required_skills": params[5],
                "available_positions": params[6],
                "application_deadline": params[7] if isinstance(params[7], date) else datetime.strptime(str(params[7]), "%Y-%m-%d").date(),
                "status": params[8],
            }
            self.db_store["rows"][new_id] = row
            self.lastrowid = new_id

        elif "WHERE ID = %S" in query.upper() and query.upper().startswith("SELECT"):
            opp_id = int(params[0])
            row = self.db_store["rows"].get(opp_id)
            self._fetched = [dict(row)] if row else []
            self._row_index = 0

        elif query.upper().startswith("SELECT * FROM OPPORTUNITIES"):
            rows = sorted(self.db_store["rows"].values(), key=lambda r: r["id"], reverse=True)
            self._fetched = [dict(r) for r in rows]
            self._row_index = 0

        elif query.upper().startswith("UPDATE OPPORTUNITIES"):
            opp_id = int(params[-1])
            if opp_id in self.db_store["rows"]:
                row = self.db_store["rows"][opp_id]
                row["research_title"] = params[0]
                row["research_description"] = params[1]
                row["research_area"] = params[2]
                row["faculty_name"] = params[3]
                row["department"] = params[4]
                row["required_skills"] = params[5]
                row["available_positions"] = params[6]
                row["application_deadline"] = params[7] if isinstance(params[7], date) else datetime.strptime(str(params[7]), "%Y-%m-%d").date()
                row["status"] = params[8]

        elif query.upper().startswith("DELETE FROM OPPORTUNITIES"):
            opp_id = int(params[0])
            self.db_store["rows"].pop(opp_id, None)

    def fetchone(self):
        if self._row_index < len(self._fetched):
            res = self._fetched[self._row_index]
            self._row_index += 1
            return res
        return None

    def fetchall(self):
        res = self._fetched[self._row_index:]
        self._row_index = len(self._fetched)
        return res

    def close(self):
        pass


class MockConnection:
    def __init__(self, db_store):
        self.db_store = db_store

    def cursor(self, dictionary=True):
        return MockCursor(self.db_store)

    def commit(self):
        pass

    def close(self):
        pass


def run_tests():
    # Attempt real connection first; if MySQL is unavailable, switch to MockConnection
    using_mock = False
    try:
        real_conn = opp_module.get_connection()
        real_conn.close()
        print("[INFO] Live MySQL connection detected. Running tests against MySQL database.")
    except Exception as e:
        using_mock = True
        print(f"[INFO] Live MySQL not reachable ({e}). Using isolated test database.")
        db_store = {"next_id": 1, "rows": {}}
        opp_module.get_connection = lambda: MockConnection(db_store)

    client = portal_app.app.test_client()
    results = []

    print("=" * 70)
    print("  RESEARCH OPPORTUNITY PORTAL — 10 REST API VERIFICATION TESTS")
    print("=" * 70)

    # Test 1 - Create Opportunity 1
    t1_payload = {
        "research_title": "Congestion Control in 5G Networks",
        "research_description": "Compare TCP congestion control algorithms (Cubic, BBR) over simulated 5G links using ns-3.",
        "research_area": "Computer Networks",
        "faculty_name": "Dr. Sana Ahmed",
        "department": "Computer Science",
        "required_skills": "C++, ns-3, TCP/IP",
        "available_positions": 2,
        "application_deadline": "2026-12-01",
        "status": "Open"
    }
    r1 = client.post("/api/opportunities", json=t1_payload)
    d1 = r1.get_json() or {}
    id1 = d1.get("data", {}).get("id")
    p1 = (r1.status_code == 201 and id1 is not None)
    results.append(("1", "Create Opportunity 1", 201, r1.status_code, "PASS" if p1 else "FAIL"))

    # Test 2 - Create Opportunity 2
    t2_payload = {
        "research_title": "IoT-Based Smart Irrigation",
        "research_description": "Design a low-cost soil moisture sensor network that automates irrigation for small farms.",
        "research_area": "Internet of Things",
        "faculty_name": "Dr. Bilal Hussain",
        "department": "Electrical Engineering",
        "required_skills": "Arduino, Embedded C, MQTT",
        "available_positions": 3,
        "application_deadline": "2026-11-20",
        "status": "Open"
    }
    r2 = client.post("/api/opportunities", json=t2_payload)
    d2 = r2.get_json() or {}
    id2 = d2.get("data", {}).get("id")
    p2 = (r2.status_code == 201 and id2 is not None)
    results.append(("2", "Create Opportunity 2", 201, r2.status_code, "PASS" if p2 else "FAIL"))

    # Test 3 - Create Opportunity 3
    t3_payload = {
        "research_title": "Phishing Website Detection",
        "research_description": "Train a classifier that detects phishing URLs using lexical and host-based features.",
        "research_area": "Cyber Security",
        "faculty_name": "Dr. Nadia Rehman",
        "department": "Cyber Security",
        "required_skills": "Python, scikit-learn, Networking basics",
        "available_positions": 1,
        "application_deadline": "2026-12-10",
        "status": "Open"
    }
    r3 = client.post("/api/opportunities", json=t3_payload)
    d3 = r3.get_json() or {}
    id3 = d3.get("data", {}).get("id")
    p3 = (r3.status_code == 201 and id3 is not None)
    results.append(("3", "Create Opportunity 3", 201, r3.status_code, "PASS" if p3 else "FAIL"))

    # Test 4 - Get All Opportunities
    r4 = client.get("/api/opportunities")
    d4 = r4.get_json() or {}
    p4 = (r4.status_code == 200 and len(d4.get("data", [])) >= 3)
    results.append(("4", "Get All Opportunities", 200, r4.status_code, "PASS" if p4 else "FAIL"))

    # Test 5 - Get One Opportunity by ID
    target_id = id1 or 1
    r5 = client.get(f"/api/opportunities/{target_id}")
    d5 = r5.get_json() or {}
    p5 = (r5.status_code == 200 and d5.get("data", {}).get("id") == target_id)
    results.append(("5", "Get One Opportunity", 200, r5.status_code, "PASS" if p5 else "FAIL"))

    # Test 6 - Update Opportunity
    t6_payload = {
        "research_title": "Congestion Control in 5G and Wi-Fi 7 Networks",
        "research_description": "Compare TCP congestion control algorithms (Cubic, BBR) over simulated 5G links using ns-3.",
        "research_area": "Computer Networks",
        "faculty_name": "Dr. Sana Ahmed",
        "department": "Computer Science",
        "required_skills": "C++, ns-3, TCP/IP, Python",
        "available_positions": 4,
        "application_deadline": "2026-12-20",
        "status": "Open"
    }
    r6 = client.put(f"/api/opportunities/{target_id}", json=t6_payload)
    d6 = r6.get_json() or {}
    p6 = (r6.status_code == 200 and d6.get("data", {}).get("available_positions") == 4 and d6.get("data", {}).get("application_deadline") == "2026-12-20")
    results.append(("6", "Update Opportunity", 200, r6.status_code, "PASS" if p6 else "FAIL"))

    # Test 7 - Close Opportunity (Open -> Closed)
    close_id = id2 or 2
    r7 = client.put(f"/api/opportunities/{close_id}", json={"status": "Closed"})
    d7 = r7.get_json() or {}
    p7 = (r7.status_code == 200 and d7.get("data", {}).get("status") == "Closed")
    results.append(("7", "Close Opportunity (Open->Closed)", 200, r7.status_code, "PASS" if p7 else "FAIL"))

    # Test 8 - Delete Opportunity
    del_id = id3 or 3
    r8 = client.delete(f"/api/opportunities/{del_id}")
    p8 = (r8.status_code == 200)
    results.append(("8", "Delete Opportunity", 200, r8.status_code, "PASS" if p8 else "FAIL"))

    # Test 9 - Get Deleted Opportunity (404)
    r9 = client.get(f"/api/opportunities/{del_id}")
    p9 = (r9.status_code == 404)
    results.append(("9", "Get Deleted ID (404)", 404, r9.status_code, "PASS" if p9 else "FAIL"))

    # Test 10 - Create with Invalid Data (400)
    t10_payload = {
        "research_title": "",
        "research_description": "Missing several required fields",
        "available_positions": -2,
        "application_deadline": "not-a-date",
        "status": "Pending"
    }
    r10 = client.post("/api/opportunities", json=t10_payload)
    d10 = r10.get_json() or {}
    p10 = (r10.status_code == 400 and isinstance(d10.get("details"), list) and len(d10.get("details")) > 0)
    results.append(("10", "Invalid/Missing Data (400)", 400, r10.status_code, "PASS" if p10 else "FAIL"))

    print(f"{'#':<3} | {'Operation':<32} | {'Expected':<8} | {'Actual':<8} | {'Status'}")
    print("-" * 70)
    for num, op, exp, act, st in results:
        print(f"{num:<3} | {op:<32} | {exp:<8} | {act:<8} | {st}")

    all_passed = all(st == "PASS" for _, _, _, _, st in results)
    print("=" * 70)
    print(f"OVERALL RESULT: {'ALL TESTS PASSED!' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
