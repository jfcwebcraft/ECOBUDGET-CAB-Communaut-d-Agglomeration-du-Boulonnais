import httpx
import json
import re
import traceback
from typing import List, Dict

SYSTEM_PROMPT = """Tu es un expert en classification "Budget Vert" pour une collectivité.
Analyse chaque ligne et attribue :
1. budget_vert (true/false)
2. axe (Axe 1 à 6)
3. code_categorie (Axxx)

AXES :
- Axe 1 : Atténuation climat (Isolation, Solaire, Véhicule électrique)
- Axe 2 : Adaptation climat (Végétalisation, Eau)
- Axe 3 : Eau (Récupération, Assainissement)
- Axe 4 : Économie circulaire (Compost, Réemploi)
- Axe 5 : Pollution (LED, Air)
- Axe 6 : Biodiversité (Plantation, Espaces verts)

CODES (Investissements Verts uniquement) :
- A125 : Constructions (Isolation, Rénovation thermique)
- A140 : Installations techniques (Panneaux solaires, LED, Composteur)
- A150 : Autres investissements (Plantation, Véhicules électriques)

RÈGLES :
- Tu DOIS traiter CHAQUE ligne
- Doute → budget_vert = false
- EXCLURE : climatisation, gazon synthétique, véhicule thermique, désherbant
- N'inclure que les dépenses DIRECTEMENT favorables climat/biodiversité

Réponds UNIQUEMENT JSON :

[
  {"ligne":"Isolation...","montant_ht":1500,"budget_vert":true,"axe":"Axe 1","code_categorie":"A125","confiance":0.9,"explication":"Rénovation thermique"},
  {"ligne":"Peinture...","montant_ht":500,"budget_vert":false,"axe":null,"code_categorie":null,"confiance":1.0,"explication":"Entretien standard"}
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
                        "num_ctx": 2048
                    }
                }
            )
            if resp.status_code != 200:
                print(f"Erreur HTTP Ollama: {resp.status_code} - {resp.text}")
            
            resp.raise_for_status()
            content = resp.json()["message"]["content"]

            # Nettoyage et extraction flexible du JSON
            json_match_list = re.search(r'\[.*\]', content, re.DOTALL)
            json_match_obj = re.search(r'\{.*\}', content, re.DOTALL)

            if json_match_list:
                try:
                    result = json.loads(json_match_list.group(0))
                except json.JSONDecodeError:
                    if json_match_obj:
                        result = [json.loads(json_match_obj.group(0))]
                    else:
                        raise
            elif json_match_obj:
                result = [json.loads(json_match_obj.group(0))]
            else:
                print(f"Réponse Ollama invalide (pas de JSON): {content}")
                raise ValueError("Pas de JSON trouvé")
            
            if isinstance(result, dict):
                result = [result]
            
            # Normalisation finale
            for item in result:
                item.setdefault("budget_vert", False)
                item.setdefault("code_categorie", None)
                item.setdefault("axe", None)
                item.setdefault("confiance", 0.8)
                item.setdefault("explication", "Non classé automatiquement")
            
            return result

        except Exception as e:
            print(f"EXCEPTION CRITIQUE OLLAMA : {str(e)}")
            traceback.print_exc()
            return [
                {
                    "ligne": l["designation"],
                    "montant_ht": l["montant_ht"],
                    "budget_vert": False,
                    "code_categorie": None,
                    "axe": None,
                    "confiance": 0.1,
                    "explication": "Erreur IA – à vérifier manuellement"
                }
                for l in lines
            ]
