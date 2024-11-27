#!/bin/bash

set -euo pipefail

# Fonction pour afficher les logs avec un timestamp
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1"
}

# 1. Lancer generate_sas.py
log "Lancement du script generate_sas.py..."
python generate_sas.py
log "Script generate_sas.py terminé avec succès."

# 2. Lancer extract_data_from_bb_to_csv.py
log "Lancement du script extract_data_from_bdd_to_csv.py..."
python extract_data_from_bdd_to_csv.py
log "Script extract_data_from_bdd_to_csv.py terminé avec succès."

# 3. Lancer download_blobs.py
log "Lancement du script download_blobs.py..."
python download_blobs.py
log "Script download_blobs.py terminé avec succès."

# 4. Déplacer le dossier nlp_data dans le dossier staging
log "Déplacement du dossier 'nlp_data' de 'downloaded_blobs' vers 'staging'..."
if [ -d "downloaded_blobs/nlp_data" ]; then
    mkdir -p staging
    mv downloaded_blobs/nlp_data staging/
    log "Dossier 'nlp_data' déplacé avec succès dans 'staging'."
else
    log "Erreur : Le dossier 'nlp_data' n'existe pas dans 'downloaded_blobs'."
    exit 1
fi

# 5. Lancer convert_multiple_parquet.sh
log "Lancement du script convert_multiple_parquet.sh..."
chmod +x convert_multiple_parquet.sh
./convert_multiple_parquet.sh
log "Script convert_multiple_parquet.sh terminé avec succès."

# 6. Lancer save_images_from_csv.py
log "Lancement du script save_images_from_csv.py..."
python save_images_from_csv.py
log "Script save_images_from_csv.py terminé avec succès."

#7. Lancer unzip_folder.sh
log "Lancement du script unzip_folder.sh..."
chmod +x unzip_folder.sh
./unzip_folder.sh
log "Script unzip_folder.sh terminé avec succès."

log "Pipeline terminé avec succès."
