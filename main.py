from flask import Flask,jsonify, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os
from moviepy_reel_generator import create_reel
from text_to_audio import text_to_speech_file
import shutil
from plyer import notification


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'user_uploads'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        print(request.files.keys())
        rec_id = request.form.get("uuid")
        desc = request.form.get("text")
        input_files = []

        for key, value in request.files.items():
            print(key, value)
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id)):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, filename))
                input_files.append(filename)

        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w") as f:
            f.write(desc)

        for fl in input_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt"), "a") as f:
                f.write(f"file '{fl}'\nduration1\n")

        text_to_speech_file(desc, rec_id)
        reel_path = create_reel(rec_id)
        
        dest_path = os.path.join("static/reels", f"{rec_id}.mp4")
        shutil.copy(reel_path, dest_path)

        print(f"Reel generated at: {reel_path}")
        print(f"Reel copied to: {dest_path}")
        notification.notify(
            title="Reel Generated!",
            message=f"Please check your generated reel in the gallery.",
            timeout=10
        )
    return render_template("create.html", myid=myid)


@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels=reels)


@app.route('/delete-reel/<filename>', methods=['DELETE'])
def delete_reel(filename):
    try:
        file_path = os.path.join("static/reels", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(debug=True)
