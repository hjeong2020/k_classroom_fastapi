from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model.sql_model import Student
from service.student_service import create_db_and_tables, get_session, StudentService


SessionDep = Annotated[Session, Depends(get_session)]
student_service = StudentService()

app = FastAPI()

origins = [
    "http://localhost:3000/*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/student/")
def create_student(student: Student, session: SessionDep) -> Student:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@app.get("/students/")
def read_students(
    session: SessionDep,
) -> list[Student]:
    students = session.exec(select(Student)).all()
    return students


@app.put("/students/")
def reset_all_class_point(session: SessionDep):
    student = student_service.reset_all_class_point(session)
    return student


@app.get("/students/{student_id}")
def read_student(student_id: int, session: SessionDep) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, session: SessionDep):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"ok": True}


@app.patch("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student, session: SessionDep):
    student_db = session.get(Student, student_id)
    if not student_db:
        raise HTTPException(status_code=404, detail="Student not found")
    student_data = student.model_dump(exclude_unset=True)
    student_db.sqlmodel_update(student_data)
    session.add(student_db)
    session.commit()
    session.refresh(student_db)
    return student_db


@app.put("/students/{student_id}/class/plus", response_model=Student)
def increase_class_point(student_id: int, session: SessionDep):
    student = student_service.increase_class_point(student_id, session)
    return student


@app.put("/students/{student_id}/class/minus", response_model=Student)
def decrease_class_point(student_id: int, session: SessionDep):
    student = student_service.decrease_class_point(student_id, session)
    return student


@app.put("/students/{student_id}/class/reset", response_model=Student)
def reset_class_point(student_id: int, session: SessionDep):
    student = student_service.reset_class_point(student_id, session)
    return student


@app.put("/students/{student_id}/homework/plus", response_model=Student)
def increase_homework_point(student_id: int, session: SessionDep):
    student = student_service.increase_homework_point(student_id, session)
    return student


@app.put("/students/{student_id}/homework/minus", response_model=Student)
def decrease_homework_point(student_id: int, session: SessionDep):
    student = student_service.decrease_homework_point(student_id, session)
    return student
