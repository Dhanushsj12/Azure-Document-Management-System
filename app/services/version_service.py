import os

from app.extensions import db
from app.models.document import Document
from app.models.version import Version
from app.services.blob_service import BlobService
from app.services.audit_service import AuditService


class VersionService:

    @staticmethod
    def upload(file, user_id):

        print("\n========== VERSION SERVICE START ==========")

        # Check whether document already exists
        document = Document.query.filter_by(
            title=file.filename
        ).first()

        if document:

            version_number = document.latest_version + 1
            document.latest_version = version_number

        else:

            document = Document(
                title=file.filename,
                owner_id=user_id,
                latest_version=1
            )

            db.session.add(document)
            db.session.flush()

            version_number = 1

        # ----------------------------------------
        # Calculate local file size
        # ----------------------------------------
        file.stream.seek(0, os.SEEK_END)
        local_size = file.stream.tell()
        file.stream.seek(0)

        print(f"Local File Size : {local_size}")

        # ----------------------------------------
        # Upload to Azure Blob Storage
        # ----------------------------------------
        blob_name = document.title

        blob = BlobService.upload_file(
            file,
            blob_name
        )

        print(f"Azure Upload Result : {blob}")

        # ----------------------------------------
        # Get Azure Blob Size
        # ----------------------------------------
        blob_client = BlobService.container_client.get_blob_client(
            blob_name
        )

        properties = blob_client.get_blob_properties()

        azure_size = properties.size

        print(f"Azure Blob Size : {azure_size}")

        # ----------------------------------------
        # Save Version
        # ----------------------------------------
        version = Version(

            document_id=document.id,

            version_number=version_number,

            uploaded_by=user_id,

            file_size=azure_size,

            file_path=blob["url"],

            azure_version_id=blob["version_id"]

        )

        db.session.add(version)
        db.session.commit()

        print(f"Saved to Database : {version.file_size}")
        print("=========== VERSION SERVICE END ===========\n")

        AuditService.log(

            user_id=user_id,

            action="Upload",

            document_name=document.title

        )

        return document

    @staticmethod
    def restore(version_id):

        version = Version.query.get_or_404(
            version_id
        )

        blob_name = version.document.title

        BlobService.restore_version(
            blob_name,
            version.azure_version_id
        )

        AuditService.log(
            user_id=version.uploaded_by,
            action="Restore",
            document_name=document.title
        )

        return True