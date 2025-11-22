import os
from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "user_uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods = ["GET", "POST"])
def create():
    my_id = uuid.uuid1()
    if request.method == "POST":
        user_id = request.form.get("myId")
        desc = request.form.get("text")

        # Create user folder
        folder_name = os.path.join(app.config["UPLOAD_FOLDER"], user_id)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        input_files = []

        # Upload files
        for key, file in request.files.items():
            if file:
                file_name = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], user_id, file_name))
                input_files.append(file_name)
        # Save Text
        with open(os.path.join(folder_name, "description.txt"), "w") as text_file:
            text_file.write(desc)

        for input_file in input_files:
            with open(os.path.join(app.config["UPLOAD_FOLDER"], user_id, "input.txt"), "a") as f:
                f.write(f"file '{input_file}'\nduration 1\n")

    return render_template("create.html", myId = my_id)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels = reels)

app.run(debug=True)