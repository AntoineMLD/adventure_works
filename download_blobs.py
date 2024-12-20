from azure.storage.blob import ContainerClient
import os

def print_blob_hierarchy(container_client):
    """
    Affiche l'arborescence des blobs dans le conteneur.
    """
    print("Arborescence des blobs dans le conteneur :")
    blob_names = [blob.name for blob in container_client.list_blobs()]
    
    # Organise les blobs en une arborescence
    file_tree = {}
    for blob_name in blob_names:
        parts = blob_name.split('/')
        current_level = file_tree
        for part in parts:
            current_level = current_level.setdefault(part, {})
    
    # Affiche l'arborescence
    def print_tree(tree, indent=""):
        for key, subtree in tree.items():
            print(f"{indent}{key}")
            if isinstance(subtree, dict):
                print_tree(subtree, indent + "  ")

    print_tree(file_tree)

def download_blob(container_client, blob_name, local_folder):
    """
    Télécharge un fichier blob spécifique depuis Azure et le sauvegarde localement.
    """
    local_path = os.path.join(local_folder, blob_name)  
    os.makedirs(os.path.dirname(local_path), exist_ok=True) 
    # Télécharge le fichier
    print(f"Téléchargement du fichier : {blob_name}")
    with open(local_path, "wb") as file:
        blob_data = container_client.get_blob_client(blob_name).download_blob()
        file.write(blob_data.readall())

def download_blobs_from_sas_url(sas_url, local_folder):
    # Créer un client ContainerClient à partir de l'URL SAS
    container_client = ContainerClient.from_container_url(container_url=sas_url)

    # Créer le dossier local racine si nécessaire
    os.makedirs(local_folder, exist_ok=True)

    
    print("Liste des blobs dans le conteneur :")
    
    # Liste tous les blobs
    blobs = container_client.list_blobs()

    # Télécharge récursivement les blobs et créer des dossiers le cas échéant
    for blob in blobs:
        blob_name = blob.name
        if '.' in os.path.basename(blob_name): 
            download_blob(container_client, blob_name, local_folder)
        else:
            print(f"Création du dossier : {blob_name}")
            # Créer le dossier correspondant localement sans télécharger de fichier
            os.makedirs(os.path.join(local_folder, blob_name), exist_ok=True)

    print("Tous les blobs ont été téléchargés.")

if __name__ == '__main__':
    # Charger l'URL SAS depuis le fichier généré par le premier script
    with open("sas_url.txt", "r") as file:
        sas_url = file.read().strip()

   
    local_folder = "downloaded_blobs"

    # Afficher l'arborescence des blobs dans le conteneur
    container_client = ContainerClient.from_container_url(container_url=sas_url)
    print_blob_hierarchy(container_client)

    
    # Télécharge tous les blobs récursivement
    download_blobs_from_sas_url(sas_url, local_folder)

