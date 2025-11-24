# backend/app/services/pdf_extractor.py
import pdfplumber
import re
from typing import List, Dict, Tuple, Optional

def clean_amount(text: str) -> Optional[float]:
    """Extrait un montant HT depuis du texte brut"""
    if not text:
        return None
    # Recherche nombres avec espaces, virgules, points
    match = re.search(r'[\d\s\.,]+', text.replace(' ', ''))
    if not match:
        return None
    amount_str = match.group(0).replace(',', '.').replace(' ', '')
    try:
        return round(float(amount_str), 2)
    except:
        return None

def extract_lines_from_pdf(filepath: str) -> List[Dict[str, any]]:
    """Extrait les lignes de devis avec designation + montant HT"""
    lines = []

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            # 1. Essai avec les tableaux (90 % des devis)
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 2:
                        continue
                    # Recherche du montant dans les dernières colonnes
                    amount = None
                    designation = ""
                    for cell in reversed(row):
                        if not cell:
                            continue
                        cell = cell.replace('\n', ' ').strip()
                        potential_amount = clean_amount(cell)
                        if potential_amount and potential_amount > 10:  # filtre petits montants
                            amount = potential_amount
                            designation = " ".join([c for c in row if c and c != cell][:4])
                            break
                    if amount and designation:
                        # Filtrer les lignes de totaux
                        designation_lower = designation.lower()
                        if any(keyword in designation_lower for keyword in ['total', 'sous-total', 'subtotal', 'montant total', 'ttc', 'tva']):
                            continue
                        
                        lines.append({
                            "designation": designation.strip()[:200],
                            "montant_ht": amount
                        })

            # 2. Fallback texte brut si pas de tableau
            if not lines:
                text = page.extract_text()
                if text:
                    for line in text.split('\n'):
                        if any(kw in line.lower() for kw in ['ht', '€', 'eur', 'total']):
                            amount = clean_amount(line)
                            if amount and amount > 50:
                                clean_line = re.sub(r'[\d\.,\s€]+', '', line)[:150]
                                # Filtrer les lignes de totaux
                                if any(keyword in clean_line.lower() for keyword in ['total', 'sous-total', 'subtotal', 'montant total', 'ttc', 'tva']):
                                    continue
                                
                                lines.append({
                                    "designation": clean_line.strip(),
                                    "montant_ht": amount
                                })

    # Déduplication basique
    seen = set()
    unique_lines = []
    for l in lines:
        key = (l["designation"][:50], l["montant_ht"])
        if key not in seen:
            seen.add(key)
            unique_lines.append(l)

    return unique_lines[:40]  # limite raisonnable pour Ollama

