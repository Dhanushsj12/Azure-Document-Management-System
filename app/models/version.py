from datetime import datetime

from app.extensions import db


class Version(db.Model):

    __tablename__ = "versions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id"),
        nullable=False
    )

    version_number = db.Column(
        db.Integer,
        nullable=False
    )

    file_path = db.Column(
        db.String(500),
        nullable=False
    )

    file_size = db.Column(
        db.Integer
    )

    # Azure Blob Version ID
    azure_version_id = db.Column(
        db.String(255),
        nullable=True
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    document = db.relationship(
        "Document",
        backref="versions"
    )

    def __repr__(self):
        return (
            f"<Version {self.version_number} "
            f"AzureVersion={self.azure_version_id}>"
        )