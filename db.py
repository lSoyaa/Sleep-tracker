import sqlite3

conn = sqlite3.connect("sleep.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sleep_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    note TEXT
)
""")

conn.commit()
conn.close()

#print("Database and table created successfully")

def insert_sessions(user_id, start_time, end_time, duration_minutes, note):
    conn = sqlite3.connect("sleep.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO  sleep_sessions (user_id, start_time, end_time, duration_minutes, note)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, start_time, end_time, duration_minutes, note)
    )

    conn.commit()
    conn.close()

def get_last(user_id):
    conn = sqlite3.connect("sleep.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT start_time, end_time, duration_minutes, note
        FROM sleep_sessions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    result = cursor.fetchone()
    conn.close()

    return result

def stat(user_id):
    conn = sqlite3.connect("sleep.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) as total,
            AVG(duration_minutes) as avarenge,
            MIN(duration_minutes) as minimum,
            MAX(duration_minutes) as maximum
        FROM sleep_sessions
        WHERE user_id = ?
        """,
        (user_id,)
    )

    result = cursor.fetchone()
    conn.close()

    return result


#if __name__ == "__main__":
 #   result = get_last(123)
 #   print(result)

