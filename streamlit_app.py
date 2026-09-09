import os
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image


# Page configuration
st.set_page_config(
    page_title="MNIST Digit Recognition",
    page_icon="🔢",
    layout="centered"
)

st.title("MNIST Digit Recognition")
st.write("Upload an image of a handwritten digit and let the model predict it.")

# Path to saved model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.keras")


@st.cache_resource
def load_model():
    """Load the trained MNIST model once."""
    return tf.keras.models.load_model(MODEL_PATH)


# Load model
try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()


# Upload image
uploaded_file = st.file_uploader(
    "Upload a handwritten digit image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    # Open image and convert to grayscale
    image = Image.open(uploaded_file).convert("L")

    # Display uploaded image
    st.image(
        image,
        caption="Uploaded digit",
        width=250
    )

    # Resize to MNIST format
    image = image.resize((28, 28), Image.Resampling.BILINEAR)

    # Convert image to NumPy array
    img_array = np.array(image, dtype=np.float32)

    # Normalize pixel values from 0-255 to 0-1
    img_array = img_array / 255.0

    # Reshape to CNN input format
    img_tensor = img_array.reshape(1, 28, 28, 1)

    # Make prediction
    predictions = model(img_tensor, training=False).numpy()[0]

    # Get predicted digit
    predicted_digit = int(np.argmax(predictions))

    # Get confidence
    confidence = float(np.max(predictions) * 100)

    # Display result
    st.success(f"Prediction: {predicted_digit}")
    st.info(f"Confidence: {confidence:.1f}%")