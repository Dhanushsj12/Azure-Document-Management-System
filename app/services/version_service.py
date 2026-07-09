import os
import uuid

from app.extensions import db

from app.models.document import Document

from app.models.version import Version


UPLOAD_FOLDER = "app/static/uploads"


class VersionService:

    @staticmethod
    def upload(file, user_id):

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

        extension = file.filename.split(".")[-1]

        unique_name = f"{uuid.uuid4()}.{extension}"

        path = os.path.join(
            UPLOAD_FOLDER,
            unique_name
        )

        file.save(path)

        version = Version(

            document_id=document.id,

            version_number=version_number,

            uploaded_by=user_id,

            file_size=os.path.getsize(path),

            file_path=path

        )

        db.session.add(version)

        db.session.commit()

        return document