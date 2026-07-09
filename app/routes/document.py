import os
from io import BytesIO

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
from app.services.blob_service import BlobService
from app.services.audit_service import AuditService


document_bp = Blueprint(
    "document",
    __name__,
)


# -------------------------------------------------
# View Documents
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
# Upload
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
        Version.query.filter_by(
            document_id=id
        )
        .order_by(
            Version.version_number.desc()
        )
        .first()
    )

    blob_name = document.title

    data = BlobService.download_blob(
        blob_name
    )

    AuditService.log(
        current_user.id,
        "Download",
        document.title
    )

    return send_file(

        BytesIO(data),

        as_attachment=True,

        download_name=document.title,

        mimetype="application/octet-stream"

    )


# -------------------------------------------------
# Download Specific Version
# -------------------------------------------------
@document_bp.route("/download/version/<int:version_id>")
@login_required
def download_version(version_id):

    version = Version.query.get_or_404(version_id)

    document = version.document

    blob_name = document.title

    blob_client = BlobService.container_client.get_blob_client(
        blob_name,
        version_id=version.azure_version_id
    )

    data = blob_client.download_blob().readall()

    AuditService.log(
        current_user.id,
        "Download Version",
        document.title
    )

    return send_file(

        BytesIO(data),

        as_attachment=True,

        download_name=document.title,

        mimetype="application/octet-stream"

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
# Restore Version
# -------------------------------------------------
# ----------------------------------------
# Restore Previous Version
# ----------------------------------------
@document_bp.route("/restore/<int:version_id>")
@login_required
def restore_version(version_id):

    version = Version.query.get_or_404(version_id)

    document_id = version.document_id

    VersionService.restore(version_id)

    flash(
        "Version Restored Successfully.",
        "success"
    )

    return redirect(
        url_for(
            "document.history",
            id=document_id
        )
    )
# -------------------------------------------------
# Delete
# -------------------------------------------------
@document_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    document = Document.query.get_or_404(id)

    versions = Version.query.filter_by(
        document_id=id
    ).all()

    blob_name = document.title

    BlobService.delete_blob(
        blob_name
    )

    for version in versions:

        db.session.delete(version)

    db.session.delete(document)

    db.session.commit()

    AuditService.log(
        current_user.id,
        "Delete",
        document.title
    )

    flash(
        "Document Deleted Successfully",
        "success",
    )

    return redirect(
        url_for("document.documents")
    )