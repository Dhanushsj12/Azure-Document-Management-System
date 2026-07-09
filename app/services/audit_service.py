from app.extensions import db

from app.models.audit import Audit


class AuditService:

    @staticmethod
    def log(user_id, action, document_name=None):

        audit = Audit(

            user_id=user_id,

            action=action,

            document_name=document_name,

        )

        db.session.add(audit)

        db.session.commit()