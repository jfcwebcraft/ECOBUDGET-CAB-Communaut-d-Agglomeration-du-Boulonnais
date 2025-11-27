from pydantic import BaseModel
from typing import Optional

class BudgetLineUpdate(BaseModel):
    statut: Optional[str] = None
    rubrique_axe1: Optional[str] = None
    cotation_axe1: Optional[str] = None
    justification_axe1: Optional[str] = None
    rubrique_axe6: Optional[str] = None
    cotation_axe6: Optional[str] = None
    justification_axe6: Optional[str] = None
    commentaire_agent: Optional[str] = None
