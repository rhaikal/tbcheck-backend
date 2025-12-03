from typing import Annotated, Optional
from pydantic import BaseModel, StringConstraints
from datetime import date

GENDER_FIELD = Annotated[
    str,
    StringConstraints(pattern=r"^(male|female)$"),
]


class ExamPatient(BaseModel):
    name: str
    age: int
    gender: GENDER_FIELD


class ExamSave(ExamPatient):
    inference_id: str
    notes: Optional[list[str]] = None


class ExamFilterParams(BaseModel):
    prediction_score: Optional[float] = None
    patient_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
