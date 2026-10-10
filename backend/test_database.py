"""Provide explicit mock tests or a uniquely named disposable MySQL database."""
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4
import mysql.connector
from config import DB_CONFIG
import routes.opportunities as routes


@contextmanager
def test_database(mode):
    original = routes.get_connection
    admin = None
    created = False
    name = "research_portal_test_" + uuid4().hex
    try:
        if mode == "mock":
            from test_api import MockConnection
            store = {"next_id": 1, "rows": {}}
            routes.get_connection = lambda: MockConnection(store)
            print("MODE: MOCK - API logic only; does NOT verify MySQL persistence")
        elif mode == "mysql":
            config = dict(DB_CONFIG)
            config.pop("database", None)
            admin = mysql.connector.connect(**config)
            cursor = admin.cursor()
            cursor.execute(f"CREATE DATABASE `{name}`")
            created = True
            cursor.execute(f"USE `{name}`")
            sql = (Path(__file__).parent.parent / "database/schema.sql").read_text()
            table = sql[sql.index("CREATE TABLE"):]
            cursor.execute(table.strip().rstrip(";"))
            cursor.close()
            config["database"] = name
            routes.get_connection = lambda: mysql.connector.connect(**config)
            print("MODE: MYSQL - disposable database", name)
        else:
            raise ValueError("Unknown test mode")
        yield
    finally:
        routes.get_connection = original
        if admin:
            try:
                if created:
                    cursor = admin.cursor()
                    cursor.execute(f"DROP DATABASE `{name}`")
                    cursor.close()
            finally:
                admin.close()
