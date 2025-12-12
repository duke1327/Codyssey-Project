from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question as QuestionModel
from domain.question.schemas import QuestionCreate, Question

router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.get('/list', response_model=list[Question])
def question_list(db: Session = Depends(get_db)) -> list[QuestionModel]:
    question_list = (
        db.query(QuestionModel)
        .order_by(QuestionModel.create_date.desc())
        .all()
    )
    return question_list


@router.post('/create', response_model=Question)
def question_create(
    question_in: QuestionCreate,
    db: Session = Depends(get_db),
) -> QuestionModel:
    question = QuestionModel(
        subject=question_in.subject,
        content=question_in.content,
        create_date=datetime.utcnow(),
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question
