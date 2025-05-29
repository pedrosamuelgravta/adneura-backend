from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.models import Brand, User, Audience, StrategicGoal
from tasks.image import image_generation
from celery.result import AsyncResult
from core.celery import celery_app
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routers import *

from core.db import initialize_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting db...")
    initialize_db()
    yield
    print("Stopping db...")


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173",
           "http://localhost:8080", "https://homolog.gravta.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(brand_router, prefix="/api")
app.include_router(audience_router, prefix="/api")
app.include_router(strategic_goal_router, prefix="/api")
app.include_router(trigger_router, prefix="/api")
app.include_router(demographic_router, prefix="/api")
app.include_router(campaign_router, prefix="/api")
app.mount("/images", StaticFiles(directory="images"), name="images")
