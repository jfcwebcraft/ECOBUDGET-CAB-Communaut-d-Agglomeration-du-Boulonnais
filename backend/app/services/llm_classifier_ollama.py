import httpx
import json
import re
import traceback
from typing import List, Dict

SYSTEM_PROMPT = """Tu es un expert en classification "Budget Vert" pour une collectivité.
Analyse chaque ligne et attribue :
1. budget_vert (true/false)
2. axe (Axe 1 à 6)
3. code_categorie (Axxx ou Rxxx)

AXES :
- Axe 1 : Atténuation climat (Isolation, Solaire, Véhicule électrique)
- Axe 2 : Adaptation climat (Végétalisation, Eau)
- Axe 3 : Eau (Récupération, Assainissement)
- Axe 4 : Économie circulaire (Compost, Réemploi)
- Axe 5 : Pollution (LED, Air)
- Axe 6 : Biodiversité (Plantation, Espaces verts)

CODES AGRÉGATS :
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
- R210 : Salaires et rémunérations
- R215 : Charges sociales
- R225 : Autres charges de fonctionnement
- R305 : Ménages
- R310 : Personnes morales de droit privé
- R315 : Collectivités territoriales
- R320 : Autres organismes publics
- R325 : Établissements d'enseignement
- R330 : Autres charges
- R515 : Autres charges financières

RÈGLES :
- Tu DOIS traiter CHAQUE ligne
- Doute → budget_vert = false
- EXCLURE : climatisation, gazon synthétique, véhicule thermique, désherbant
- N'inclure que les dépenses DIRECTEMENT favorables climat/biodiversité

Réponds UNIQUEMENT JSON :

[
  {"ligne":"Isolation...","montant_ht":1500,"budget_vert":true,"axe":"Axe 1","code_categorie":"A125","confiance":0.9,"explication":"Rénovation thermique"},
  {"ligne":"Peinture...","montant_ht":500,"budget_vert":false,"axe":null,"code_categorie":"R205","confiance":1.0,"explication":"Entretien standard"}
]
"""

import time
import httpx
import json
import re
import traceback
from typing import List, Dict

SYSTEM_PROMPT = """Tu es un expert en classification "Budget Vert" pour une collectivité.
Analyse chaque ligne et attribue :
1. budget_vert (true/false)
2. axe (Axe 1 à 6)
3. code_categorie (Axxx ou Rxxx)

AXES :
- Axe 1 : Atténuation climat (Isolation, Solaire, Véhicule électrique)
- Axe 2 : Adaptation climat (Végétalisation, Eau)
- Axe 3 : Eau (Récupération, Assainissement)
- Axe 4 : Économie circulaire (Compost, Réemploi)
- Axe 5 : Pollution (LED, Air)
- Axe 6 : Biodiversité (Plantation, Espaces verts)

CODES AGRÉGATS :
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
- R210 : Salaires et rémunérations
- R215 : Charges sociales
- R225 : Autres charges de fonctionnement
- R305 : Ménages
- R310 : Personnes morales de droit privé
- R315 : Collectivités territoriales
- R320 : Autres organismes publics
- R325 : Établissements d'enseignement
- R330 : Autres charges
- R515 : Autres charges financières

RÈGLES :
- Tu DOIS traiter CHAQUE ligne
- Doute → budget_vert = false
- EXCLURE : climatisation, gazon synthétique, véhicule thermique, désherbant
- N'inclure que les dépenses DIRECTEMENT favorables climat/biodiversité

Réponds UNIQUEMENT par un objet JSON (pas de liste) :

{
  "ligne": "Isolation...",
  "montant_ht": 1500,
  "budget_vert": true,
  "axe": "Axe 1",
  "code_categorie": "A125",
  "confiance": 0.9,
  "explication": "Rénovation thermique"
}
"""

import time

async def classify_lines_with_ollama(lines: List[Dict]) -> Dict:
    if not lines:
        return {"results": [], "metadata": {}}

    start_time = time.time()
    all_results = []
    
    # Traiter chaque ligne individuellement pour éviter le timeout
    async with httpx.AsyncClient(timeout=180.0) as client:
        for i, line in enumerate(lines, 1):
            try:
                user_message = f"Analyse cette ligne de devis :\n\n{line['designation']} | {line['montant_ht']} € HT"
                
                print(f"--- ENVOI OLLAMA (ligne {i}/{len(lines)}) ---")
                resp = await client.post(
                    "http://ollama:11434/api/chat",
                    json={
                        "model": "mistral",
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
                    # En cas d'erreur, marquer la ligne comme non classée
                    all_results.append({
                        "ligne": line['designation'],
                        "montant_ht": line['montant_ht'],
                        "budget_vert": False,
                        "axe": None,
                        "code_categorie": None,
                        "confiance": 0.0,
                        "explication": "Erreur IA – à vérifier manuellement"
                    })
                    continue
                
                resp.raise_for_status()
                content = resp.json()["message"]["content"]
                
                print(f"--- RÉPONSE OLLAMA ligne {i} ---")
                print(content)
                print("------------------------------------------")

                # Tentative d'extraction du JSON
                result = None
                try:
                    # Essayer de parser directement
                    result = json.loads(content)
                except json.JSONDecodeError:
                    # Si échec, essayer de trouver un objet JSON avec regex
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        try:
                            result = json.loads(json_match.group(0))
                        except:
                            pass

                if result:
                    # Si le résultat est une liste (ancien format), prendre le premier élément
                    if isinstance(result, list) and len(result) > 0:
                        result = result[0]
                    
                    # Normalisation
                    result.setdefault("ligne", line['designation'])
                    result.setdefault("montant_ht", line['montant_ht'])
                    result.setdefault("budget_vert", False)
                    result.setdefault("code_categorie", None)
                    result.setdefault("axe", None)
                    result.setdefault("confiance", 0.0)
                    result.setdefault("explication", "Non classifié")
                    
                    # Nettoyage du code catégorie
                    if result.get("code_categorie"):
                        code = str(result["code_categorie"]).strip().upper()
                        # Garder seulement si format valide (A ou R suivi de chiffres)
                        if re.match(r'^[AR]\d+$', code):
                            result["code_categorie"] = code
                        else:
                            # Essayer d'extraire le code si mélangé avec du texte (ex: "A125 - Constructions")
                            match_code = re.search(r'([AR]\d+)', code)
                            if match_code:
                                result["code_categorie"] = match_code.group(1)
                            else:
                                result["code_categorie"] = None
                    
                    all_results.append(result)
                else:
                    print(f"Réponse Ollama invalide (pas de JSON): {content}")
                    # Ligne non classée
                    all_results.append({
                        "ligne": line['designation'],
                        "montant_ht": line['montant_ht'],
                        "budget_vert": False,
                        "axe": None,
                        "code_categorie": None,
                        "confiance": 0.0,
                        "explication": "Erreur IA – format invalide"
                    })
                    
            except Exception as e:
                print(f"EXCEPTION ligne {i}: {e}")
                # En cas d'erreur, marquer la ligne comme non classée
                all_results.append({
                    "ligne": line['designation'],
                    "montant_ht": line['montant_ht'],
                    "budget_vert": False,
                    "axe": None,
                    "code_categorie": None,
                    "confiance": 0.0,
                    "explication": "Erreur IA – à vérifier manuellement"
                })
    
    duration = round(time.time() - start_time, 2)
    
    return {
        "results": all_results,
        "metadata": {
            "model": "mistral",
            "duration": duration,
            "lines_input": len(lines),
            "lines_output": len(all_results)
        }
    }
