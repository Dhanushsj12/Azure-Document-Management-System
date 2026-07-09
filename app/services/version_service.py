import os
import uuid

from app.extensions import db
from app.models.document import Document
from app.models.version import Version

# -------------------------------------------------
# Absolute Upload Folder
# -------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "app",
    "static",
    "uploads",
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class VersionService:

    @staticmethod
    def upload(file, user_id):

        # -----------------------------------------
        # Check whether document already exists
        # -----------------------------------------

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

                latest_version=1,

            )

            db.session.add(document)

            db.session.flush()

            version_number = 1

        # -----------------------------------------
        # Generate Unique Filename
        # -----------------------------------------

        extension = file.filename.rsplit(".", 1)[-1]

        unique_filename = f"{uuid.uuid4()}.{extension}"

        full_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename,
        )

        # -----------------------------------------
        # Save File
        # -----------------------------------------

        file.save(full_path)

        # -----------------------------------------
        # Save Version Information
        # -----------------------------------------

        version = Version(

            document_id=document.id,

            version_number=version_number,

            uploaded_by=user_id,

            file_size=os.path.getsize(full_path),

            file_path=full_path,

        )

        db.session.add(version)

        db.session.commit()

        return document