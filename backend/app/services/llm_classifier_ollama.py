# backend/app/services/llm_classifier_ollama.py
import httpx
import json
import re
from typing import List, Dict

SYSTEM_PROMPT = """Tu es un agent comptable expert du budget vert de la Communauté d'Agglomération du Boulonnais.
Tu appliques strictement la méthodologie nationale 2025 (Ademe/I4CE).

RÈGLES ABSOLUES :
- Doute → budget_vert = false
- Exclure automatiquement : climatisation, gazon synthétique, véhicules thermiques, éclairage non LED, désherbant, carburant, gasoil
- N'inclure que les dépenses DIRECTEMENT favorables au climat ou à la biodiversité

Réponds EXACTEMENT avec une liste JSON (rien d'autre, pas de ```json, pas de texte avant/après) :

[
  {"ligne":"Isolation toiture 200m²","montant_ht":15420.50,"budget_vert":true,"code_categorie":"V1","confiance":0.98,"explication":"Rénovation thermique"},
  {"ligne":"Climatisation réversible","montant_ht":8900.00,"budget_vert":false,"code_categorie":null,"confiance":1.00,"explication":"Refroidissement actif exclu"}
]
"""

async def classify_lines_with_ollama(lines: List[Dict]) -> List[Dict]:
    if not lines:
        return []

    user_message = "Analyse ces lignes de devis :\n\n"
    for i, line in enumerate(lines, 1):
        user_message += f"{i}. {line['designation']} | {line['montant_ht']} € HT\n"

    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            resp = await client.post(
                "http://ollama:11434/api/chat",  # Port interne Docker (toujours 11434)
                json={
                    "model": "mistral-nemo",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.1,
                        "num_ctx": 8192
                    }
                }
            )
            resp.raise_for_status()
            content = resp.json()["message"]["content"]

            # Nettoyage strict du JSON
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if not json_match:
                raise ValueError("Pas de JSON trouvé")
            
            result = json.loads(json_match.group(0))
            
            # Normalisation finale
            for item in result:
                item.setdefault("budget_vert", False)
                item.setdefault("code_categorie", None)
                item.setdefault("confiance", 0.8)
                item.setdefault("explication", "Non classé automatiquement")
            
            return result

        except Exception as e:
            print(f"Erreur Ollama : {e}")
            # Fallback minimal
            return [
                {
                    "ligne": l["designation"],
                    "montant_ht": l["montant_ht"],
                    "budget_vert": False,
                    "code_categorie": None,
                    "confiance": 0.1,
                    "explication": "Erreur IA – à vérifier manuellement"
                }
                for l in lines
            ]

