from pydantic import BaseModel


class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    is_done: bool


class TodoUpdate(BaseModel):
    title: str
    description: str
    is_done: bool
