from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.models.exam import Exam
from sqlalchemy import func


async def save_exam(exam_data, user: User, inference_store, session: AsyncSession):
    exam = Exam(
        user_id=user.id,
        raw_image_path=inference_store["raw_image"],
        processed_image_path=inference_store["processed_image"],
        prediction_score=inference_store["prediction_score"],
        patient_name=exam_data.name,
        patient_age=exam_data.age,
        patient_gender=exam_data.gender,
    )
    session.add(exam)
    await session.commit()
    await session.refresh(exam)
    return exam


async def get_exams(user: User, session: AsyncSession, skip: int = 0, limit: int = 0):
    query = (
        select(
            Exam.id,
            Exam.user_id,
            Exam.patient_name,
            Exam.prediction_score,
            Exam.created_at,
        )
        .where(Exam.user_id == user.id)
        .order_by(Exam.created_at.desc())
    )

    if skip is not 0 and limit is not 0:
        query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    return result.mappings().all()


async def get_total_exams(user: User, session: AsyncSession):
    result = await session.execute(
        select(func.count(Exam.id)).where(Exam.user_id == user.id)
    )
    return result.scalar_one()


async def get_exam_by_id(exam_id: int, user: User, session: AsyncSession):
    result = await session.execute(
        select(Exam).where(Exam.user_id == user.id).where(Exam.id == exam_id)
    )
    return result.scalars().first()
