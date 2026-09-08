"""
MNIST CNN Model Training Script
Extracted from Project.ipynb (Cell 2)

This script trains the Convolutional Neural Network (CNN) on the MNIST dataset
and saves the trained model to 'model.keras' for use in the Flask web application.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def train_and_save():
    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Preprocessing: Reshape to (28, 28, 1) and normalize pixel values [0, 255] -> [0.0, 1.0]
    x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    x_test  = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

    # One-hot encode targets
    y_train_cat = to_categorical(y_train, 10)
    y_test_cat  = to_categorical(y_test, 10)

    # Build CNN Architecture (matches Project.ipynb Cell 2)
    print("Building CNN Model...")
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])

    # Compile Model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train Model (5 epochs)
    print("Training CNN model for 5 epochs...")
    model.fit(x_train, y_train_cat, epochs=5, batch_size=128, verbose=1, validation_split=0.1)

    # Evaluate Model
    loss, accuracy = model.evaluate(x_test, y_test_cat, verbose=0)
    print(f"Model Test Accuracy: {accuracy * 100:.2f}%")

    # Save Model to disk
    print("Saving model to model.keras...")
    model.save("model.keras")
    print("Model saved successfully as 'model.keras'!")

if __name__ == "__main__":
    train_and_save()
