import datetime

from pydantic import BaseModel, field_validator


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return value


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True
