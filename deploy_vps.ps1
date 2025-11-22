$VPS_USER = "root"
$VPS_HOST = "168.231.77.11"
$REMOTE_DIR = "/root/ECOBUDGET-CAB"

Write-Host "=== Déploiement ECOBUDGET-CAB sur $VPS_HOST ==="

# 1. Création de l'archive
Write-Host "1. Création de l'archive locale (ecobudget.tar.gz)..."
try {
    tar -czf ecobudget.tar.gz --exclude=venv --exclude=node_modules --exclude=__pycache__ --exclude=.git --exclude=dist --exclude=ollama_models .
} catch {
    Write-Error "Erreur lors de la création de l'archive. Vérifiez que 'tar' est installé."
    exit 1
}

# 2. Transfert
Write-Host "2. Transfert de l'archive (mot de passe requis)..."
scp ecobudget.tar.gz ${VPS_USER}@${VPS_HOST}:/root/

# 3. Déploiement distant
Write-Host "3. Installation et lancement sur le VPS (mot de passe requis)..."
$commands = "
    mkdir -p $REMOTE_DIR
    tar -xzf /root/ecobudget.tar.gz -C $REMOTE_DIR
    cd $REMOTE_DIR
    if [ ! -f .env ]; then cp .env.example .env; fi
    # Création du dossier pour les modèles Ollama s'il n'existe pas
    mkdir -p ollama_models
    docker-compose down
    docker-compose up -d --build
    rm /root/ecobudget.tar.gz
"
ssh ${VPS_USER}@${VPS_HOST} $commands

# 4. Nettoyage
Write-Host "4. Nettoyage local..."
Remove-Item ecobudget.tar.gz

Write-Host "=== Déploiement terminé ! ==="
Write-Host "Backend API : http://${VPS_HOST}:8000/docs"
Write-Host "Frontend    : http://${VPS_HOST}:5173"
