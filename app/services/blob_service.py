import os

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

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

    # ---------------------------------------------------
    # Upload File
    # ---------------------------------------------------
    @staticmethod
    def upload_file(file, blob_name):

        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        file.stream.seek(0)

        blob_client.upload_blob(
            data=file.stream,
            overwrite=True,
            content_type=file.content_type
        )

        properties = blob_client.get_blob_properties()

        return {
            "url": blob_client.url,
            "version_id": properties.version_id,
            "size": properties.size
        }

    # ---------------------------------------------------
    # Download Latest / Specific Version
    # ---------------------------------------------------
    @staticmethod
    def download_blob(
        blob_name,
        version_id=None
    ):

        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        return blob_client.download_blob(
            version_id=version_id
        ).readall()

    # ---------------------------------------------------
    # Delete Blob
    # ---------------------------------------------------
    @staticmethod
    def delete_blob(blob_name):

        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        blob_client.delete_blob(
            delete_snapshots="include"
        )

    # ---------------------------------------------------
    # Restore Previous Version
    # ---------------------------------------------------
    @staticmethod
    def restore_version(
        blob_name,
        version_id
    ):

        # Create a client for the OLD version
        old_blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        # Download the requested version
        data = old_blob_client.download_blob(
            version_id=version_id
        ).readall()

        # Create a NEW client for the current blob
        latest_blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        # Upload the old data as the newest version
        latest_blob_client.upload_blob(
            data=data,
            overwrite=True
        )

        properties = latest_blob_client.get_blob_properties()

        return properties.version_id