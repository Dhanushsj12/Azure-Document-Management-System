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

        # Always rewind stream before upload
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

        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        data = blob_client.download_blob(
            version_id=version_id
        ).readall()

        blob_client.upload_blob(
            data,
            overwrite=True
        )

        properties = blob_client.get_blob_properties()

        return properties.version_id