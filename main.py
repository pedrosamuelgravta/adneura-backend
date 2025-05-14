from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.models import Brand, User, Audience, StrategicGoal

from api.routers import *

from core.db import initialize_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting db...")
    initialize_db()
    yield
    print("Stopping db...")


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(brand_router)
app.include_router(audience_router)
