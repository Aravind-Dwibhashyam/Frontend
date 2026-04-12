from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.client import connect_to_mongo, close_mongo_connection
from db.init import init_indexes
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    await connect_to_mongo()
    await init_indexes()
    yield
    # Shutdown actions
    await close_mongo_connection()

app = FastAPI(title="Module 2: Chronic Disease Management", lifespan=lifespan)

# Allow React Dev Server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real app, limit this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import patients, diseases, diagnoses, metrics, episodes, risks, plans, adherence, integrations
from middleware.error_handler import custom_error_handler
from starlette.middleware.base import BaseHTTPMiddleware

# ...

app.add_middleware(BaseHTTPMiddleware, dispatch=custom_error_handler)

app.include_router(patients.router)
app.include_router(diseases.router)
app.include_router(diagnoses.router)
app.include_router(metrics.router)
app.include_router(episodes.router)
app.include_router(risks.router)
app.include_router(plans.router)
app.include_router(adherence.router)
app.include_router(integrations.router)

@app.get("/")
async def root():
    return {"message": "Welcome to ChronicCare Module 2 API"}

