from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.exam import Exam


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
