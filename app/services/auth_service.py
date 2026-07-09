from app.extensions import db
from app.extensions import bcrypt

from app.models.user import User


class AuthService:

    @staticmethod
    def register_user(name, email, password):

        existing = User.query.filter_by(email=email).first()

        if existing:
            return None

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            full_name=name,
            email=email,
            password=hashed,
        )

        db.session.add(user)

        db.session.commit()

        return user

    @staticmethod
    def authenticate(email, password):

        user = User.query.filter_by(email=email).first()

        if not user:
            return None

        if bcrypt.check_password_hash(user.password, password):
            return user

        return None