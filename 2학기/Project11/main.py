from fastapi import FastAPI

from database import Base, engine
from models import Question
from domain.question.question_router import router as question_router

app = FastAPI()

# 앱 시작 시 테이블 생성 (alembic 사용 전까지 임시용)
Base.metadata.create_all(bind=engine)

app.include_router(question_router)


@app.get('/')
def read_root() -> dict:
    return {'message': 'Hello Mars Board'}
