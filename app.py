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
else:
    model = None
    print("Warning: model.keras not found! Please run train_model.py first.")

@app.route('/')
def home():
    """Renders the main frontend HTML page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives canvas drawing as base64 PNG, preprocesses image into (1, 28, 28, 1) tensor,
    runs CNN prediction, and returns predicted digit + confidence score as JSON.
    """
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train model first.'}), 500

    try:
        # Get JSON data from POST request
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        image_data = data['image']

        # Remove header 'data:image/png;base64,' if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        # Decode base64 string to bytes
        image_bytes = base64.b64decode(image_data)

        # Open image using Pillow
        image = Image.open(io.BytesIO(image_bytes))

        # Convert image to Grayscale ('L')
        image = image.convert('L')

        # Resize image to 28x28 pixels (MNIST target input size)
        image = image.resize((28, 28), Image.Resampling.BILINEAR)

        # Convert PIL Image to numpy array
        img_array = np.array(image, dtype=np.float32)

        # Normalize pixel values from [0, 255] to [0.0, 1.0] (matching Project.ipynb)
        img_array = img_array / 255.0

        # Reshape array to (1, 28, 28, 1) matching the CNN input shape
        img_tensor = img_array.reshape(1, 28, 28, 1)

        # Perform prediction
        predictions = model.predict(img_tensor, verbose=0)[0]

        # Get predicted digit (index of highest probability)
        predicted_digit = int(np.argmax(predictions))

        # Get confidence percentage
        confidence = float(np.max(predictions) * 100)

        # Return prediction and confidence as JSON
        return jsonify({
            'prediction': predicted_digit,
            'confidence': round(confidence, 1)
        })

    except Exception as e:
        print(f"Error processing prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Listen on Render-provided PORT variable, defaulting to 5000 for local testing
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
