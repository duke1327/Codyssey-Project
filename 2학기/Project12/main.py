# main.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from database import Base, engine
from models import Question
from domain.question.question_router import router as question_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 앱 시작 시 테이블 생성 (alembic 사용 전까지 임시용)
Base.metadata.create_all(bind=engine)

app.include_router(question_router)

app.mount('/', StaticFiles(directory='frontend', html=True), name='frontend')
