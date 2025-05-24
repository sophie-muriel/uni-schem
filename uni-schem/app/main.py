"""
Main application entry point for Uni-ScheM.

This module sets up the FastAPI app instance, includes all route modules, 
and initializes the database metadata using SQLAlchemy.

Routes included:
    - Availability
    - Classroom
    - Course
    - Professor
    - Schedule
    - Student-Course relationships
    - Student

App Metadata:
    - Title: Uni-ScheM
    - Description: University Schedule Manager
    - Contact: Sophie Muriel (https://github.com/sophie-muriel/uni-schem)
"""
from app.api.v1 import (availability_routes, classroom_routes, course_routes,
                        professor_routes, schedule_routes,
                        student_course_routes, student_routes)
from app.db.database import Base, engine
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)


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

app.include_router(availability_routes.router,
                   prefix="/availability",  tags=["Availability"])
app.include_router(classroom_routes.router,
                   prefix="/classroom",     tags=["Classroom"])
app.include_router(course_routes.router,
                   prefix="/course",        tags=["Course"])
app.include_router(professor_routes.router,
                   prefix="/professor",     tags=["Professor"])
app.include_router(schedule_routes.router,
                   prefix="/schedule",      tags=["Schedule"])
app.include_router(student_course_routes.router,
                   prefix="/student-course", tags=["Student - Course"])
app.include_router(student_routes.router,
                   prefix="/student",       tags=["Student"])
