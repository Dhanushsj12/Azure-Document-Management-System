from datetime import datetime
from zoneinfo import ZoneInfo
from app.extensions import db


class Document(db.Model):

    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(255),
        nullable=False
    )

    latest_version = db.Column(
        db.Integer,
        default=1
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )

    owner = db.relationship(
        "User",
        backref="documents"
    )

    def __repr__(self):

        return f"<Document {self.title}>"