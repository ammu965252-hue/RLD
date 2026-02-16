import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "riceguard.db")

def backup_db():
    if os.path.exists(DB_PATH):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = DB_PATH + f".bak_{ts}"
        shutil.copy2(DB_PATH, bak)
        print(f"Backup created: {bak}")
    else:
        print("No database file found to backup.")


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info('{table}')")
    cols = [r[1] for r in cursor.fetchall()]
    return column in cols


def add_role_column():
    if not os.path.exists(DB_PATH):
        print("Database file not found at", DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        if column_exists(cur, 'users', 'role'):
            print("Column 'role' already exists in 'users' table")
            return

        # SQLite supports simple ADD COLUMN
        cur.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
        conn.commit()
        print("Added 'role' column to 'users' table (default 'user')")
    except Exception as e:
        print("Migration failed:", e)
    finally:
        conn.close()


if __name__ == '__main__':
    print("Backing up database...")
    backup_db()
    print("Applying migration to add 'role' column...")
    add_role_column()
    print("Done.")
