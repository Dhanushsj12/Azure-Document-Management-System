import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
)

from flask_login import (
    login_required,
    current_user,
)

from app.extensions import db
from app.models.document import Document
from app.models.version import Version
from app.services.version_service import VersionService
from app.services.audit_service import AuditService

document_bp = Blueprint(
    "document",
    __name__,
)


# -------------------------------------------------
# View All Documents + Search
# -------------------------------------------------
@document_bp.route("/documents")
@login_required
def documents():

    search = request.args.get("search", "").strip()

    if search:

        documents = (
            Document.query.filter(
                Document.title.ilike(f"%{search}%")
            )
            .order_by(Document.created_at.desc())
            .all()
        )

    else:

        documents = (
            Document.query.order_by(
                Document.created_at.desc()
            ).all()
        )

    return render_template(
        "documents.html",
        documents=documents,
        search=search,
    )


# -------------------------------------------------
# Upload Document
# -------------------------------------------------
@document_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        file = request.files.get("document")

        if file and file.filename != "":

            VersionService.upload(
                file,
                current_user.id,
            )

            # -----------------------------
            # Audit Log
            # -----------------------------
            AuditService.log(
                user_id=current_user.id,
                action="Upload",
                document_name=file.filename,
            )

            flash(
                "Document Uploaded Successfully",
                "success",
            )

            return redirect(
                url_for("document.documents")
            )

        flash(
            "Please choose a file.",
            "warning",
        )

    return render_template(
        "upload.html",
    )


# -------------------------------------------------
# Download Latest Version
# -------------------------------------------------
@document_bp.route("/download/<int:id>")
@login_required
def download(id):

    document = Document.query.get_or_404(id)

    latest_version = (
        Version.query.filter_by(document_id=id)
        .order_by(Version.version_number.desc())
        .first()
    )

    # -----------------------------
    # Audit Log
    # -----------------------------
    AuditService.log(
        user_id=current_user.id,
        action="Download",
        document_name=document.title,
    )

    return send_file(
        latest_version.file_path,
        as_attachment=True,
        download_name=document.title,
    )


# -------------------------------------------------
# Download Specific Version
# -------------------------------------------------
@document_bp.route("/download/version/<int:version_id>")
@login_required
def download_version(version_id):

    version = Version.query.get_or_404(version_id)

    document = Document.query.get_or_404(
        version.document_id
    )

    # -----------------------------
    # Audit Log
    # -----------------------------
    AuditService.log(
        user_id=current_user.id,
        action=f"Download Version {version.version_number}",
        document_name=document.title,
    )

    return send_file(
        version.file_path,
        as_attachment=True,
        download_name=document.title,
    )


# -------------------------------------------------
# Version History
# -------------------------------------------------
@document_bp.route("/history/<int:id>")
@login_required
def history(id):

    document = Document.query.get_or_404(id)

    versions = (
        Version.query.filter_by(
            document_id=id
        )
        .order_by(
            Version.version_number.desc()
        )
        .all()
    )

    return render_template(
        "version_history.html",
        document=document,
        versions=versions,
    )


# -------------------------------------------------
# Delete Document
# -------------------------------------------------
@document_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    document = Document.query.get_or_404(id)

    # Save title before deleting
    document_title = document.title

    versions = Version.query.filter_by(
        document_id=id
    ).all()

    for version in versions:

        if (
            version.file_path
            and os.path.exists(version.file_path)
        ):
            os.remove(version.file_path)

        db.session.delete(version)

    db.session.delete(document)

    db.session.commit()

    # -----------------------------
    # Audit Log
    # -----------------------------
    AuditService.log(
        user_id=current_user.id,
        action="Delete",
        document_name=document_title,
    )

    flash(
        "Document Deleted Successfully",
        "success",
    )

    return redirect(
        url_for("document.documents")
    )