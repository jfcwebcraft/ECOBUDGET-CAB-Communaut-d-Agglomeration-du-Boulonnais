import httpx
import json
import re
import traceback
from typing import List, Dict

SYSTEM_PROMPT = """Tu es un expert en classification "Budget Vert" pour une collectivité.
Tu dois analyser chaque ligne de dépense et lui attribuer :
1. Un statut "Budget Vert" (Vrai/Faux)
2. Un Axe (Axe 1 à Axe 6)
3. Un Code Agrégat (Axxx) selon la liste ci-dessous.

LISTE DES AXES :
- Axe 1 : Atténuation du changement climatique (Ex: Rénovation énergétique, Véhicules électriques)
- Axe 2 : Adaptation au changement climatique (Ex: Végétalisation, Gestion de l'eau)
- Axe 3 : Gestion de la ressource en eau
- Axe 4 : Économie circulaire (Ex: Réemploi, Déchets)
- Axe 5 : Pollution (Ex: Qualité de l'air)
- Axe 6 : Biodiversité (Ex: Espaces verts, Protection nature)

LISTE DES AGRÉGATS (Catégories) :
- A105 : Subventions d'investissement versées
- A110 : Autres immobilisations incorporelles
- A115 : Immobilisations incorporelles en cours
- A120 : Terrains
- A125 : Constructions
- A130 : Réseaux et installations de voirie
- A135 : Réseaux divers
- A140 : Installations techniques, agencements et matériel
- A145 : Immobilisations mises en concessions ou affermées
- A150 : Autres
- A155 : Immobilisations corporelles en cours
- A165 : IMMOBILISATIONS FINANCIÈRES
- A225 : Créances correspondant à des opérations pour compte de tiers
- R105 : Dotations de l'état
- R115 : Compensations, autres attributions et autres participations
- R130 : Ventes de biens ou prestations de services
- R205 : Achats et charges externes
- R210 : Dont salaires, traitements et rémunérations diverses
- R215 : Dont charges sociales
- R225 : Autres charges de fonctionnement (dont pertes sur créances irrécouvrables)
- R305 : Dont ménages
- R310 : Dont personnes morales de droit privé
- R315 : Dont collectivités territoriales
- R320 : Dont autres organismes publics
- R325 : Dont établissements d'enseignement
- R330 : Autres charges
- R515 : Autres charges financières

RÈGLES ABSOLUES :
- Tu DOIS traiter CHAQUE ligne fournie en entrée.
- Si tu reçois 5 lignes, tu DOIS renvoyer une liste de 5 objets.
- Doute → budget_vert = false
- Exclure : climatisation, gazon synthétique, véhicules thermiques, éclairage non LED, désherbant, carburant
- N'inclure que les dépenses DIRECTEMENT favorables au climat/biodiversité

Réponds UNIQUEMENT avec une liste JSON valide :

[
  {"ligne":"Isolation...","montant_ht":1500,"budget_vert":true,"axe":"Axe 1","code_categorie":"A125","confiance":0.9,"explication":"Rénovation thermique"},
  {"ligne":"Peinture...","montant_ht":500,"budget_vert":false,"axe":null,"code_categorie":"R205","confiance":1.0,"explication":"Entretien standard"}
]
"""

async def classify_lines_with_ollama(lines: List[Dict]) -> List[Dict]:
    if not lines:
        return []

    user_message = "Analyse ces lignes de devis :\n\n"
    for i, line in enumerate(lines, 1):
        user_message += f"{i}. {line['designation']} | {line['montant_ht']} € HT\n"

    async with httpx.AsyncClient(timeout=300.0) as client:  # 180s → 300s (5 minutes)
        try:
            resp = await client.post(
                "http://ollama:11434/api/chat",
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
                        "num_ctx": 4096  # 2048 → 4096 (plus de mémoire pour Phi-3)
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
