from flask import (
    Blueprint,
    render_template,
)

from flask_login import login_required

from app.models.audit import Audit

audit_bp = Blueprint(
    "audit",
    __name__,
)


@audit_bp.route("/audit")
@login_required
def audit_logs():

    logs = (
        Audit.query
        .order_by(Audit.timestamp.desc())
        .all()
    )

    return render_template(
        "audit_logs.html",
        logs=logs,
    )