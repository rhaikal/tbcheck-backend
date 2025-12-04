from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .exam import Exam


class ExamNote(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    exam_id: int = Field(foreign_key="exam.id")
    note: str
    created_at: datetime = Field(default_factory=datetime.now)
    exam: Optional["Exam"] = Relationship(
        back_populates="notes",
    )
