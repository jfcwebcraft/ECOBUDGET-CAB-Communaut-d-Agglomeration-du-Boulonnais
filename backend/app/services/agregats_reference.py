import json
import os
from typing import Dict

# Charger la référence des agrégats
AGREGATS_FILE = os.path.join(os.path.dirname(__file__), "../data/agregats_reference.json")

def get_agregats_reference() -> Dict:
    """Retourne la liste complète des agrégats avec leurs libellés"""
    try:
        with open(AGREGATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ATTENTION: Fichier de référence des agrégats introuvable: {AGREGATS_FILE}")
        return {}
    except json.JSONDecodeError as e:
        print(f"ERREUR: Impossible de lire le fichier JSON des agrégats: {e}")
        return {}
