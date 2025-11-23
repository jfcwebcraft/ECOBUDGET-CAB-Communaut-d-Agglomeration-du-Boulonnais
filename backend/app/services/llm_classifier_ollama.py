# backend/app/services/llm_classifier_ollama.py
import httpx
import json
import re
from typing import List, Dict

SYSTEM_PROMPT = """Tu es un agent comptable expert du budget vert de la Communauté d'Agglomération du Boulonnais.
Tu appliques strictement la méthodologie nationale 2025 (Ademe/I4CE).

RÈGLES ABSOLUES :
- Tu DOIS traiter CHAQUE ligne fournie en entrée.
- Si tu reçois 5 lignes, tu DOIS renvoyer une liste de 5 objets.
- Doute → budget_vert = false
- Exclure : climatisation, gazon synthétique, véhicules thermiques, éclairage non LED, désherbant, carburant
- N'inclure que les dépenses DIRECTEMENT favorables au climat/biodiversité

Réponds UNIQUEMENT avec une liste JSON valide (pas de texte avant/après) :

[
  {"ligne":"Isolation...","montant_ht":1500,"budget_vert":true,"code_categorie":"V1","confiance":0.9,"explication":"..."},
  {"ligne":"Peinture...","montant_ht":500,"budget_vert":false,"code_categorie":null,"confiance":1.0,"explication":"..."}
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
                    "model": "phi3",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.1,
                        "num_ctx": 2048  # Réduit pour économiser la RAM (8192 -> 2048)
                    }
                }
            )
            if resp.status_code != 200:
                print(f"Erreur HTTP Ollama: {resp.status_code} - {resp.text}")
            
            resp.raise_for_status()
            content = resp.json()["message"]["content"]

            # Nettoyage et extraction flexible du JSON
            # 1. Chercher une liste JSON [...]
            json_match_list = re.search(r'\[.*\]', content, re.DOTALL)
            
            # 2. Chercher un objet JSON unique {...} (si le LLM oublie la liste)
            json_match_obj = re.search(r'\{.*\}', content, re.DOTALL)

            if json_match_list:
                try:
                    result = json.loads(json_match_list.group(0))
                except json.JSONDecodeError:
                    # Fallback si la liste est mal formée, on essaie l'objet
                    if json_match_obj:
                        result = [json.loads(json_match_obj.group(0))]
                    else:
                        raise
            elif json_match_obj:
                # Cas où le LLM renvoie un seul objet au lieu d'une liste
                result = [json.loads(json_match_obj.group(0))]
            else:
                print(f"Réponse Ollama invalide (pas de JSON): {content}")
                raise ValueError("Pas de JSON trouvé")
            
            # S'assurer que c'est bien une liste
            if isinstance(result, dict):
                result = [result]
            
            # Normalisation finale
            for item in result:
                item.setdefault("budget_vert", False)
                item.setdefault("code_categorie", None)
                item.setdefault("confiance", 0.8)
                item.setdefault("explication", "Non classé automatiquement")
            
            return result

        except Exception as e:
            print(f"EXCEPTION CRITIQUE OLLAMA : {str(e)}")
            import traceback
            traceback.print_exc()
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

