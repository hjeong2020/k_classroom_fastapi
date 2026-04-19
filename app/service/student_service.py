from typing import Union

from sqlmodel import select, Session, SQLModel, create_engine
import logging
import os

from pathlib import Path

from model.sql_model import Student

# Create a Path object for the service file (current script)
script_path = Path(__file__)

# Remove the 'service' subdirectory from the path
database_dir = script_path.parent.parent

# Construct the path to the database file
database_file_path = database_dir / 'database/'

print(f"The path to {database_file_path.name} is: {database_file_path}")
sqlite_file_name = "students.db"

directory = "/Users/hyesunjeong/Documents/projects/k-class-app/k_class_backend/src/database/"

# file_path = os.path.join(directory,fast sqlite_file_name)
file_path = os.path.join(database_file_path, sqlite_file_name)
sqlite_url = f"sqlite:///{file_path}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

class StudentService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def increase_class_point(self, student_id: int, session: Session) -> Union[Student | None]:
        self.logger.info(f"increase_class_point {student_id}")
        student_db = session.get(Student, student_id)
        if not student_db:
            return None
        student_db.class_point = student_db.class_point + 1
        student_db.total_points = student_db.total_points + 1
        session.add(student_db)
        session.commit()
        session.refresh(student_db)
        return student_db


    def decrease_class_point(self, student_id: int, session: Session) -> Union[Student | None]:
        self.logger.info(f"decrease_class_point {student_id}")
        student_db = session.get(Student, student_id)
        if not student_db:
            return None
        student_db.class_point = student_db.class_point - 1
        student_db.total_points = student_db.total_points - 1
        session.add(student_db)
        session.commit()
        session.refresh(student_db)
        return student_db


    def reset_class_point(self, student_id: int, session: Session) -> Union[Student | None]:
        self.logger.info(f"decrease_class_point {student_id}")
        student_db = session.get(Student, student_id)
        if not student_db:
            return None
        student_db.class_point = 0
        session.add(student_db)
        session.commit()
        session.refresh(student_db)
        return student_db


    def increase_homework_point(self, student_id: int, session: Session) -> Union[Student | None]:
        self.logger.info(f"increase_homework_point {student_id}")
        student_db = session.get(Student, student_id)
        if not student_db:
            return None
        student_db.homework_points = student_db.homework_points + 1
        session.add(student_db)
        session.commit()
        session.refresh(student_db)
        return student_db


    def decrease_homework_point(self, student_id: int, session: Session) -> Union[Student | None]:
        self.logger.info(f"decrease_homework_point {student_id}")
        student_db = session.get(Student, student_id)
        if not student_db:
            return None
        student_db.homework_points = student_db.homework_points - 1
        session.add(student_db)
        session.commit()
        session.refresh(student_db)
        return student_db


    def reset_all_class_point(self, session: Session) -> str:
        students = session.exec(select(Student)).all()
        for student_db in students:
            student_db.class_point = 0
            session.add(student_db)
            session.commit()
            session.refresh(student_db)
        print(students)
        return "success"

