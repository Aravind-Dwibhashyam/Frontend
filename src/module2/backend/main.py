from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.client import connect_to_mongo, close_mongo_connection
from db.init import init_indexes
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions — wrapped so server starts even if DB is slow
    try:
        await connect_to_mongo()
        await init_indexes()
    except Exception as e:
        print(f"WARNING: Startup DB init failed: {e}")
        print("Server will start anyway — DB will connect on first request")
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

from routes import patients, diseases, diagnoses, metrics, episodes, risks, plans, adherence, integrations, demographics
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
app.include_router(demographics.router)

@app.get("/")
async def root():
    return {"message": "Welcome to ChronicCare Module 2 API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
