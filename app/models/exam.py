from datetime import datetime
from typing import TYPE_CHECKING, Optional
from config import settings

from pydantic import ConfigDict

from sqlalchemy import case
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from .exam_note import ExamNote


class Exam(SQLModel, table=True):
    model_config = ConfigDict(ignored_types=(property, hybrid_property))

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    raw_image_path: str
    processed_image_path: str
    prediction_score: float
    patient_name: str
    patient_age: int
    patient_gender: str
    notes: Optional[list["ExamNote"]] = Relationship(back_populates="exam")
    created_at: datetime = Field(default_factory=datetime.now)

    @hybrid_property
    def status(self) -> int:
        return 1 if self.prediction_score >= settings.detection_threshold else 0

    @status.expression
    def status(cls):
        return case(
            (cls.prediction_score >= settings.detection_threshold, 1),
            else_=0,
        )
