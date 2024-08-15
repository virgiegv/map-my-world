from fastapi import FastAPI

from src.db import models
from src.location_and_categories import router as location_category_router
from src.reviews import router as reviews_router
from src.db.database import engine

app = FastAPI()

#TO DO: look up how to do this with Alembic and apply migrations
models.Base.metadata.create_all(bind=engine)

app.include_router(location_category_router.router)
app.include_router(reviews_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
