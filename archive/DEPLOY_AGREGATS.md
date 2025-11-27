# Commandes de déploiement VPS - Vérification des Agrégats

```bash
# Connexion au VPS
ssh root@168.231.77.11

# Aller dans le répertoire du projet
cd /root/ECOBUDGET-CAB-Communaut-d-Agglomeration-du-Boulonnais

# Récupérer les dernières modifications
git pull origin main

# Redémarrer les services backend et frontend
docker-compose restart backend frontend

# Vérifier les logs
docker-compose logs -f --tail=50 backend
```

## Nouveautés de cette version

### Interface de Vérification des Agrégats
- **Colonne "Catégorie" éditable** : chaque ligne possède un menu déroulant permettant de changer l'agrégat
- **27 agrégats disponibles** : A105 à R515 avec libellés complets
- **Indicateur visuel** : les lignes modifiées sont surlignées en jaune avec animation
- **Tooltip** : survol affiche le code et libellé complet (ex: "A125 - Constructions")

### Données de référence
- Fichier `backend/data/agregats_reference.json` : référentiel complet
- Endpoint `/analyze` enrichi avec `agregats_reference` dans la réponse
- Service backend `agregats_reference.py` pour charger la référence

### Améliorations UX
- Background jaune sur les lignes modifiées
- Animation "ping" pour attirer l'attention
- Select toujours visible avec focus anneau bleu
- Libellés complets dans les options du dropdown
