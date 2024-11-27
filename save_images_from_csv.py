import pandas as pd
import os
from PIL import Image
from io import BytesIO
import json

def save_image_from_bytes(image_bytes, item_id, output_dir, image_format='PNG', metadata=None):
    """ Convertir les bytes de l'image et les enregistrer dans un fichier avec les métadonnées """
    try:
        # Convertir les bytes en image
        image = Image.open(BytesIO(image_bytes))
        
        # Créer le chemin du fichier image avec les métadonnées dans le nom
        image_filename = f"{item_id}_{metadata['query']}_{metadata['position']}.{image_format.lower()}"
        image_path = os.path.join(output_dir, image_filename)
        
        # Sauvegarder l'image en format spécifié (PNG ou JPEG)
        image.save(image_path, format=image_format)
        print(f"Image sauvegardée : {image_path}")
        
        # Enregistrer les métadonnées dans un fichier JSON
        metadata_path = os.path.join(output_dir, f"{item_id}_metadata.json")
        with open(metadata_path, 'w') as meta_file:
            json.dump(metadata, meta_file, indent=4)
        print(f"Métadonnées sauvegardées : {metadata_path}")
    
    except Exception as e:
        print(f"Erreur lors de la conversion de l'image pour {item_id}: {e}")

def process_csv(csv_file, output_dir, image_format='PNG'):
    """ Lire le CSV et traiter chaque ligne pour extraire l'image et l'enregistrer avec les métadonnées """
    df = pd.read_csv(csv_file)
    
    # Assurer que le dossier de sortie existe
    os.makedirs(output_dir, exist_ok=True)
    
    for index, row in df.iterrows():
        image_bytes_str = row['image']  # On suppose que la colonne 'image' contient des bytes
        item_id = row['item_ID']
        
        # Extraire les métadonnées
        metadata = {
            'item_ID': item_id,
            'query': row['query'],
            'title': row['title'],
            'position': row['position']
        }
        
        # Convertir les bytes de l'image de la chaîne
        image_bytes = eval(image_bytes_str)['bytes']  # Évaluer les bytes à partir de la chaîne
        
        # Sauvegarder l'image et ses métadonnées
        save_image_from_bytes(image_bytes, item_id, output_dir, image_format, metadata)

if __name__ == "__main__":
    # Liste des fichiers CSV générés par le script précédent
    csv_files = [
        'downloaded_blobs/product_eval/test-00000-of-00003.csv',  
        'downloaded_blobs/product_eval/test-00001-of-00003.csv',  
        'downloaded_blobs/product_eval/test-00002-of-00003.csv'   
    ]
    

    os.makedirs('staging/product_eval', exist_ok=True)
    
    output_dir = 'staging/product_eval'
    
    
    image_format = 'JPEG'
    
    # Traiter chaque fichier CSV
    for csv_file in csv_files:
        print(f"Traitement du fichier CSV : {csv_file}")
        process_csv(csv_file, output_dir, image_format)
