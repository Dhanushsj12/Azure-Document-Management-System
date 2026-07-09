import os

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()


class BlobService:

    connection_string = os.getenv(
        "AZURE_STORAGE_CONNECTION_STRING"
    )

    container_name = os.getenv(
        "AZURE_CONTAINER_NAME"
    )

    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string
    )

    container_client = blob_service_client.get_container_client(
        container_name
    )

    @staticmethod
    def upload_file(file, blob_name):

        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        file.seek(0)

        blob_client.upload_blob(
            file,
            overwrite=True
        )

        return blob_client.url

    @staticmethod
    def download_blob(blob_name):

        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        return blob_client.download_blob().readall()

    @staticmethod
    def delete_blob(blob_name):

        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        blob_client.delete_blob()