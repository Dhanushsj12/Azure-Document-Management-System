import uuid
import os

from app.extensions import db
from app.models.document import Document
from app.models.version import Version
from app.services.blob_service import BlobService
from app.services.audit_service import AuditService


class VersionService:

    @staticmethod
    def upload(file, user_id):

        # Find existing document
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

        # Create unique blob filename

        extension = os.path.splitext(file.filename)[1]

        unique_name = f"{uuid.uuid4()}{extension}"

        # Upload to Azure Blob Storage

        blob_url = BlobService.upload_file(
            file,
            unique_name
        )

        # Store metadata

        version = Version(

            document_id=document.id,

            version_number=version_number,

            uploaded_by=user_id,

            file_size=file.content_length if file.content_length else 0,

            file_path=blob_url

        )

        db.session.add(version)

        db.session.commit()

        AuditService.log(

            user_id=user_id,

            action="Upload",

            document_name=document.title

        )

        return document