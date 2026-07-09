import os

from werkzeug.utils import secure_filename

from app.extensions import db

from app.models.document import Document


UPLOAD_FOLDER = "app/static/uploads"


class DocumentService:

    @staticmethod
    def upload(file, user_id):

        filename = secure_filename(file.filename)

        path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(path)

        document = Document(

            filename=filename,

            original_filename=file.filename,

            file_size=os.path.getsize(path),

            uploaded_by=user_id,

            file_path=path,

        )

        db.session.add(document)

        db.session.commit()

        return document

    @staticmethod
    def get_all():

        return Document.query.order_by(
            Document.uploaded_at.desc()
        ).all()

    @staticmethod
    def delete(document):

        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        db.session.delete(document)

        db.session.commit()