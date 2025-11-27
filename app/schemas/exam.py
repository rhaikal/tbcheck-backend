from typing import Annotated, Optional
from pydantic import BaseModel, StringConstraints

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
