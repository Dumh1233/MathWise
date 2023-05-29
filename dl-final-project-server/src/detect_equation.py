from flask import Flask
from tensorflow.keras import models
from PIL import Image
import numpy as np
import os
import joblib
import cv2
from skimage.feature import hog


app = Flask(__name__)
SEGMENTED_OUTPUT_DIR = './segmented/'
MATH_MODEL_PATH = "\..\..\dl_models\saved_model\math_model\math_model.h5"
FRACTION_MODEL_PATH = "\..\..\dl_models\model_check_number\kmeans_model.pkl"
FRACTION_MODEL_LABELS = ['no_fraction', 'no_fraction', 'fraction']
labels = ['/', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '*', '<', '>']
model = ''


def load_model(root_path):
    path = root_path + MATH_MODEL_PATH
    return models.load_model(path)


def hog_image(image):
    fd, hog_image = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, channel_axis=-1)
    return hog_image


def resize_image(image):
    bgr_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image_resize = cv2.resize(bgr_image, (64, 128))
    return image_resize


def detect(segmented_equation_path):
    print(segmented_equation_path)
    model = load_model(app.root_path)
    equation = ''
    segmented_images = []
    files = [f for r, d, f in os.walk(segmented_equation_path)][0]
    for f in files:
        im = Image.open(os.path.join(segmented_equation_path, f))
        segmented_images.append(im)

    knn_model = joblib.load(open(app.root_path+FRACTION_MODEL_PATH, 'rb'))

    for i in segmented_images:
        fraction_image = resize_image(i)
        fraction_image = hog_image(fraction_image)
        features = np.array(fraction_image).shape[0] * np.array(fraction_image).shape[1]
        flattened = np.array(fraction_image).reshape(1, features)
        predict = knn_model.predict(flattened)
        print("predict: " + str(FRACTION_MODEL_LABELS[predict[0]]))
        if FRACTION_MODEL_LABELS[predict[0]] != 2:
            img = i.resize((28, 28))
            im = np.asarray(img)
            im = np.reshape(im, (1, 28, 28, 1))
            equation += labels[np.argmax(model.predict(im))]
        else:
            numerator_img = i.crop((0, 0, i.width, i.height/2))
            denomenator_img = i.crop((0, i.height/2, i.width, i.height))
            numerator_img = numerator_img.resize((28, 28))
            denomenator_img = denomenator_img.resize((28, 28))
            numerator_img = np.asarray(numerator_img)
            denomenator_img = np.asarray(denomenator_img)
            numerator_img = np.reshape(numerator_img, (1, 28, 28, 1))
            denomenator_img = np.reshape(denomenator_img, (1, 28, 28, 1))
            index = len(equation) - 1
            brackets_opened = 0
            while (index >= 0) and (equation[index].isnumeric() or equation[index] == ')' or brackets_opened != 0):
                if equation[index] == ')':
                    brackets_opened += 1
                elif equation[index] == '(':
                    brackets_opened -= 1
                index -= 1

            equation = equation[:index+1] + "(" + equation[index+1:]
            special_fraction_flag = False
            if equation[-1] != '(':
                special_fraction_flag = True
                equation += "+("
            equation += labels[np.argmax(model.predict(numerator_img))]
            equation += "/"
            equation += labels[np.argmax(model.predict(denomenator_img))]
            equation += ")"
            if special_fraction_flag:
                equation += ")"

    return equation
