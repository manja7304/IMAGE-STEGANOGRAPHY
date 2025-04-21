import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from steganography import create_image, decode_image

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png"}

# Create upload folder if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def home():
    return render_template("steganography_ui_final.html")


@app.route("/encode", methods=["POST"])
def encode():
    if "image" not in request.files or "secret_message" not in request.form:
        return "Missing image or message!"

    image = request.files["image"]
    secret_message = request.form["secret_message"]

    if image.filename == "" or not allowed_file(image.filename):
        return "Invalid image format! PNG only."

    filename = secure_filename(image.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(path):
        os.remove(path)

    image.save(path)

    # Apply steganography
    create_image(secret_message, path)

    return render_template(
        "steganography_ui_final.html", message=secret_message, img_path="/" + path
    )


@app.route("/decode", methods=["POST"])
def decode():
    if "image" not in request.files:
        return "Missing image!"

    image = request.files["image"]

    if image.filename == "":
        return "No file selected."

    filename = secure_filename(image.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(path)

    # Decode message
    secret = decode_image(path)

    return render_template("steganography_ui_final.html", secret=secret)


if __name__ == "__main__":
    app.run(debug=True)
