"""
Database helper: opens a new MySQL connection for each request.
"""
import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Return a new connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)
