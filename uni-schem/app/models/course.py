from pydantic import BaseModel, constr

NameStr = constr(max_length=100)
CodeStr = constr(max_length=20)
SemesterStr = constr(max_length=20)

class Course(BaseModel):
    """
    Represents a course taught by a professor.

    Attributes:
        course_id (int): Unique identifier for the course.
        name (str): Full name of the course.
        code (str): Code used to identify the course.
        semester (str): Semester when the course is offered.
        professor_id (int): ID of the assigned professor.
    """
    course_id: int
    name: NameStr
    code: CodeStr
    semester: SemesterStr
    professor_id: int