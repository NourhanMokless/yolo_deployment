from flask import Flask, render_template, request
from ultralytics import YOLO
from PIL import Image
import os
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": ""}})

def predict_disease(image_path):
    model = YOLO('yolov8n-cls.pt')
    with Image.open(image_path) as img:
        img = img.resize((255, 255))
    results = model(img, show=True)
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()
    print(f"Probabilities: {probs}")
    print(f"Max Probability: {max(probs)}")
    if max(probs) > 0.90:  # Lowered threshold to 0.90
       return "no disease is found"
    else:
      prediction = names_dict[probs.index(max(probs))]
      return f'leaf has {prediction} disease'


@app.route('/')
def index():
    return render_template('index.html', prediction=None)

@app.route('/predict/', methods=['POST','GET'])
def predict():
    file = request.files['image']
    image_path = 'temp_image.jpg'
    file.save(image_path)
    prediction = predict_disease(image_path)
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)


##################################################################
# from flask import Flask, render_template, request
# from ultralytics import YOLO
# from PIL import Image
# import os
# import numpy as np
# from flask_cors import CORS

# app = Flask(__name__)
# cors = CORS(app, resources={r"/": {"origins": ""}})

# def predict_disease(image_path):
#     model = YOLO('yolov8n-cls.pt')
#     with Image.open(image_path) as img:
#         img = img.resize((255, 255))
#     results = model(img, show=True)
#     names_dict = results[0].names
#     probs = results[0].probs.data.tolist()
#     print(probs)
#     print(max(probs))
#     if max(probs) > 0.80:
#         return "no disease is found"
#     else:
#         prediction = names_dict[probs.index(max(probs))]
#         return f'leaf has {prediction} disease'

# @app.route('/')
# def index():
#     return render_template('index.html', prediction=None)

# @app.route('/predict/', methods=['POST','GET'])
# def predict():
#     file = request.files['image']
#     image_path = 'temp_image.jpg'
#     file.save(image_path)
#     prediction = predict_disease(image_path)
#     return render_template('index.html', prediction=prediction)

# if __name__ == '__main__':
#     app.run(debug=True)

