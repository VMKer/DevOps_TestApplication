from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentRead

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)) -> StudentRead:
    student = Student(
        student_id=payload.student_id,
        name=payload.name,
        grades=payload.grades,
    )
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="student_id already exists",
        )
    db.refresh(student)
    return student


@router.get("", response_model=List[StudentRead])
def list_students(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> List[StudentRead]:
    result = db.execute(select(Student).offset(offset).limit(limit))
    return list(result.scalars().all())


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: str, db: Session = Depends(get_db)) -> StudentRead:
    result = db.execute(select(Student).where(Student.student_id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str, db: Session = Depends(get_db)) -> Response:
    result = db.execute(select(Student).where(Student.student_id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
