from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship

from app.models.exam_note import ExamNote


class Exam(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    raw_image_path: str
    processed_image_path: str
    prediction_score: float
    patient_name: str
    patient_age: int
    patient_gender: str
    notes: list["ExamNote"] = Relationship()
    created_at: datetime = Field(default_factory=datetime.now)
