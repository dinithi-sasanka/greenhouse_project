# utils/db.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def get_connection():
    """Return a new database connection."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


# ---------- FETCH ALL USERS ----------
def fetch_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


# ---------- ADD USER ----------
def add_user(username, password, role, email, address, telephone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, password, role, email, address, telephone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (username, password, role, email, address, telephone))
    conn.commit()
    cur.close()
    conn.close()


# ---------- DELETE USER ----------
def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


# ---------- UPDATE USER ----------
def update_user(user_id, username, role, email, address, telephone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET username=%s, role=%s, email=%s, address=%s, telephone=%s
        WHERE id=%s
    """, (username, role, email, address, telephone, user_id))
    conn.commit()
    cur.close()
    conn.close()


# ---------- SEARCH USERS ----------
def search_users(keyword):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    like = f"%{keyword}%"
    cur.execute("""
        SELECT * FROM users
        WHERE username ILIKE %s
           OR email ILIKE %s
           OR role ILIKE %s
           OR telephone ILIKE %s
    """, (like, like, like, like))
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


# ---------- VALIDATE LOGIN ----------
def validate_user(username, password):
    """
    Returns user dict if username and password match, else None.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT * FROM users
        WHERE username = %s AND password = %s
    """, (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user
