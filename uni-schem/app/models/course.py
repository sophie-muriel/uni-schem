from pydantic import BaseModel, constr


class Course(BaseModel):
    """
    Represents a course taught by a professor.

    Attributes:
        course_id (int): Unique identifier for the course.
        name (str): Full name of the course.
        code (str): Code used to identify the course.
        semester (str): Semester when the course is offered.
        professor_id (int): The ID of the professor assigned to the course.
    """

    course_id: int
    name: constr(max_length=100)
    code: constr(max_length=20)
    semester: constr(max_length=20)
    professor_id: int
