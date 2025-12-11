from fastapi import APIRouter, FastAPI
from typing import Dict, List
import csv
import os

CSV_FILE_PATH = 'todo.csv'
todo_list: List[Dict] = []

router = APIRouter()


def load_todo_list() -> None:
    """Load todo_items from CSV file into todo_list."""
    if not os.path.exists(CSV_FILE_PATH):
        return

    with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        items: List[Dict] = []
        for row in reader:
            items.append({'title': row.get('title', ''), 'description': row.get('description', '')})
        todo_list.clear()
        todo_list.extend(items)


def save_todo_list() -> None:
    """Save todo_list items into CSV file."""
    fieldnames = ['title', 'description']

    with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in todo_list:
            writer.writerow(
                {
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                },
            )


@router.post('/add_todo')
async def add_todo(item: Dict) -> Dict:
    """
    Add a new todo_item.

    If the given item dict is empty, return a warning message.
    """
    if not item:
        return {'success': False, 'message': '입력 데이터가 비어 있습니다.'}

    todo_list.append(item)
    save_todo_list()
    return {'success': True, 'item': item}


@router.get('/retrieve_todo')
async def retrieve_todo() -> Dict:
    """Retrieve todo_list items."""
    load_todo_list()
    return {'success': True, 'items': todo_list}


app = FastAPI()
app.include_router(router)
