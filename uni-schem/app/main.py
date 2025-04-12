# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from app.api.v1 import item_routes

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://user:password@mysql:3306/mydatabase"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="Uni-ScheM",
    description="University Schedule Manager",
    contact={
        "name": "Sophie Muriel",
        "url": "https://github.com/sophie-muriel/uni-schem"
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

app.include_router(item_routes.router, prefix="/api/v1/item")