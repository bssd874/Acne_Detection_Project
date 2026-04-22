from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os

from utils import SkinValidatorSimple, ACNE_SOLUTIONS

app = Flask(__name__)
CORS(app)  # Enable CORS untuk frontend

# Konfigurasi
MODEL_PATH = 'model/acne_model_best (1).keras'
IMG_HEIGHT = 224
IMG_WIDTH = 224
CLASS_NAMES = ['blackheads', 'papules', 'pustules', 'cysts','whiteheads']
CONFIDENCE_THRESHOLD = 0.6

# Load model
print("⏳ Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print(f"✅ Model loaded! Output shape: {model.output_shape}")
print(f"✅ Classes: {CLASS_NAMES}")

# Inisialisasi validator
validator = SkinValidatorSimple()

def preprocess_image(image_bytes):
    """Preprocess gambar dari bytes"""
    # Convert bytes ke numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Acne Detection API is running!',
        'endpoints': {
            'predict': 'POST /predict - Upload gambar untuk prediksi',
            'health': 'GET /health - Cek status API'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'classes': CLASS_NAMES
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Cek ada file gak
        if 'image' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'Tidak ada file gambar. Gunakan key "image" untuk upload.'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'File kosong.'
            }), 400
        
        # Baca gambar
        image_bytes = file.read()
        img = preprocess_image(image_bytes)
        
        # Validasi
        is_valid, message = validator.validate_image(img)
        
        if not is_valid:
            return jsonify({
                'status': 'error',
                'type': 'not_human_skin',
                'message': message,
                'tip': 'Pastikan upload foto wajah atau kulit manusia yang jelas. Hindari foto binatang, benda, atau pemandangan.'
            }), 400
        
        # Preprocess untuk model
        img_resized = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
        img_normalized = img_resized / 255.0
        img_expanded = np.expand_dims(img_normalized, axis=0)
        
        # Prediksi
        predictions = model.predict(img_expanded, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])
        
        # Cek confidence threshold
        if confidence < CONFIDENCE_THRESHOLD:
            all_probs = {CLASS_NAMES[i]: float(predictions[0][i]) for i in range(len(CLASS_NAMES))}
            return jsonify({
                'status': 'uncertain',
                'message': 'Model tidak yakin dengan gambar ini',
                'confidence': confidence,
                'predicted_class': CLASS_NAMES[predicted_idx],
                'all_probabilities': all_probs,
                'tip': 'Coba upload foto dengan kualitas lebih baik, pencahayaan cukup, dan fokus pada area jerawat.'
            }), 200
        
        # Success
        predicted_class = CLASS_NAMES[predicted_idx]
        solution = ACNE_SOLUTIONS.get(predicted_class, {})
        
        all_probs = {CLASS_NAMES[i]: float(predictions[0][i]) for i in range(len(CLASS_NAMES))}
        
        # Convert gambar ke base64 buat display di frontend
        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'predicted_class': predicted_class,
            'class_name': solution.get('name', predicted_class),
            'confidence': confidence,
            'all_probabilities': all_probs,
            'description': solution.get('description', ''),
            'causes': solution.get('causes', []),
            'solutions': solution.get('solutions', []),
            'ingredients': solution.get('ingredients', []),
            'products': solution.get('products', []),
            'warning': solution.get('warning', None),
            'validation_message': message,
            'image_base64': img_base64  # Gambar yang diupload (opsional)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Pastikan folder model ada
    os.makedirs('model', exist_ok=True)
    
    print("🚀 Starting Acne Detection API...")
    print(f"📊 Model: {MODEL_PATH}")
    print(f"🎯 Classes: {CLASS_NAMES}")
    print(f"🔧 Confidence threshold: {CONFIDENCE_THRESHOLD}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)