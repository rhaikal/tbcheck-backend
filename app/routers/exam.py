from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from config import settings

from app.schemas.pagination import PaginationParams
from app.schemas.exam import ExamFilterParams

from app.dependencies.auth import require_auth
from app.models.user import User

from app.modules.exam import get_exams, get_total_exams, get_exam_by_id

router = APIRouter()


@router.get("/")
async def get_all(
    pagination: Annotated[PaginationParams, Depends()],
    filters: Annotated[ExamFilterParams, Depends()],
    user: Annotated[User, Depends(require_auth)],
    session: AsyncSession = Depends(get_session),
):
    page = pagination.page
    size = pagination.size

    skip = (page - 1) * size if page and size else None
    exams = await get_exams(user, session, skip, size, filters)
    total_exams = await get_total_exams(user, session, filters)
    return {
        "data": exams,
        "metadata": {
            "total_items": total_exams,
            **({"total_pages": (total_exams // size)} if skip else {}),
            **({"current_page": page} if page else {}),
            **({"current_size": size} if size else {}),
        },
    }


@router.get("/summary")
async def get_summary(
    user: Annotated[User, Depends(require_auth)],
    session: AsyncSession = Depends(get_session),
):
    today = date.today()
    total_exams = await get_total_exams(user, session)
    total_today_exams = await get_total_exams(
        user, session, ExamFilterParams(start_date=today, end_date=today)
    )
    total_positive_exams = await get_total_exams(
        user, session, ExamFilterParams(prediction_score=settings.detection_threshold)
    )
    recent_exams = await get_exams(user, session, 0, 5)
    return {
        "total_exams": total_exams,
        "total_today_exams": total_today_exams,
        "total_positive_exams": total_positive_exams,
        "recent_exams": recent_exams,
    }


@router.get("/{exam_id}")
async def get_by_id(
    exam_id: int,
    user: Annotated[User, Depends(require_auth)],
    session: AsyncSession = Depends(get_session),
):
    exam = await get_exam_by_id(exam_id, user, session)
    return exam
