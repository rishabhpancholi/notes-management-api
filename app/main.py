import asyncio

from typing import AsyncIterator

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.utils import utils
from app.database.connection import engine
from app.api.auth_routes import auth_router
from app.api.crud_routes import crud_router
from app.utils.exceptions import register_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncIterator[None]:
    await asyncio.sleep(5)
    await utils.init_db(engine)

    yield

app = FastAPI(lifespan = lifespan)

app.include_router(auth_router)
app.include_router(crud_router)
    
@app.get("/")
def hello():
    return {"message": "Welcome to the API!"}

@app.get("/health")
def health():
    return {"message": "Healthy"}

register_exception_handler(app)