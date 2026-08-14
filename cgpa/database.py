import os
import sqlite3

DB_DIR = "database"
DB_NAME = os.path.join(DB_DIR, "cgpa.db")


def _is_valid_database(path):
    if not os.path.exists(path):
        return False

    try:
        with sqlite3.connect(path) as conn:
            conn.execute("SELECT name FROM sqlite_master LIMIT 1")
        return True
    except sqlite3.DatabaseError:
        return False


def create_database():
    os.makedirs(DB_DIR, exist_ok=True)

    if os.path.exists(DB_NAME) and not _is_valid_database(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            register_no TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            batch TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_no TEXT NOT NULL,
            semester INTEGER NOT NULL,
            subject_code TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            grade TEXT NOT NULL,
            grade_point REAL NOT NULL,
            credit REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_student(name, register_no, department, batch):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, register_no, department, batch)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        register_no,
        department,
        batch
    ))

    conn.commit()
    conn.close()


def add_subject(
    register_no,
    semester,
    subject_code,
    subject_name,
    grade,
    grade_point,
    credit
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subjects
        (
            register_no,
            semester,
            subject_code,
            subject_name,
            grade,
            grade_point,
            credit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        register_no,
        semester,
        subject_code,
        subject_name,
        grade,
        grade_point,
        credit
    ))

    conn.commit()
    conn.close()