import sqlite3

def create_table():
    conn = sqlite3.connect("resume_data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_role TEXT,
    match_score INTEGER,
    ats_score INTEGER,
    matched_skills TEXT,
    missing_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_data(job_role, score, ats, matched, missing):
    conn = sqlite3.connect("resume_data.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO results (job_role, match_score, ats_score, matched_skills, missing_skills)
    VALUES (?, ?, ?, ?, ?)
    """, (job_role, score, ats, matched, missing))

    conn.commit()
    conn.close()