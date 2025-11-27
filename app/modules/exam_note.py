from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import insert

from app.models.exam import Exam
from app.models.exam_note import ExamNote


async def save_exam_notes(exam: Exam, notes: list, session: AsyncSession):
    params = [
        {
            "exam_id": exam.id,
            "note": note,
        }
        for note in notes
    ]

    await session.execute(insert(ExamNote), params=params)
    await session.commit()
    return notes
