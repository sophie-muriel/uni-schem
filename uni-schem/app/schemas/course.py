from pydantic import BaseModel, constr

class CourseBase(BaseModel):
    """
    Shared attributes for course models.
    """
    name: constr(max_length=100)
    code: constr(max_length=20)
    semester: constr(max_length=20)
    professor_id: int


class CourseCreate(CourseBase):
    """
    Schema for creating a new course.
    """
    course_id: int


class CourseUpdate(BaseModel):
    """
    Schema for updating a course. All fields are optional.
    """
    name: constr(max_length=100) | None = None
    code: constr(max_length=20) | None = None
    semester: constr(max_length=20) | None = None
    professor_id: int | None = None


class CourseOut(CourseBase):
    """
    Schema for outputting course data.
    """
    course_id: int

    class Config:
        orm_mode = True
