from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question

router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.get('/list')
def question_list(db: Session = Depends(get_db)) -> list[dict]:
    question_list = (
        db.query(Question)
        .order_by(Question.create_date.desc())
        .all()
    )
    return [
        {
            'id': q.id,
            'subject': q.subject,
            'content': q.content,
            'create_date': q.create_date,
        }
        for q in question_list
    ]

@router.post('/create')
def question_create(
    subject: str,
    content: str,
    db: Session = Depends(get_db),
) -> dict:
    question = Question(
        subject=subject,
        content=content,
        create_date=datetime.utcnow(),
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return {'id': question.id}