import os
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="MNIST Digit Recognition",
    page_icon="🔢",
    layout="centered"
)

st.title("MNIST Digit Recognition")
st.write("Draw a handwritten digit below and let the model predict it.")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.keras")


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()


st.subheader("Draw a digit")

canvas_result = st_canvas(
    fill_color="black",
    stroke_width=18,
    stroke_color="white",
    background_color="black",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)


if st.button("Predict"):
    if canvas_result.image_data is not None:

        image = canvas_result.image_data.astype(np.uint8)

        # Convert RGBA image to grayscale
        image = Image.fromarray(image).convert("L")

        # Resize to MNIST format
        image = image.resize((28, 28), Image.Resampling.BILINEAR)

        # Normalize pixel values
        img_array = np.array(image, dtype=np.float32) / 255.0

        # Add batch and channel dimensions
        img_tensor = img_array.reshape(1, 28, 28, 1)

        # Prediction
        predictions = model(img_tensor, training=False).numpy()[0]

        predicted_digit = int(np.argmax(predictions))
        confidence = float(np.max(predictions) * 100)

        st.success(f"Prediction: {predicted_digit}")
        st.info(f"Confidence: {confidence:.1f}%")