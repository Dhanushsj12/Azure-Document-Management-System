from flask import Blueprint, render_template
from flask_login import login_required

from app.models.user import User
from app.models.document import Document
from app.models.version import Version

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    total_users = User.query.count()

    total_documents = Document.query.count()

    total_versions = Version.query.count()

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_documents=total_documents,
        total_versions=total_versions,
    )