import os
from fastapi import FastAPI
from app.db.database import engine, Base
import app.models.day
import app.models.availability
import app.models.classroom
import app.models.course
import app.models.professor
import app.models.schedule
import app.models.student
import app.models.student_course

Base.metadata.create_all(bind=engine)

from app.api.v1 import (
    availability_routes,
    classroom_routes,
    course_routes,
    professor_routes,
    schedule_routes,
    student_course_routes,
    student_routes,
)

app = FastAPI(
    title="Uni-ScheM",
    description="University Schedule Manager",
    contact={
        "name": "Sophie Muriel",
        "url": "https://github.com/sophie-muriel/uni-schem",
    },
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "persistAuthorization": True,
    },
)

app.include_router(availability_routes.router,    prefix="/availability",  tags=["Availability"])
app.include_router(classroom_routes.router,       prefix="/classroom",     tags=["Classroom"])
app.include_router(course_routes.router,          prefix="/course",        tags=["Course"])
app.include_router(professor_routes.router,       prefix="/professor",     tags=["Professor"])
app.include_router(schedule_routes.router,        prefix="/schedule",      tags=["Schedule"])
app.include_router(student_course_routes.router,  prefix="/student-course",tags=["Student - Course"])
app.include_router(student_routes.router,         prefix="/student",       tags=["Student"])
