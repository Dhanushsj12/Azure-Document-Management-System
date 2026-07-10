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

    # Calculate total storage used
    total_storage = (
        sum(v.file_size or 0 for v in Version.query.all())
        / (1024 * 1024)
    )

    # Recent uploads
    recent_uploads = (
        Version.query.order_by(
            Version.uploaded_at.desc()
        )
        .limit(5)
        .all()
    )

    return render_template(

        "dashboard.html",

        total_users=total_users,

        total_documents=total_documents,

        total_versions=total_versions,

        total_storage=round(total_storage, 2),

        recent_uploads=recent_uploads,

    )