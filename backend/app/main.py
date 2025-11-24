from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze

app = FastAPI(title="ECOBUDGET-CAB API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(analyze.router, tags=["analyze"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API ECOBUDGET-CAB"}
