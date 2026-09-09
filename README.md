# MNIST Handwritten Digit Recognition Web Application

🚀 **[Live Demo](https://2pm9xwx3qcruqqxmqh6mtv.streamlit.app/)**

A simple, beginner-friendly web application that allows users to draw handwritten digits (0–9) on an interactive canvas and get predictions powered by a Convolutional Neural Network (CNN) trained on the MNIST dataset.

Built with **Python, Streamlit, TensorFlow/Keras, NumPy, and Pillow**.


---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How the Machine Learning Model Works](#how-the-machine-learning-model-works)
- [How the Web Application Works](#how-the-web-application-works)
- [Application Workflow](#application-workflow)
- [Project Structure](#project-structure)
- [How to Run Locally](#how-to-run-locally)
- [Deployment](#deployment)
- [Technical Interview Talking Points](#technical-interview-talking-points)

---

## Project Overview

This project converts the exploratory machine learning experiments in `Project.ipynb` into an interactive, end-to-end web application. This project demonstrates how a CNN trained on the MNIST dataset can be integrated into an interactive web application and deployed online.

---

## Features
- **Interactive Drawing Canvas**: Allows users to draw digits using the mouse or touch input.-
- **Digit Prediction**: Processes the drawn digit and predicts the corresponding digit using the trained CNN model.
- **Confidence Score Display**: Shows prediction confidence percentage alongside predicted digit.
- **One-Click Clear**: Easily clear canvas to draw another digit.
- **Beginner-Friendly Architecture**: Lightweight, dependency-minimal setup without bloated JS frameworks or databases.

---

## Technologies Used

- **Frontend / UI**: Streamlit
- **Drawing Canvas**: Streamlit Drawable Canvas
- **Machine Learning**: TensorFlow / Keras
- **Data Processing**: NumPy, Pillow (PIL)
- **Dataset**: MNIST
- **Deployment**: Streamlit Community Cloud

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

## How the Web Application Works

1. The user draws a handwritten digit on the interactive canvas.
2. When the user clicks **Predict**, the canvas image is captured.
3. The image is converted to grayscale.
4. The handwritten digit is detected and cropped.
5. Padding is added around the digit.
6. The image is resized to `28x28` pixels.
7. Pixel values are normalized to the range `0–1`.
8. The processed image is passed to the trained CNN model.
9. The model predicts one of the ten digits (`0–9`).
10. The predicted digit and confidence score are displayed.

---


## Application Workflow

```text
[ User Draws Digit ]
         │
         ▼
[ Click "Predict" ]
         │
         ▼
[ Capture Canvas Image ]
         │
         ▼
[ Grayscale Conversion ]
         │
         ▼
[ Crop + Padding ]
         │
         ▼
[ Resize to 28x28 ]
         │
         ▼
[ Normalize Pixel Values ]
         │
         ▼
[ CNN Model Inference ]
         │
         ▼
[ Prediction + Confidence ]
```

---

## Project Structure

```text
MNIST/
│
├── streamlit_app.py       # Main Streamlit application
├── train_model.py         # CNN training script
├── Project.ipynb          # Original ML exploration notebook
├── model.keras            # Trained CNN model
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
            
```

## How to Run Locally

### Prerequisites
- Python 3.13 installed.

### Step-by-Step Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gaiusparasa10-hash/MNIST.git
   cd MNIST

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

5. **Run the Streamlit Application**:
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Open in Browser**:
    Navigate to `http://localhost:8501` in your web browser.

---

## Deployment
   
   This application is deployed using **Streamlit Community Cloud**.
   
   ### Live Demo
   
🚀 **[Open Live Demo](https://2pm9xwx3qcruqqxmqh6mtv.streamlit.app/)**   
   The application is connected to the GitHub repository and automatically updates when changes are pushed to the `main` branch.
   
   ### Deployment Configuration
   
   - **Platform**: Streamlit Community Cloud
   - **Python Version**: Python 3.13
   - **Main File**: `streamlit_app.py`
   - **Dependencies**: `requirements.txt`
   
   The deployed application allows users to draw a handwritten digit on an interactive canvas and receive a prediction from the         trained CNN model.

---

## Technical Interview Talking Points

- **Why CNN over classical ML (Logistic Regression/KNN)?**
  - Spatial invariance: CNNs preserve 2D grid structure of image pixels through convolutional filters, making them significantly         better at handling shifted or varied handwriting styles compared to flat vector models like Logistic Regression or KNN.
- **How is image preprocessing handled?**
  - The drawing canvas captures the handwritten digit as an image. The application converts it to grayscale, finds the digit             boundaries, crops the digit, adds padding, resizes it to 28x28 pixels, and normalizes pixel values to the range 0–1 before           passing it to the CNN model.
- **Why resize the image to 28x28?**
  - MNIST images are 28x28 grayscale images, so the user's drawing is resized to the same dimensions expected by the trained CNN         model.
