from app.database import connect


def _row_to_task(row: sqlite3.Row)-> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
    }


def find_all_tasks(done: bool | None = None, search: str | None = None) -> list[dict]:
    clauses: list[str] = []
    params: list[int] = []
    if done is not None:
        clauses.append("done = %s")
        params.append((done))
    if search and search.strip():
        clauses.append("title LIKE %s")
        params.append(f"%{search.strip()}%")
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    connection = connect()
    try:
        rows = connection.execute(
            f"SELECT id, title, done FROM tasks {where} ORDER BY title",
            params,
        ).fetchall()
        return [_row_to_task(row) for row in rows]
    finally:
        connection.close()

def find_by_id(task_id: int) -> dict | None:
    connection = connect()
    try: 
        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = %s",
            (task_id,),
    ).fetchone()
        return _row_to_task(row) if row else None
    finally:
        connection.close()

def add(new_task: dict) -> dict:
    connection = connect()
    try:
        row = connection.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING id, title, done
            """,
            (new_task["title"], bool(new_task["done"])),
        ).fetchone()
        connection.commit()
        if row is None:
            raise RuntimeError("Inserted task was not found")
        return _row_to_task(row)
    finally:
        connection.close()


def update_task(task_id: int, updated_fields: dict) -> dict | None:
    connection = connect()
    try:
        cursor = connection.execute(
            "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
            (updated_fields["title"], (bool(updated_fields["done"])), task_id),
        )
        connection.commit()
        if cursor.rowcount ==0:
            return None
    finally:
        connection.close()
    return find_by_id(task_id)

def delete_task_repository(task_id: int) -> bool:
   connection = connect()
   try:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,),
        )
        connection.commit()
        return cursor.rowcount > 0
   finally:
        connection.close()

def count_tasks() -> dict:
    connection = connect()
    try:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN done THEN 1 ELSE 0 END) AS done,
                SUM(CASE WHEN NOT done THEN 1 ELSE 0 END) AS pending
            FROM tasks
            """
        ).fetchone()
        return {
            "total": row["total"],
            "done": row["done"] or 0,
            "pending": row["pending"] or 0,
        }
    finally:
        connection.close()