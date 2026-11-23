from app.repositories.tasks_repository import find_by_id, find_all_tasks, add, update_task, delete_task_repository, count_tasks


def list_tasks(done: bool | None = None, search: str | None = None):
    return find_all_tasks(done=done, search=search)

def get_task_by_id(task_id: int):
    return find_by_id(task_id)

class InvalidTaskError(Exception):
    pass

def create_task(data: dict) -> dict:
    title = data.get("title", "").strip()
    if not title:
        raise InvalidTaskError("Title is required")
    return add({"title": title, "done": False})

def update_task_service(task_id: int, updated_task: dict) -> dict | None:
    current = find_by_id(task_id)
    if current is None:
        return None
    title = updated_task.get("title", current["title"])
    if isinstance(title, str):
        title = title.strip()
    done = updated_task.get("done", current["done"])
    return update_task(task_id, {"title": title, "done": done})

def delete_task_service(task_id: int) -> bool:
    return delete_task_repository(task_id)

def get_task_stats() -> dict:
    return count_tasks()
           