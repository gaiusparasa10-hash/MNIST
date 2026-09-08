# MNIST Handwritten Digit Recognition Web Application

A simple, beginner-friendly web application that allows users to draw handwritten digits (0–9) on an interactive canvas and get real-time predictions powered by a Convolutional Neural Network (CNN) trained on the MNIST dataset.

Built with **HTML, CSS, JavaScript** on the frontend and **Python Flask** on the backend. Fully ready for deployment on **Render**.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How the Machine Learning Model Works](#how-the-machine-learning-model-works)
- [How the Frontend Works](#how-the-frontend-works)
- [How the Flask Backend Works](#how-the-flask-backend-works)
- [Application Workflow](#application-workflow)
- [Project Structure](#project-structure)
- [How to Run Locally](#how-to-run-locally)
- [Deployment on Render](#deployment-on-render)
- [Technical Interview Talking Points](#technical-interview-talking-points)

---

## Project Overview

This project converts the exploratory machine learning experiments in `Project.ipynb` into an interactive, end-to-end web application. The core objective is to bridge the gap between machine learning model training and real-world deployment with clean, understandable code.

---

## Features
- **Interactive HTML5 Canvas**: Smooth drawing experience with mouse or touch support.
- **Real-Time Prediction**: Sends drawn digits to the backend Flask API and receives instant predictions.
- **Confidence Score Display**: Shows prediction confidence percentage alongside predicted digit.
- **One-Click Clear**: Easily clear canvas to draw another digit.
- **Beginner-Friendly Architecture**: Lightweight, dependency-minimal setup without bloated JS frameworks or databases.

---

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Backend Framework**: Python Flask
- **Machine Learning**: TensorFlow / Keras, NumPy, Pillow (PIL)
- **Production Server**: Gunicorn (WSGI server for Render deployment)

---

## How the Machine Learning Model Works

The machine learning logic is based directly on `Project.ipynb` (Cell 2).

1. **Dataset**: The model is trained on the standard **MNIST handwritten digit dataset** (60,000 training images, 10,000 test images of size 28x28 pixels).
2. **Architecture**: A Convolutional Neural Network (CNN) implemented with TensorFlow/Keras:
   - `Conv2D (32 filters, 3x3 kernel, ReLU activation)`: Extracts low-level visual features like edges and curves.
   - `MaxPooling2D (2x2)`: Downsamples spatial dimensions to reduce computation and prevent overfitting.
   - `Conv2D (64 filters, 3x3 kernel, ReLU activation)`: Extracts higher-level digit features.
   - `MaxPooling2D (2x2)`: Second pooling layer.
   - `Flatten()`: Converts 2D feature maps into a 1D vector.
   - `Dense (128 units, ReLU activation)`: Fully connected layer for pattern learning.
   - `Dropout (0.5)`: Randomly drops 50% of neurons during training to prevent overfitting.
   - `Dense (10 units, Softmax activation)`: Output layer producing class probabilities for digits `0` through `9`.
3. **Training & Persistence**: The model is trained for 5 epochs with Adam optimizer and Categorical Cross-Entropy loss, achieving ~99% accuracy. The trained model is saved to `model.keras`.

---

## How the Frontend Works

1. **HTML5 Canvas (`<canvas>`)**: Rendered at `280x280` pixels with a black background (`#000000`) and white stroke (`#ffffff`), matching the MNIST dataset appearance.
2. **User Interaction (`script.js`)**:
   - Listens to mouse (`mousedown`, `mousemove`, `mouseup`) and touch events (`touchstart`, `touchmove`, `touchend`).
   - Draws white strokes with round line caps (`lineWidth = 18`).
3. **Data Transfer**:
   - When the user clicks **Predict**, `canvas.toDataURL('image/png')` converts the canvas drawing into a base64-encoded PNG string.
   - A `fetch()` POST request sends `{ "image": dataUrl }` to the `/predict` API endpoint.
4. **UI Update**: Receives JSON response and displays predicted digit and confidence score.

---

## How the Flask Backend Works

1. **Model Loading (`app.py`)**: Upon server startup, Flask loads `model.keras` into memory.
2. **Endpoint `/predict` (POST)**:
   - Receives JSON payload containing base64 PNG string.
   - **Image Preprocessing Pipeline**:
     1. Decodes base64 string into binary bytes.
     2. Opens image using `Pillow (PIL)` and converts to Grayscale (`'L'`).
     3. Resizes image to `28x28` pixels (matching model input shape).
     4. Normalizes pixel values from `[0, 255]` range to `[0.0, 1.0]` by dividing by `255.0`.
     5. Reshapes array into 4D tensor `(1, 28, 28, 1)` matching CNN input expectations.
   - Runs `model.predict(img_tensor)` to get probability distribution across 10 classes.
   - Finds index of maximum probability (`np.argmax()`) and formats confidence (`max_prob * 100`).
   - Returns JSON: `{"prediction": 7, "confidence": 96.4}`.

---

## Application Workflow

```
[ User Draws Digit ]
         │
         ▼
[ Click "Predict" Button ]
         │
         ▼
[ Convert Canvas -> Base64 PNG ]
         │
         ▼
[ POST /predict (Flask API) ]
         │
         ▼
[ Preprocessing: Grayscale -> Resize (28x28) -> Normalize -> Reshape (1,28,28,1) ]
         │
         ▼
[ Model Inference (model.keras) ]
         │
         ▼
[ Return JSON: { "prediction": 7, "confidence": 96.4 } ]
         │
         ▼
[ Update UI Display ]
```

---

## Project Structure

```
MNIST/
│
├── app.py              # Main Flask web application server
├── train_model.py      # Script to train CNN model and save model.keras
├── Project.ipynb       # Original ML exploration notebook
├── README.md           # Documentation & setup guide
├── requirements.txt    # Python dependencies
├── model.keras         # Trained CNN model file
│
├── templates/
│   └── index.html      # Frontend HTML template
│
└── static/
    ├── style.css       # Frontend CSS styling
    └── script.js       # Frontend JavaScript (canvas drawing & API calls)
```

---

## How to Run Locally

### Prerequisites
- Python 3.9 – 3.12 installed.

### Step-by-Step Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gaiusparasa10-hash/MNIST.git
   cd MNIST
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train and Save Model (If model.keras is missing)**:
   ```bash
   python train_model.py
   ```

5. **Run Flask Application**:
   ```bash
   python app.py
   ```

6. **Open in Browser**:
   Navigate to `http://127.0.0.1:5000` in your web browser.

---

## Deployment on Render

This application is fully compatible with **Render Web Services**.

### Exact Render Settings

- **Environment**: Python 3
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  gunicorn app:app
  ```

### Why Port Configuration Matters:
In `app.py`, the server dynamically binds to the `PORT` environment variable supplied by Render:
```python
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```

---

## Technical Interview Talking Points

- **Why CNN over classical ML (Logistic Regression/KNN)?**
  - Spatial invariance: CNNs preserve 2D grid structure of image pixels through convolutional filters, making them significantly better at handling shifted or varied handwriting styles compared to flat vector models like Logistic Regression or KNN.
- **How is image preprocessing handled between Frontend and Backend?**
  - The canvas renders a high-res 280x280 drawing for smooth UX. The backend resizes this down to 28x28, converts to grayscale, and divides pixel intensities by 255.0 to mirror the exact preprocessing applied during MNIST dataset training.
- **Why use base64 encoding for image transfer?**
  - Base64 encoding allows transmitting drawing canvas image data directly as an inline payload over standard JSON HTTP POST requests without writing temporary files to server disk.
