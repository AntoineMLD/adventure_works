from dotenv import load_dotenv
import datetime
import os
from azure.storage.blob import ContainerClient, ContainerSasPermissions, generate_container_sas, BlobServiceClient



class SASSamples:
    def create_service_sas_container(self, container_client: ContainerClient, account_key: str):
        # Créer un SAS token valide pour un jour
        start_time = datetime.datetime.now(datetime.timezone.utc)
        expiry_time = start_time + datetime.timedelta(days=1)

        sas_token = generate_container_sas(
            account_name=container_client.account_name,
            container_name=container_client.container_name,
            account_key=account_key,
            permission=ContainerSasPermissions(read=True, list=True),
            expiry=expiry_time,
            start=start_time
        )

        return sas_token

    def generate_sas_url(self, blob_service_client):
        container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
        container_client = blob_service_client.get_container_client(container=container_name)

        # Extrait la clé de l'environnement
        account_key = os.getenv("STORAGE_CONNECTION_STRING").split("AccountKey=")[1].split(";")[0]

        # Génére le SAS token
        sas_token = self.create_service_sas_container(container_client, account_key)

        # Construit l'URL avec le SAS token
        sas_url = f"{container_client.url}?{sas_token}"
        return sas_url

if __name__ == '__main__':
    
    load_dotenv()

    
    connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Génére le SAS URL
    sample = SASSamples()
    sas_url = sample.generate_sas_url(blob_service_client)

    # Sauvegarde l'URL SAS dans un fichier
    print(f"SAS URL générée : {sas_url}")
    with open("sas_url.txt", "w") as file:
        file.write(sas_url)
