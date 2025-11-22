$file = "ecobudget.tar.gz"

if (-not (Test-Path $file)) {
    Write-Error "Le fichier $file est introuvable."
    return
}

Write-Host "=== Tentative d'upload vers file.io ==="

try {
    # Upload vers file.io (expire après 1 téléchargement ou 14 jours)
    $response = Invoke-RestMethod -Uri "https://file.io" -Method Post -InFile $file
    if ($response.success) {
        $url = $response.link
    } else {
        throw "Erreur file.io"
    }
} catch {
    Write-Warning "Echec file.io. Tentative vers transfer.sh..."
    try {
        $url = curl.exe --upload-file $file "https://transfer.sh/$file"
    } catch {
        Write-Error "Tous les uploads ont échoué. Vérifiez votre connexion internet."
        return
    }
}

Write-Host ""
Write-Host "✅ Upload réussi !"
Write-Host "COPIEZ et COLLEZ la ligne ci-dessous dans votre terminal VPS :"
Write-Host "------------------------------------------------------------------------"
Write-Host "wget $url -O ecobudget.tar.gz && mkdir -p ECOBUDGET-CAB && tar -xzf ecobudget.tar.gz -C ECOBUDGET-CAB && cd ECOBUDGET-CAB && if [ ! -f .env ]; then cp .env.example .env; fi && mkdir -p ollama_models && docker-compose down && docker-compose up -d --build"
Write-Host "------------------------------------------------------------------------"
