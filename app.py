import os
import io
import base64
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
import tensorflow as tf

# Initialize Flask application
app = Flask(__name__)

# Path to saved model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.keras')

# Load trained TensorFlow/Keras model when app starts
print("Loading trained MNIST model...")

if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")

    # Warm up TensorFlow with one dummy prediction.
    # This avoids doing model initialization during the first user request.
    dummy_input = np.zeros((1, 28, 28, 1), dtype=np.float32)
    model(dummy_input, training=False)

    print("Model warm-up completed!")
else:
    model = None
    print("Warning: model.keras not found! Please run train_model.py first.")


@app.route('/')
def home():
    """Render the main frontend page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Receive canvas drawing as base64 PNG,
    preprocess it to 28x28,
    run the trained model,
    and return digit + confidence.
    """

    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please train model first.'
        }), 500

    try:
        # Get JSON data from frontend
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({
                'error': 'No image data provided'
            }), 400

        image_data = data['image']

        # Remove base64 header if present
        if ',' in image_data:
            image_data = image_data.split(',', 1)[1]

        # Decode base64 image
        image_bytes = base64.b64decode(image_data)

        # Open image using Pillow
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to grayscale
        image = image.convert('L')

        # Resize to MNIST format
        image = image.resize((28, 28), Image.Resampling.BILINEAR)

        # Convert to NumPy array
        img_array = np.array(image, dtype=np.float32)

        # Normalize pixel values
        img_array = img_array / 255.0

        # Reshape to model input shape
        img_tensor = img_array.reshape(1, 28, 28, 1)

        # Direct model inference
        # This is lighter/faster than model.predict() for one image.
        predictions = model(img_tensor, training=False).numpy()[0]

        # Get predicted digit
        predicted_digit = int(np.argmax(predictions))

        # Get confidence
        confidence = float(np.max(predictions) * 100)

        return jsonify({
            'prediction': predicted_digit,
            'confidence': round(confidence, 1)
        })

    except Exception as e:
        print(f"Error processing prediction: {e}")

        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Render provides PORT automatically.
    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )