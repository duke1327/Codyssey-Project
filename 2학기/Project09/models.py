from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database import Base

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
