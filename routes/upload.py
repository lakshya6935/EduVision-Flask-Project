from flask import Blueprint, render_template, request, redirect, url_for
from services.upload_service import process_uploaded_file

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/input")
def upload_page():
    return render_template("upload.html")


@upload_bp.route("/upload", methods=["POST"])
def upload_data():
    file = request.files.get("file")

    if not file:
        return render_template("upload.html", error="No file uploaded.")

    try:
        process_uploaded_file(file)
        return redirect(url_for("analytics.analytics_dashboard"))
    except Exception as e:
        return render_template("upload.html", error=str(e))
