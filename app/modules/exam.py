from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, case

from app.models.user import User
from app.models.exam import Exam
from app.schemas.exam import ExamFilterParams

from config import settings


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


def apply_filters_if_any(query, filters: ExamFilterParams | dict | None = None):
    if not filters:
        return query

    get = (
        filters.get
        if isinstance(filters, dict)
        else lambda k: getattr(filters, k, None)
    )

    prediction_score = get("prediction_score")
    patient_name = get("patient_name")
    start_date = get("start_date")
    end_date = get("end_date")

    if prediction_score:
        query = query.where(Exam.prediction_score >= prediction_score)
    if patient_name:
        query = query.where(Exam.patient_name.ilike(f"%{patient_name}%"))
    if start_date:
        query = query.where(func.date(Exam.created_at) >= start_date)
    if end_date:
        query = query.where(func.date(Exam.created_at) <= end_date)

    return query


async def get_exams(
    user: User,
    session: AsyncSession,
    skip: int = 0,
    limit: int = 0,
    filters: ExamFilterParams = None,
):
    query = (
        select(
            Exam.id,
            Exam.user_id,
            Exam.patient_name,
            Exam.patient_age,
            Exam.prediction_score,
            Exam.created_at,
            case(
                (Exam.prediction_score >= settings.detection_threshold, 1), else_=0
            ).label("status"),
        )
        .where(Exam.user_id == user.id)
        .order_by(Exam.created_at.desc())
    )

    query = apply_filters_if_any(query, filters)

    if skip is not 0 and limit is not 0:
        query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    return result.mappings().all()


async def get_total_exams(
    user: User, session: AsyncSession, filters: ExamFilterParams = None
):
    query = select(func.count(Exam.id)).where(Exam.user_id == user.id)

    query = apply_filters_if_any(query, filters)

    result = await session.execute(query)
    return result.scalar_one()


async def get_exam_by_id(exam_id: int, user: User, session: AsyncSession):
    result = await session.execute(
        select(Exam).where(Exam.user_id == user.id).where(Exam.id == exam_id)
    )
    return result.scalars().first()
