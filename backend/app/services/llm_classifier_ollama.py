import os
import time
import json
import re
import httpx
import traceback
from typing import List, Dict

SYSTEM_PROMPT = """Tu es un expert en finances publiques. Analyse cette dépense pour le Budget Vert.
Si le libellé est vague, classe en 'A_APPROFONDIR' et pose une question dans le champ justification.

Tu dois renvoyer un objet JSON unique contenant :
                designation = line.get('designation') or line.get('libelle') or ''
                user_message = f"Analyse cette ligne de devis :\n\n{designation} | {line.get('montant_ht')} € HT"
- montant_ht (number)
- budget_vert (true/false)
- axe ("Axe 1".."Axe 6" | null)
- code_categorie (Axxx ou Rxxx | null)
- confiance (0.0..1.0)
- explication (string)

RÈGLES :
- Traite CHAQUE ligne
- Doute → budget_vert = false
- EXCLURE : climatisation, gazon synthétique, véhicule thermique, désherbant
- N'inclure que les dépenses DIRECTEMENT favorables climat/biodiversité

Contrainte : réponds uniquement par un objet JSON (strict) sans autre texte.
Exemple de sortie :
{"ligne":"Isolation...","montant_ht":1500,"budget_vert":true,"axe":"Axe 1","code_categorie":"A125","confiance":0.9,"explication":"Rénovation thermique"}
"""

import time

async def classify_lines_with_ollama(lines: List[Dict]) -> Dict:
    if not lines:
        return {"results": [], "metadata": {}}

                        "ligne": designation,
                        "montant_ht": line.get('montant_ht'),
    
    # Traiter chaque ligne individuellement pour éviter le timeout
    async with httpx.AsyncClient(timeout=180.0) as client:
        for i, line in enumerate(lines, 1):
            try:
                user_message = f"Analyse cette ligne de devis :\n\n{line['designation']} | {line['montant_ht']} € HT"
                
                print(f"--- ENVOI OLLAMA (ligne {i}/{len(lines)}) ---")
                ollama_url = os.getenv('OLLAMA_URL', 'http://ollama:11434')
                content = resp.json().get("message", {}).get("content", "")
                    f"{ollama_url}/api/chat",
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
                        "ligne": designation,
                        "montant_ht": line.get('montant_ht'),
                        result = result[0]
                    
                    # Normalisation
                    result.setdefault("ligne", line['designation'])
                    result.setdefault("montant_ht", line['montant_ht'])
                    result.setdefault("budget_vert", False)
                    result.setdefault("code_categorie", None)
                    result.setdefault("axe", None)
                    result.setdefault("confiance", 0.0)
                    result.setdefault("explication", "Non classifié")
                    
                    "ligne": designation,
                    "montant_ht": line.get('montant_ht'),
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
