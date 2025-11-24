from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_extractor import extract_lines_from_pdf
from app.services.llm_classifier_ollama import classify_lines_with_ollama
import shutil
import os

router = APIRouter()

@router.post("/analyze")
async def analyze_invoice(file: UploadFile = File(...)):
    # Sauvegarder le fichier temporairement
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extraction des données
    try:
        lines = extract_lines_from_pdf(temp_file)
    except Exception as e:
        os.remove(temp_file)
        raise HTTPException(status_code=400, detail=f"Erreur extraction PDF: {str(e)}")
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Classification IA
    classification_response = await classify_lines_with_ollama(lines)
    
    # Gestion de la compatibilité (si l'ancien format liste est retourné par erreur)
    if isinstance(classification_response, list):
        classified_lines = classification_response
        metadata = {"model": "unknown", "duration": 0}
    else:
        classified_lines = classification_response.get("results", [])
        metadata = classification_response.get("metadata", {})

    # Calcul des totaux
    total_ht = sum(l.get("montant_ht", 0) or 0 for l in classified_lines)
    total_vert = sum(l.get("montant_ht", 0) or 0 for l in classified_lines if l.get("budget_vert"))
    part_verte = (total_vert / total_ht * 100) if total_ht > 0 else 0

    return {
        "filename": file.filename,
        "total_ht": round(total_ht, 2),
        "total_vert": round(total_vert, 2),
        "part_verte": round(part_verte, 1),
        "lines": classified_lines,
        "metadata": metadata
    }
