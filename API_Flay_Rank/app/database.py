import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tasks.db"

SEED_TASKS: list[tuple[int, str, int]] = [
    (1, "Code at night", 1),
    (2, "Run at the park", 0),
    (3, "Have a lunch", 1),
]

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL CHECK (done IN (0, 1))
)
"""

def init_db() -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute(CREATE_TASKS_TABLE)
        row = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()
        task_count = int(row[0]) if row else 0
        if task_count == 0:
            connection.executemany(
                "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
                SEED_TASKS,
            )
        connection.commit()
    finally:
        connection.close()
