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

from app.models.document import Document
from app.services.version_service import VersionService

document_bp = Blueprint(
    "document",
    __name__,
)


# -----------------------------
# View All Documents
# -----------------------------
@document_bp.route("/documents")
@login_required
def documents():

    documents = Document.query.order_by(
        Document.created_at.desc()
    ).all()

    return render_template(
        "documents.html",
        documents=documents,
    )


# -----------------------------
# Upload Document
# -----------------------------
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


# -----------------------------
# Download Document
# -----------------------------
@document_bp.route("/download/<int:id>")
@login_required
def download(id):

    document = Document.query.get_or_404(id)

    latest_version = sorted(
        document.versions,
        key=lambda x: x.version_number,
        reverse=True,
    )[0]

    return send_file(
        latest_version.file_path,
        as_attachment=True,
        download_name=document.title,
    )


# -----------------------------
# Delete Document
# -----------------------------
@document_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    document = Document.query.get_or_404(id)

    # Delete all version files
    for version in document.versions:

        if os.path.exists(version.file_path):
            os.remove(version.file_path)

    # Delete database records
    from app.extensions import db

    for version in document.versions:
        db.session.delete(version)

    db.session.delete(document)

    db.session.commit()

    flash(
        "Document Deleted Successfully",
        "success",
    )

    return redirect(
        url_for("document.documents"),
    )