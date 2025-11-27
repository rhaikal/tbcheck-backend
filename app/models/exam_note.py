from datetime import datetime

from sqlmodel import Field, SQLModel


class ExamNote(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    exam_id: int = Field(foreign_key="exam.id")
    note: str
    created_at: datetime = Field(default_factory=datetime.now)
