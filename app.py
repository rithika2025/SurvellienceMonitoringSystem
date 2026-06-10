from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load trained model
model = tf.keras.models.load_model("model.h5")

classes = ["Non Violence", "Violence"]


def predict_video(video_path):

    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()

    if not ret:
        return "Video cannot be read"

    # resize frame
    frame = cv2.resize(frame, (224, 224))

    # normalize
    frame = frame / 255.0

    # convert to numpy
    frame = np.array(frame)

    # add dimension
    frame = np.expand_dims(frame, axis=0)

    # prediction
    prediction = model.predict(frame)

    result = classes[np.argmax(prediction)]

    cap.release()

    return result


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "video" not in request.files:
        return "No video uploaded"

    file = request.files["video"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    result = predict_video(filepath)

    return "<h2>Prediction Result: " + result + "</h2>"


if __name__ == "__main__":

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    app.run(debug=True)