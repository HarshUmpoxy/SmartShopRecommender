import pickle
import numpy as np
from numpy.linalg import norm
from flask import Blueprint, render_template, request, send_from_directory, url_for, current_app
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
import cv2
import io
import base64
import os

fashion_bp = Blueprint('fashion_bp', __name__, template_folder='templates')


print("Fashion BluePrint Called")
# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load precomputed data
features_file = os.path.join(current_dir, 'embeddings.pkl')
filenames_file = os.path.join(current_dir, 'filenames.pkl')

features_list = np.array(pickle.load(open(features_file, 'rb')))
filenames = pickle.load(open(filenames_file, 'rb'))

model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False

model = tf.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
neighbors.fit(features_list)

UPLOAD_FOLDER = 'uploads'
IMAGES_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_recommendations(image_data):
    img = image.load_img(io.BytesIO(image_data), target_size=(224, 224))  # Updated line
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocess_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocess_img).flatten()
    normalized_result = result / norm(result)

    distances, indices = neighbors.kneighbors([normalized_result])

    recommendations = []
    image_paths = []  # Initialize an empty list to store image paths

    for file_idx in indices[0][1:6]:
        recommendations.append(filenames[file_idx])
        normalized_path = filenames[file_idx].replace('\\', '/')  # Convert backslashes to forward slashes
        image_paths.append(normalized_path)

    print("total image path: ", image_paths)
    for i in image_paths:
        print("image_paths: ", i)
    return recommendations, image_paths  # Return both recommendations and image paths

@fashion_bp.route('/')
def index():
    print("route'/' called")
    return render_template('fashion.html')

@fashion_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_image_path = os.path.join(fashion_bp.root_path, 'uploads', filename)
    if os.path.exists(upload_image_path):
        return send_from_directory(os.path.join(fashion_bp.root_path, 'uploads'), filename)
    return "Image not found", 404

@fashion_bp.route('/images/<filename>')
def my_database_img_file(filename):
    return send_from_directory(os.path.join(fashion_bp.root_path, 'images'), filename)

@fashion_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        # Ensure the upload folder exists within the blueprint
        upload_folder = os.path.join(fashion_bp.root_path, 'uploads')  # Generate the correct path
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = os.path.join(upload_folder, file.filename)
        file.save(filename)
        return render_template('fashion.html', image_filename=file.filename)
    else:
        return "Invalid file format."
   

@fashion_bp.route('/recommend', methods=['POST'])
def recommend():
    image_filename = request.form.get('image_filename')
    print("image_filename inside recommend", image_filename)
    # image_path = os.path.join(fashion_bp.root_path, 'uploads', image_filename)
    image_path= 'fashion/uploads/'+image_filename
    # image_path = os.path.join(fashion_bp.config['UPLOAD_FOLDER'], image_filename)    
    print("image_path inside recommend ", image_path)
    with open(image_path, 'rb') as f:
        image_data = f.read()
        recommendations, image_paths = get_recommendations(image_data)
    
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    return render_template('result.html', image_base64=image_base64, image_paths=image_paths, recommendations=recommendations)
