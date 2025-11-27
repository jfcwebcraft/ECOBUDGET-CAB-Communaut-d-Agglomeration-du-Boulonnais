from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.ingestion_service import process_upload
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import BudgetLine

router = APIRouter()

@router.post("/upload", response_model=List[Dict[str, Any]])
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Format de fichier invalide. Veuillez uploader un fichier Excel ou CSV.")
    
    content = await file.read()
    try:
        results = await process_upload(content, file.filename)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/budget-lines", response_model=List[Dict[str, Any]])
def get_budget_lines(db: Session = Depends(get_db)):
    budget_lines = db.query(BudgetLine).all()
    return [
        {
            "exercice": line.exercice,
            "num_bordereau": line.num_bordereau,
            "num_piece": line.num_piece,
            "libelle": line.libelle,
            "montant_ht": line.montant_ht,
            "montant_tva": line.montant_tva,
            "montant_ttc": line.montant_ttc,
            "tiers": line.tiers,
            "nature": line.nature,
            "fonction": line.fonction,
            "operation": line.operation,
            "service": line.service,
            "gestionnaire": line.gestionnaire,
            "rubrique_axe1": line.rubrique_axe1,
            "cotation_axe1": line.cotation_axe1,
            "justification_axe1": line.justification_axe1,
            "rubrique_axe6": line.rubrique_axe6,
            "cotation_axe6": line.cotation_axe6,
            "justification_axe6": line.justification_axe6,
            "statut": line.statut,
            "commentaire_agent": line.commentaire_agent
        }
        for line in budget_lines
    ]

from app.schemas import BudgetLineUpdate

@router.put("/budget-lines/{exercice}/{num_bordereau}/{num_piece}", response_model=Dict[str, Any])
def update_budget_line(
    exercice: int,
    num_bordereau: int,
    num_piece: int,
    update_data: BudgetLineUpdate,
    db: Session = Depends(get_db)
):
    db_line = db.query(BudgetLine).filter(
        BudgetLine.exercice == exercice,
        BudgetLine.num_bordereau == num_bordereau,
        BudgetLine.num_piece == num_piece
    ).first()

    if not db_line:
        raise HTTPException(status_code=404, detail="Ligne budgétaire non trouvée")

    # Update fields if provided
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_line, key, value)

    db.commit()
    db.refresh(db_line)

    return {
        "exercice": db_line.exercice,
        "num_bordereau": db_line.num_bordereau,
        "num_piece": db_line.num_piece,
        "statut": db_line.statut,
        "commentaire_agent": db_line.commentaire_agent,
        "rubrique_axe1": db_line.rubrique_axe1,
        "cotation_axe1": db_line.cotation_axe1,
        "justification_axe1": db_line.justification_axe1,
        "rubrique_axe6": db_line.rubrique_axe6,
        "cotation_axe6": db_line.cotation_axe6,
        "justification_axe6": db_line.justification_axe6,
    }
