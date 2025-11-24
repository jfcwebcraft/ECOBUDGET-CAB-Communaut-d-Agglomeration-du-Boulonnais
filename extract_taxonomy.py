import pandas as pd
import sys

try:
    # Lire les agrégats depuis le CSV déjà extrait
    df_agregats = pd.read_csv(r"C:\Users\docje\OneDrive\Documents\Code\CAB\ECOBUDGET-CAB\taxonomy_agregats.csv")
    
    # Garder unique (Code, Libellé)
    # Les colonnes sont: LIBELLE_NOMENCLATURE, NUMERO_COMPTE, AGR_DEBIT, LIBELLE_AGREGAT_DEBIT
    agregats_list = df_agregats[['AGR_DEBIT', 'LIBELLE_AGREGAT_DEBIT']].drop_duplicates().values.tolist()
    
    print("Génération du Prompt Système...")
    prompt = 'Tu es un expert en classification "Budget Vert" pour une collectivité.\n'
    prompt += 'Tu dois analyser chaque ligne de dépense et lui attribuer :\n'
    prompt += '1. Un statut "Budget Vert" (Vrai/Faux)\n'
    prompt += '2. Un Axe (Axe 1 à Axe 6)\n'
    prompt += '3. Un Code Agrégat (Axxx) selon la liste ci-dessous.\n\n'
    
    prompt += 'LISTE DES AXES :\n'
    prompt += '- Axe 1 : Atténuation du changement climatique (Ex: Rénovation énergétique, Véhicules électriques)\n'
    prompt += '- Axe 2 : Adaptation au changement climatique (Ex: Végétalisation, Gestion de l\'eau)\n'
    prompt += '- Axe 3 : Gestion de la ressource en eau\n'
    prompt += '- Axe 4 : Économie circulaire (Ex: Réemploi, Déchets)\n'
    prompt += '- Axe 5 : Pollution (Ex: Qualité de l\'air)\n'
    prompt += '- Axe 6 : Biodiversité (Ex: Espaces verts, Protection nature)\n\n'
    
    prompt += 'LISTE DES AGRÉGATS (Catégories) :\n'
    for code, libelle in agregats_list:
        if pd.notna(code) and pd.notna(libelle):
            prompt += f'- {code} : {libelle}\n'
            
    # Sauvegarder le prompt dans un fichier pour lecture facile
    with open(r"C:\Users\docje\OneDrive\Documents\Code\CAB\ECOBUDGET-CAB\generated_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
        
    print("Prompt généré avec succès dans generated_prompt.txt")

except Exception as e:
    print(f"Erreur : {e}")
