from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StudentCreate(BaseModel):
    student_id: str
    name: str
    grades: Optional[dict] = None


class StudentRead(BaseModel):
    id: int
    student_id: str
    name: str
    grades: Optional[dict] = None
    created_at: datetime

    class Config:
        orm_mode = True
