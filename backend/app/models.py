from sqlalchemy import Column, Integer, String, Float, Numeric
from app.core.database import Base

class BudgetLine(Base):
    __tablename__ = "budget_lines"

    # Composite Primary Key
    exercice = Column(Integer, primary_key=True, index=True)
    num_bordereau = Column(Integer, primary_key=True, index=True)
    num_piece = Column(Integer, primary_key=True, index=True)

    libelle = Column(String, nullable=True)
    montant_ht = Column(Float, nullable=True) # Using Float for SQLite simplicity, Numeric is better for Postgres
    montant_tva = Column(Float, nullable=True)
    montant_ttc = Column(Float, nullable=True)
    tiers = Column(String, nullable=True)
    nature = Column(String, nullable=True)
    fonction = Column(String, nullable=True)
    operation = Column(String, nullable=True)
    service = Column(String, nullable=True)
    gestionnaire = Column(String, nullable=True)

    rubrique_axe1 = Column(String, nullable=True)
    cotation_axe1 = Column(String, nullable=True)
    justification_axe1 = Column(String, nullable=True)

    rubrique_axe6 = Column(String, nullable=True)
    cotation_axe6 = Column(String, nullable=True)
    justification_axe6 = Column(String, nullable=True)

    statut = Column(String, default="A_TRAITER")
    commentaire_agent = Column(String, nullable=True)
