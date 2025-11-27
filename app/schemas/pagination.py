from typing import Optional
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Optional[int] = None
    size: Optional[int] = None
