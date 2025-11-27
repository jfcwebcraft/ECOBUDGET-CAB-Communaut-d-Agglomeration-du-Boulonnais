from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import upload

from app.core.database import engine, Base
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Configuration CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import upload

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
# app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"]) # Commented out for now as we are replacing logic
# app.include_router(lines.router, prefix="/api/v1", tags=["lines"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API ECOBUDGET-CAB"}
