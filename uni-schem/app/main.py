# main.py
from fastapi import FastAPI
from api.v1 import item_routes

app = FastAPI(
    title="Uni-ScheM",
    description="University Schedule Manager",
    contact={
        "name": "Sophie Muriel",
        "url": "https://github.com/sophie-muriel"
    }
)

app.include_router(item_routes.router, prefix="/api/v1/item")