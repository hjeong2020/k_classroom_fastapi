from sqlmodel import Field, SQLModel


class StudentBase(SQLModel):
    name: str = Field(index=True)
    english_name: str = Field(index=True)
    icon: str = Field(default=None)
    class_point: int = Field(default=0)
    total_points: int = Field(default=0)
    homework_points: int = Field(default=0)


class Student(StudentBase, table=True):
    id: int = Field(default=None, primary_key=True)


