from flask import Flask, render_template, redirect, url_for
from camera.camera import capture_image
from ocr.plate_reader import read_number_plate
from database.db import insert_record, fetch_records
from database.db import clear_records
from flask import request
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/records")
def records():
    data = fetch_records()
    return render_template("records.html", records=data)

@app.route("/clear")
def clear_all():
    clear_records()
    return redirect(url_for("records"))

@app.route("/upload", methods=["POST"])
def upload_image():
    image_data = request.data

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"esp32_{timestamp}.jpg"

    save_path = os.path.join("static", "images", "captures", filename)

    with open(save_path, "wb") as f:
        f.write(image_data)

    # Now reuse your pipeline
    plate = read_number_plate(save_path)
    if plate is None:
        plate = "NOT_DETECTED"

    insert_record(plate, save_path)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)