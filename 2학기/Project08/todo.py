import csv
from typing import List, Dict, Optional

from fastapi import APIRouter, HTTPException

from model import TodoItem, TodoUpdate


todo_router = APIRouter(
    prefix='/todos',
    tags=['todos'],
)

CSV_FILE = 'todos.csv'
FIELDNAMES = ['id', 'title', 'description', 'is_done']


def read_all_todos() -> List[Dict[str, str]]:
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=FIELDNAMES)
        next(reader, None)  # 헤더 스킵
        return list(reader)


def write_all_todos(rows: List[Dict[str, str]]) -> None:
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def get_todo_by_id(todo_id: int) -> Optional[Dict[str, str]]:
    todos = read_all_todos()
    for row in todos:
        if int(row['id']) == todo_id:
            return row
    return None


def update_todo_in_csv(todo_id: int, data: Dict[str, str]) -> Optional[Dict[str, str]]:
    todos = read_all_todos()
    updated = None

    for index, row in enumerate(todos):
        if int(row['id']) == todo_id:
            todos[index] = data
            updated = todos[index]
            break

    if updated is None:
        return None

    write_all_todos(todos)
    return updated


def delete_todo_in_csv(todo_id: int) -> bool:
    todos = read_all_todos()
    new_todos = [row for row in todos if int(row['id']) != todo_id]

    if len(new_todos) == len(todos):
        return False

    write_all_todos(new_todos)
    return True


@todo_router.get('/{todo_id}', response_model=TodoItem)
def get_single_todo(todo_id: int) -> TodoItem:
    row = get_todo_by_id(todo_id)
    if row is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    return TodoItem(
        id=int(row['id']),
        title=row['title'],
        description=row['description'],
        is_done=row['is_done'].lower() == 'true',
    )


@todo_router.put('/{todo_id}', response_model=TodoItem)
def update_todo(todo_id: int, todo_update: TodoUpdate) -> TodoItem:
    data = {
        'id': str(todo_id),
        'title': todo_update.title,
        'description': todo_update.description,
        'is_done': 'true' if todo_update.is_done else 'false',
    }

    updated = update_todo_in_csv(todo_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    return TodoItem(
        id=int(updated['id']),
        title=updated['title'],
        description=updated['description'],
        is_done=updated['is_done'].lower() == 'true',
    )


@todo_router.delete('/{todo_id}')
def delete_single_todo(todo_id: int) -> dict:
    deleted = delete_todo_in_csv(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Todo not found')

    return {'message': 'Todo deleted'}
