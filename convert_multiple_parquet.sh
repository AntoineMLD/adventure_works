#!/bin/bash

# Liste des fichiers Parquet à convertir
files=(
    "downloaded_blobs/product_eval/test-00000-of-00003.parquet"
    "downloaded_blobs/product_eval/test-00001-of-00003.parquet"
    "downloaded_blobs/product_eval/test-00002-of-00003.parquet"
)

# Boucle pour chaque fichier Parquet
for file in "${files[@]}"; do

    # Exécution du script Python pour chaque fichier Parquet
    echo "Conversion du fichier : $file"
    python convert_parquet_to_csv.py "$file"
done
