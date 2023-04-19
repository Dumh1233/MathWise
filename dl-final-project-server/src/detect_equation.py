from tensorflow import keras
from PIL import Image
import numpy as np
import os

SEGMENTED_OUTPUT_DIR = './segmented/'
labels = ['/', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '*']
model = ''

def load_model():
    global model
    model =  keras.models.load_model("../../dl_models/saved_model/math_model")

def detect():
    equation = ''
    segmented_images = []
    files = [f for r, d, f in os.walk(SEGMENTED_OUTPUT_DIR)][0]
    for f in files:
        img = Image.open(SEGMENTED_OUTPUT_DIR + f)
        img = img.resize((28,28))
        im = np.asarray(img)
        im = np.reshape(im, (28, 28, 1))
        segmented_images.append(im)
    segmented_images = np.array(segmented_images)
    y_pred = model.predict(segmented_images)
    for i in range(len(y_pred)):
        equation += labels[np.argmax(y_pred[i])]
    return equation