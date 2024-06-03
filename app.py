import os
import numpy as np
from PIL import Image
import cv2
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model


# Load the model
model_path = r"C:\\Users\\aasma\\OneDrive\\Desktop\\VAC project -  local\\oct.h5"
model = load_model(model_path)

app = Flask(__name__)
print('Model loaded. Check http://127.0.0.1:5000/')


def get_className(classNo):
    if classNo == 0:
        return "Choroidal neovascularization (CNV)"
    elif classNo == 1:
        return "Diabetic macular edema (DME)"
    elif classNo == 2:
        return "Drusen"
    else:
        return "Normal"


def preprocess_image(image_path):
    # Read image using OpenCV
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert color from BGR to RGB
    image = cv2.resize(image, (256, 256))  # Resize to match the model's expected input
    image = np.array(image) / 255.0  # Normalize the image
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image


def classify_image(image_path):
    tensor = preprocess_image(image_path)
    pred = model.predict(tensor)
    label = np.argmax(pred, axis=1)[0]
    return label


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # Directory where the file will be stored
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)  # Create directory if it does not exist
        file_path = os.path.join(basepath, upload_folder, secure_filename(f.filename))
        f.save(file_path)

        class_no = classify_image(file_path)
        result = get_className(class_no)
        return result
    return None

if __name__ == '__main__':
    app.run(debug=True)
