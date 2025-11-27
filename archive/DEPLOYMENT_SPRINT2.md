# 🚀 SPRINT 2 - INSTRUCTIONS DE DÉPLOIEMENT

## ✅ Ce qui vient d'être fait (sur votre PC)

- ✅ Implémentation **pdf_extractor.py** : extraction intelligente des tableaux + fallback texte
- ✅ Implémentation **llm_classifier_ollama.py** : classification avec prompt budget vert strict
- ✅ Création de l'endpoint **POST /api/v1/analyze** : extraction + classification en 1 appel
- ✅ Mise à jour du README avec le statut Sprint 2
- ✅ Code committé et poussé sur GitHub ✅

## 🎯 ACTIONS À FAIRE MAINTENANT

### 1. Télécharger le modèle Mistral-Nemo (5 min)

**Sur le terminal VPS (root@168.231.77.11) :**

```bash
docker exec -it ecobudget-cab-communaut-d-agglomeration-du-boulonnais_ollama_1 ollama pull mistral-nemo
```

> ⏳ **Temps estimé** : 3-5 minutes (télécharge ~7 GB)

**Vérifier que le modèle est bien téléchargé :**
```bash
docker exec -it ecobudget-cab-communaut-d-agglomeration-du-boulonnais_ollama_1 ollama list
```

Vous devriez voir `mistral-nemo` dans la liste.

---

### 2. Redéployer l'application (Backend + Frontend) (3 min)

**Sur le terminal VPS :**

```bash
cd /root/ECOBUDGET-CAB-Communaut-d-Agglomeration-du-Boulonnais
git pull origin main
docker-compose down
docker-compose up -d --build
```

> ⏳ **Temps estimé** : 2-3 minutes (rebuild frontend + backend)

---

### 3. Tester l'interface complète (1 min)

1. Allez sur **http://168.231.77.11:5173**
2. Vous devriez voir la nouvelle interface "ECOBUDGET-CAB" avec la zone d'upload verte.
3. Glissez-déposez un PDF.
4. Admirez le résultat : tableau analysé, totaux calculés, badges "VERT" ou "NON".

#### Option B : Test API seul (si besoin)

```bash
# Depuis votre PC (PowerShell)
curl -X POST "http://168.231.77.11:8000/api/v1/analyze" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "file=@C:\chemin\vers\votre\devis.pdf"
```

---

## 📊 Résultat attendu

La réponse JSON devrait ressembler à :

```json
{
  "status": "success",
  "filename": "devis_exemple.pdf",
  "lignes": [
    {
      "ligne": "Isolation toiture 200 m²",
      "montant_ht": 15420.50,
      "budget_vert": true,
      "code_categorie": "V1",
      "confiance": 0.98,
      "explication": "Rénovation thermique performante"
    },
    {
      "ligne": "Climatisation réversible 12kW",
      "montant_ht": 8900.00,
      "budget_vert": false,
      "code_categorie": null,
      "confiance": 1.00,
      "explication": "Refroidissement actif exclu du budget vert"
    }
  ],
  "total_ht": 24320.50,
  "total_budget_vert": 15420.50,
  "pourcentage_budget_vert": 63.4
}
```

---

## 🔥 Pour la démo devant la compta/transition éco

### Points à montrer

1. **Upload d'un vrai devis PDF** (anonymisé)
2. **Extraction automatique** des lignes avec montants
3. **Classification intelligente** :
   - ✅ Isolation, LED, bornes IRVE → budget_vert = true
   - ❌ Climatisation, gasoil → budget_vert = false
4. **Calculs automatiques** : total HT, total budget vert, %
5. **Explications** : chaque ligne a son explication

### Message clé pour les décideurs

> "L'outil analyse automatiquement les devis en suivant les règles strictes de l'Ademe 2025. Il gagne un temps considérable en pré-classifiant les dépenses, tout en restant 100% local (RGPD-compliant). La validation humaine reste possible pour les cas douteux."

---

## ⚠️ En cas de problème

### Le modèle ne répond pas
```bash
# Vérifier les logs Ollama
docker logs ecobudget-cab-communaut-d-agglomeration-du-boulonnais_ollama_1
```

### Erreur d'extraction PDF
```bash
# Vérifier les logs backend
docker logs ecobudget-cab-communaut-d-agglomeration-du-boulonnais_backend_1
```

### L'endpoint /analyze n'existe pas
- Vérifiez que `git pull` a bien récupéré les nouveaux fichiers
- Relancez `docker-compose up -d --build`

### Erreur "KeyError: 'ContainerConfig'"
C'est un bug connu des vieilles versions de `docker-compose`.
Solution radicale (si la suppression simple échoue) :
```bash
cd /root/ECOBUDGET-CAB-Communaut-d-Agglomeration-du-Boulonnais
# Lister tous les conteneurs (même arrêtés) pour trouver le fautif
docker ps -a | grep frontend
# Supprimer par ID (remplacez CONTAINER_ID par l'ID trouvé)
docker rm -f CONTAINER_ID
# OU supprimer tous les conteneurs du projet pour repartir propre
docker-compose down --remove-orphans
docker-compose up -d --build
```

---

## 📌 Fichiers créés/modifiés dans ce sprint

- ✅ `backend/app/services/pdf_extractor.py` (75 lignes)
- ✅ `backend/app/services/llm_classifier_ollama.py` (83 lignes)
- ✅ `backend/app/routers/analyze.py` (48 lignes - NOUVEAU)
- ✅ `backend/app/main.py` (ajout du router)
- ✅ `README.md` (section Sprint 2 ajoutée)

**Total : ~200 lignes de code production prêtes pour la démo !**
