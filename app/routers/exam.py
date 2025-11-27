from typing import Annotated
from fastapi import APIRouter, Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session

from app.schemas.pagination import PaginationParams

from app.dependencies.auth import require_auth
from app.models.user import User

from app.modules.exam import get_exams, get_total_exams

router = APIRouter()


@router.get("/")
async def get_all(
    pagination: Annotated[PaginationParams, Depends()],
    user: Annotated[User, Depends(require_auth)],
    session: AsyncSession = Depends(get_session),
):
    page = pagination.page
    size = pagination.size

    skip = (page - 1) * size if page and size else None
    exams = await get_exams(user, session, skip, size)
    total_exams = await get_total_exams(user, session)
    return {
        "data": exams,
        "metadata": {
            "total_items": total_exams,
            **({"total_pages": (total_exams // size)} if skip else {}),
            **({"current_page": page} if page else {}),
            **({"current_size": size} if size else {}),
        },
    }
