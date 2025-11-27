import pandas as pd
import httpx
import os
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import BudgetLine
from app.core.database import SessionLocal

SYSTEM_PROMPT = """Tu es un expert finances publiques. Analyse cette dépense pour le Budget Vert. 
Si le libellé est vague, classe en 'A_APPROFONDIR' et pose une question dans le champ justification.

Tu dois renvoyer un objet JSON unique contenant :
- rubrique_axe1 (string | null)
- cotation_axe1 ('FAVORABLE', 'DEFAVORABLE', 'NEUTRE', 'A_APPROFONDIR')
- justification_axe1 (string)
- rubrique_axe6 (string | null)
- cotation_axe6 ('FAVORABLE', 'DEFAVORABLE', 'NEUTRE', 'A_APPROFONDIR')
- justification_axe6 (string)

RÈGLES :
- Traite CHAQUE ligne
- Doute -> A_APPROFONDIR
- Contrainte : réponds uniquement par un objet JSON (strict) sans autre texte.
"""

def save_to_db(data: List[Dict[str, Any]]):
    db: Session = SessionLocal()
    try:
        for item in data:
            # Check if exists (upsert logic or just skip)
            # For simplicity, we'll try to merge or add. 
            # Since primary key is composite (exercice, bordereau, piece), we can use merge.
            
            db_item = BudgetLine(**item)
            db.merge(db_item)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

import io

async def process_upload(file_content: bytes, filename: str) -> List[Dict[str, Any]]:
    # 1. Read Excel
    try:
        df = pd.read_excel(io.BytesIO(file_content))
    except Exception:
        try:
            df = pd.read_csv(io.BytesIO(file_content))
        except:
            raise ValueError("Format de fichier non supporté. Utilisez Excel (.xlsx) ou CSV.")

    results = []
    
    # Ollama Client
    ollama_url = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for index, row in df.iterrows():
            item = {
                "exercice": int(row.get("Exercice", 2024)),
                "num_bordereau": int(row.get("N° Bordereau", 0)),
                "num_piece": int(row.get("N° Pièce", 0)),
                "libelle": str(row.get("Libellé", "")),
                "montant_ht": float(row.get("Montant HT", 0)),
                "montant_tva": float(row.get("Montant TVA", 0)),
                "montant_ttc": float(row.get("Montant TTC", 0)),
                "tiers": str(row.get("Tiers", "")),
                "nature": str(row.get("Nature", "")),
                "fonction": str(row.get("Fonction", "")),
                "operation": str(row.get("Opération", "")),
                "service": str(row.get("Service", "")),
                "gestionnaire": str(row.get("Gestionnaire", "")),
                "statut": "A_TRAITER",
                "commentaire_agent": ""
            }

            # 2. Filter Rule
            nature = item["nature"]
            if nature.startswith("64") or nature.startswith("66"):
                item["cotation_axe1"] = "NEUTRE"
                item["rubrique_axe1"] = "Personnel/Financier"
                item["justification_axe1"] = "Dépense neutre par nature (M57)"
                item["cotation_axe6"] = "NEUTRE"
                item["rubrique_axe6"] = "Personnel/Financier"
                item["justification_axe6"] = "Dépense neutre par nature (M57)"
                item["statut"] = "VALIDE"
            else:
                # 3. AI Call
                user_message = f"Analyse cette dépense : Libellé='{item['libelle']}', Tiers='{item['tiers']}', Montant='{item['montant_ht']}', Fonction='{item['fonction']}'"
                
                try:
                    resp = await client.post(
                        f"{ollama_url}/api/chat",
                        json={
                            "model": "mistral",
                            "messages": [
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": user_message}
                            ],
                            "stream": False,
                            "format": "json",
                            "options": {"temperature": 0.1}
                        }
                    )
                    resp.raise_for_status()
                    content = resp.json()["message"]["content"]
                    
                    # Parse JSON
                    ai_data = json.loads(content)
                    item["rubrique_axe1"] = ai_data.get("rubrique_axe1")
                    item["cotation_axe1"] = ai_data.get("cotation_axe1", "A_APPROFONDIR")
                    item["justification_axe1"] = ai_data.get("justification_axe1")
                    item["rubrique_axe6"] = ai_data.get("rubrique_axe6")
                    item["cotation_axe6"] = ai_data.get("cotation_axe6", "A_APPROFONDIR")
                    item["justification_axe6"] = ai_data.get("justification_axe6")
                    
                    if item["cotation_axe1"] == "A_APPROFONDIR" or item["cotation_axe6"] == "A_APPROFONDIR":
                        item["statut"] = "A_APPROFONDIR"
                    else:
                        item["statut"] = "A_TRAITER"
                        
                except Exception as e:
                    print(f"Ollama Error: {e}")
                    # Mock AI Fallback
                    item["statut"] = "A_TRAITER"
                    item["commentaire_agent"] = "Analyse IA échouée (Mock appliqué)"
                    item["cotation_axe1"] = "NEUTRE"
                    item["justification_axe1"] = "Mock: Analyse non disponible"
                    item["cotation_axe6"] = "NEUTRE"
                    item["justification_axe6"] = "Mock: Analyse non disponible"

            results.append(item)
            
    # Save to DB
    save_to_db(results)
            
    return results
