import pandas as pd
import base64
from PIL import Image
from io import BytesIO
import os

def save_image_from_bytes(image_bytes, item_id, output_dir, image_format='JPEG'):
    """ Convertir les bytes de l'image et les enregistrer dans un fichier """
    try:
        # Convertir les bytes en image
        image = Image.open(BytesIO(image_bytes))
        image_path = os.path.join(output_dir, f"{item_id}.{image_format.lower()}")
        
        # Sauvegarder l'image
        image.save(image_path, format=image_format)
        print(f"Image sauvegardée : {image_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion de l'image pour {item_id}: {e}")

def process_csv(csv_file, output_dir, image_format='JPEG'):
    """ Lire le CSV et traiter chaque ligne pour extraire l'image et l'enregistrer """
    df = pd.read_csv(csv_file)
    
    # Assurer que le dossier de sortie existe
    os.makedirs(output_dir, exist_ok=True)
    
    for index, row in df.iterrows():
        image_bytes_str = row['image']  
        item_id = row['item_ID']
        
        # Convertir les bytes de l'image de la chaîne
        image_bytes = eval(image_bytes_str)['bytes']  # Évaluer les bytes à partir de la chaîne
        save_image_from_bytes(image_bytes, item_id, output_dir, image_format)

if __name__ == "__main__":
    # Liste des fichiers CSV générés par le script précédent
    csv_files = [
        'downloaded_blobs/product_eval/test-00000-of-00003.csv',  # Remplacez par le chemin réel du CSV 1
        'downloaded_blobs/product_eval/test-00001-of-00003.csv',  # Remplacez par le chemin réel du CSV 2
        'downloaded_blobs/product_eval/test-00002-of-00003.csv'   # Remplacez par le chemin réel du CSV 3
    ]
    
    # Dossier de sortie pour les images
    output_dir = 'output_images'
    
    
    image_format = 'JPEG'
    
    # Traiter chaque fichier CSV
    for csv_file in csv_files:
        print(f"Traitement du fichier CSV : {csv_file}")
        process_csv(csv_file, output_dir, image_format)
