from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.services.pdf_extractor import extract_lines_from_pdf
from app.services.llm_classifier_ollama import classify_lines_with_ollama

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze")
async def analyze_devis(file: UploadFile = File(...)):
    """Extrait + Classifie un devis PDF en une seule requête"""
    try:
        # 1. Sauvegarder le fichier
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        # 2. Extraire les lignes
        lines = extract_lines_from_pdf(file_location)
        
        if not lines:
            return {
                "status": "warning",
                "message": "Aucune ligne extraite du PDF",
                "lignes": [],
                "total_ht": 0.0,
                "total_budget_vert": 0.0
            }
        
        # 3. Classifier avec Ollama
        classified_lines = await classify_lines_with_ollama(lines)
        
        # 4. Calculer les totaux
        total_ht = sum(l["montant_ht"] for l in classified_lines)
        total_budget_vert = sum(
            l["montant_ht"] for l in classified_lines if l.get("budget_vert", False)
        )
        
        return {
            "status": "success",
            "filename": file.filename,
            "lignes": classified_lines,
            "total_ht": round(total_ht, 2),
            "total_budget_vert": round(total_budget_vert, 2),
            "pourcentage_budget_vert": round((total_budget_vert / total_ht * 100) if total_ht > 0 else 0, 1)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse : {str(e)}")
