#!/bin/bash

# Décompresse le fichier ZIP dans le répertoire "unzip_folder"
unzip downloaded_blobs/machine_learning/reviews.zip -d unzip_folder

# Vérifie si le fichier "amazon_review_polarity_csv.tgz" existe dans le répertoire
if [ -f "unzip_folder/amazon_review_polarity_csv.tgz" ]; then
    # Si le fichier existe, le décompresser
    tar -xzvf "unzip_folder/amazon_review_polarity_csv.tgz" -C "unzip_folder"
    echo "Fichier .tgz décompressé avec succès."

    # Supprime le fichier .tgz après décompression
    rm "unzip_folder/amazon_review_polarity_csv.tgz"
    echo "Fichier .tgz supprimé."
else
    echo "Le fichier .tgz n'existe pas dans le dossier."
fi

# Créer le dossier "staging" s'il n'existe pas
mkdir -p staging/machine_learning

# Renomme et déplace les fichiers test.csv et train.csv du dossier unzip_folder
if [ -f "unzip_folder/test.csv" ]; then
    mv "unzip_folder/test.csv" "staging/machine_learning/test_reviews.csv"
    echo "Fichier test.csv déplacé et renommé en test_reviews.csv."
fi

if [ -f "unzip_folder/train.csv" ]; then
    mv "unzip_folder/train.csv" "staging/machine_learning/train_reviews.csv"
    echo "Fichier train.csv déplacé et renommé en train_reviews.csv."
fi

# Renomme et déplace les fichiers test.csv et train.csv du dossier amazon_review_polarity_csv
if [ -f "unzip_folder/amazon_review_polarity_csv/test.csv" ]; then
    mv "unzip_folder/amazon_review_polarity_csv/test.csv" "staging/machine_learning/test_amazon_polarity.csv"
    echo "Fichier test.csv (amazon_review_polarity_csv) déplacé et renommé en test_amazon_polarity.csv."
fi

if [ -f "unzip_folder/amazon_review_polarity_csv/train.csv" ]; then
    mv "unzip_folder/amazon_review_polarity_csv/train.csv" "staging/machine_learning/train_amazon_review_polarity.csv"
    echo "Fichier train.csv (amazon_review_polarity_csv) déplacé et renommé en train_amazon_review_polarity.csv."
fi

rm -rf unzip_folder
echo "Dossier unzip_folder et son contenu supprimés avec succès."

echo "Tous les fichiers ont été déplacés, renommés et le dossier temporaire a été nettoyé."
