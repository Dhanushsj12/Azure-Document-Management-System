from datetime import datetime

from app.extensions import db


class Audit(db.Model):

    __tablename__ = "audits"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    action = db.Column(
        db.String(100),
        nullable=False
    )

    document_name = db.Column(
        db.String(255)
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="audit_logs"
    )

    def __repr__(self):

        return f"<Audit {self.action}>"