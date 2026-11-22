

import sqlite3
from app.database import DB_PATH

SEED_TASKS = [
    {"id": 1, "title": "Code at night", "done": True},
    {"id": 2, "title": "Run at the park", "done": False},
    {"id": 3, "title": "Have a lunch", "done": True},
]


tasks = [task.copy() for task in SEED_TASKS]

def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def _row_to_task(row: sqlite3.Row)-> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
    }


def find_all_tasks() -> list[dict]:
    connection = _connect()
    try:
        rows = connection.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()
        return [_row_to_task(row) for row in rows]
    finally:
        connection.close()

def find_by_id(task_id: int) -> dict | None:
    connection = _connect()
    try: 
        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,),
    ).fetchone()
        return _row_to_task(row) if row else None
    finally:
        connection.close()

def add(new_task: dict) -> dict:
    connection = _connect()
    try:
        cursor = connection.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (new_task["title"], int(bool(new_task["done"]))),
        )
        connection.commit()
        return {
            "id": cursor.lastrowid,
            "title": new_task["title"],
            "done": bool(new_task["done"]),
        }
    finally:
        connection.close()


def update_task(task_id: int, updated_fields: dict) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            task.update(updated_fields)
            return task
    return None

def delete_task_repository(task_id: int) -> bool:
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            return True
    return False