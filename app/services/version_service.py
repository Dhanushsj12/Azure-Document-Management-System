import os

from app.extensions import db
from app.models.document import Document
from app.models.version import Version
from app.services.blob_service import BlobService
from app.services.audit_service import AuditService


class VersionService:

    @staticmethod
    def upload(file, user_id):

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

        # Upload using ORIGINAL filename
        # Azure automatically creates previous versions

        blob_name = document.title

        blob = BlobService.upload_file(
            file,
            blob_name
        )

        print("Azure Upload Result:", blob)

        version = Version(

            document_id=document.id,

            version_number=version_number,

            uploaded_by=user_id,

            file_size=file.content_length if file.content_length else 0,

            file_path=blob["url"],

            azure_version_id=blob["version_id"]

        )

        db.session.add(version)

        db.session.commit()

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

            document_name=version.document.title

        )

        return True