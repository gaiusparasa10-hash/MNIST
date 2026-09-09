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


# Initialize session state
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None


st.subheader("Draw a digit")

canvas_result = st_canvas(
    fill_color="black",
    stroke_width=18,
    stroke_color="white",
    background_color="black",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key=f"canvas_{st.session_state.canvas_key}",
    return_image_data=True,
)


col1, col2 = st.columns(2)

with col1:
    predict_clicked = st.button("Predict")

with col2:
    clear_clicked = st.button("Clear")


# Clear canvas and prediction
if clear_clicked:
    st.session_state.canvas_key += 1
    st.session_state.prediction = None
    st.session_state.confidence = None
    st.rerun()


# Predict digit
if predict_clicked:
    try:
        image = canvas_result.image_data

        if image is None or np.max(image[:, :, :3]) == 0:
            st.warning("Please draw a digit first.")
            st.stop()

        # Convert canvas RGBA image to grayscale
        image = Image.fromarray(image.astype(np.uint8)).convert("L")

        # Find the bounding box of the handwritten digit
        image_array = np.array(image)

        rows = np.any(image_array > 20, axis=1)
        cols = np.any(image_array > 20, axis=0)

        if not rows.any() or not cols.any():
            st.warning("Please draw a digit first.")
            st.stop()

        top, bottom = np.where(rows)[0][[0, -1]]
        left, right = np.where(cols)[0][[0, -1]]

        # Crop the digit
        image = image.crop((left, top, right + 1, bottom + 1))

        # Add padding around the digit
        width, height = image.size
        padding = int(max(width, height) * 0.2)

        padded = Image.new(
            "L",
            (width + padding * 2, height + padding * 2),
            0
        )

        padded.paste(image, (padding, padding))

        # Resize to MNIST format
        image = padded.resize((28, 28), Image.Resampling.LANCZOS)

        # Normalize pixel values
        img_array = np.array(image, dtype=np.float32) / 255.0

        # Add batch and channel dimensions
        img_tensor = img_array.reshape(1, 28, 28, 1)

        # Make prediction
        predictions = model(img_tensor, training=False).numpy()[0]

        predicted_digit = int(np.argmax(predictions))
        confidence = float(np.max(predictions) * 100)

        # Store prediction in session state
        st.session_state.prediction = predicted_digit
        st.session_state.confidence = confidence

    except Exception as e:
        st.error(f"Prediction error: {e}")


# Display prediction result
if st.session_state.prediction is not None:
    st.success(f"Prediction: {st.session_state.prediction}")
    st.info(f"Confidence: {st.session_state.confidence:.1f}%")