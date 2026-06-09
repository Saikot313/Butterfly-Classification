
import os
import json
import time
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import io

# ── TensorFlow import (with graceful fallback) ──────────────────────────────
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
    print(f"TensorFlow {tf.__version__} loaded")
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not installed. Run: pip install tensorflow")


# App Configuration 
app = Flask(__name__, template_folder='classifier_UI', static_folder='classifier_UI', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

# Model config
IMG_SIZE = (128, 128)
MODEL_PATH = os.path.join('models', 'butterfly_cnn.h5')
CLASS_NAMES_PATH = os.path.join('models', 'class_names.json')

# Global model variables 
model = None
class_names = []


def load_ml_model():
    """Load CNN model and class names from disk."""
    global model, class_names

    if not TF_AVAILABLE:
        print("TensorFlow not available - model not loaded")
        return False

    # Load class names
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, 'r') as f:
            class_names = json.load(f)
        print(f"Class names loaded: {len(class_names)} species")
    else:
        print(f"class_names.json not found at {CLASS_NAMES_PATH}")
        print("   → Please run the Jupyter notebook (butterfly_cnn_training.ipynb) first!")
        return False

    # Load model
    if os.path.exists(MODEL_PATH):
        print(f"Loading model from {MODEL_PATH} ...")
        model = load_model(MODEL_PATH)
        print(f"Model loaded successfully!")
        return True
    else:
        print(f"Model not found at {MODEL_PATH}")
        print("   → Please run the Jupyter notebook first to train and save the model!")
        return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_bytes):
    """Convert raw image bytes to model-ready numpy array."""
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    original_size = img.size
    img = img.resize(IMG_SIZE)
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array, original_size


def predict_species(img_array, top_k=5):
    """Run inference and return top-k predictions."""
    if model is None:
        return None

    start = time.time()
    predictions = model.predict(img_array, verbose=0)[0]
    inference_ms = (time.time() - start) * 1000

    top_indices = predictions.argsort()[-top_k:][::-1]
    results = []
    for idx in top_indices:
        results.append({
            'rank': len(results) + 1,
            'species': class_names[idx],
            'confidence': float(predictions[idx]) * 100,
            'index': int(idx)
        })

    return results, round(inference_ms, 1)


# Routes 

@app.route('/')
def index():
    """Serve the main web app."""
    return render_template('index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


@app.route('/api/status', methods=['GET'])
def api_status():
    """Health check endpoint."""
    return jsonify({
        'status': 'online',
        'model_loaded': model is not None,
        'total_classes': len(class_names),
        'tensorflow_available': TF_AVAILABLE,
        'species_list': class_names
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint.
    Accepts: multipart/form-data with 'image' file field
    Returns: JSON with top-5 predictions and confidence scores
    """
    # Check model is loaded
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first using the Jupyter notebook.',
            'tip': 'Run butterfly_cnn_training.ipynb to train and save butterfly_cnn.h5'
        }), 503

    # Check file in request
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided. Send as form-data with key "image"'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'File type not allowed. Supported: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    try:
        # Read and preprocess image
        image_bytes = file.read()
        img_array, original_size = preprocess_image(image_bytes)

        # Run prediction
        predictions, inference_ms = predict_species(img_array, top_k=5)

        # Save uploaded file for display (optional)
        filename = secure_filename(file.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        with open(saved_path, 'wb') as f:
            f.write(image_bytes)

        fun_fact = {
    'DANAID EGGFLY': 'The male Danaid Eggfly is territorial and will chase away any intruder!',
    'MONARCH': 'Monarch butterflies migrate up to 3,000 miles every year!',
    'BLUE MORPHO': "The Blue Morpho's wings are not actually blue — it's an optical illusion!",
    'PAINTED LADY': 'The Painted Lady is the most widespread butterfly in the world!',
    'PEACOCK': 'The Peacock butterfly hibernates through winter as an adult!',
    'ZEBRA LONG WING': 'The Zebra Longwing is the official state butterfly of Florida!',
    'VICEROY': 'The Viceroy mimics the Monarch butterfly to avoid predators!',
    'PAPER KITE': 'The Paper Kite butterfly is often used in butterfly house displays!',
}

        top_species = predictions[0]['species']
        fact = fun_fact.get(top_species, f'The {top_species.title()} is one of 75 beautiful species our AI can identify!')
        
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'top_prediction': predictions[0],
            'fun_fact': fact,         
            'image_info': {
            'filename': filename,
            'original_size': original_size,
            'processed_size': IMG_SIZE,
    },
    'inference_time_ms': inference_ms,
    'model_info': f'CNN trained on {len(class_names)} butterfly species'
})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_shortcut():
    return predict()

@app.route('/api/species', methods=['GET'])
def get_species():
    """Return list of all recognizable butterfly species."""
    return jsonify({
        'total': len(class_names),
        'species': class_names
    })


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("\n" + "="*55)
    print(" Butterfly Classification - Flask API")
    print("="*55)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    model_loaded = load_ml_model()

    if not model_loaded:
        print("\nWARNING: Model not loaded!")
        print("   The server will start but /api/predict will return errors.")
        print("   Train the model first: open butterfly_cnn_training.ipynb\n")

    print("\nStarting server...")
    print("   URL: http://127.0.0.1:5000")
    print("   Press CTRL+C to stop\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
