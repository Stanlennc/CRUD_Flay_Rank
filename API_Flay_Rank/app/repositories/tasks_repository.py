

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


def find_all_tasks(done: bool | None = None) -> list[dict]:
    clauses: list[str] = []
    params: list[int] = []
    if done is not None:
        clauses.append("done = ?")
        params.append(int(done))
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    connection = _connect()
    try:
        rows = connection.execute(
            f"SELECT id, title, done FROM tasks {where} ORDER BY title",
            params,
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
    connection = _connect()
    try:
        cursor = connection.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (updated_fields["title"], int(bool(updated_fields["done"])), task_id),
        )
        connection.commit()
        if cursor.rowcount ==0:
            return None
    finally:
        connection.close()
    return find_by_id(task_id)

def delete_task_repository(task_id: int) -> bool:
   connection = _connect()
   try:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )
        connection.commit()
        return cursor.rowcount > 0
   finally:
        connection.close()