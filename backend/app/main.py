from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import upload

app = FastAPI(title=settings.PROJECT_NAME)

# Configuration CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://168.231.77.11:5173",  # VPS Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API ECOBUDGET-CAB"}
