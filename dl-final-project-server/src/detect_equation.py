from fractions import Fraction
from turtle import shape
from flask import Flask
from tensorflow import keras
from PIL import Image
import numpy as np
import os
import joblib
import cv2
from skimage.feature import hog
import json
from skimage.transform import resize


app = Flask(__name__)
SEGMENTED_OUTPUT_DIR = './segmented/'
MATH_MODEL_PATH = "\..\..\dl_models\saved_model\math_model\math_model.h5"

FRACTION_MODEL_PATH = "\..\..\dl_models\model_check_number\kmeans_model.pkl"
FRACTION_MODEL_LABELS = ['fraction', 'no_fraction', 'no_fraction', 'no_fraction']
labels = ['/', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '*', '<', '>']
model = ''

SHAPE_MODEL_PATH = "\..\..\dl_models\shape_fraction_model\shape_fraction_model.h5"
file_path = os.path.abspath("C:/Users/mikim/OneDrive/Desktop/projects/MathWise/dl_models/shape_fraction_model/labels_dict.json")
SHAPE_MODEL_LABELS_FILE = open(file_path)
SHAPE_MODEL_LABELS = json.load(SHAPE_MODEL_LABELS_FILE)


def load_math_model(root_path):
    path = root_path + MATH_MODEL_PATH
    return keras.models.load_model(path)

def load_shape_model(root_path):
    path = root_path + SHAPE_MODEL_PATH
    return keras.models.load_model(path)

def hog_image(image):
    fd, hog_image = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, channel_axis=-1)
    return hog_image


def resize_image(image):
    bgr_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image_resize = cv2.resize(bgr_image, (64, 128))
    return image_resize

def preprocess_shape_image(img):
    # Convert the image to grayscale
    img_gray = img.convert('L')

    # Convert the grayscale image to a numpy array
    img_array = np.array(img_gray)

    # Applying Gaussian blur to remove noise
    blur = cv2.GaussianBlur(img_array, (11, 11), 0)

    # Setting threshold of gray image
    _, threshold = cv2.threshold(blur, 250, 255, cv2.THRESH_BINARY_INV)

    # Using findContours() function with RETR_EXTERNAL and CHAIN_APPROX_SIMPLE flags
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask to store the foreground (shape) pixels
    mask = np.zeros_like(img_array)

    # Iterate through the contours and draw the shapes on the mask
    for contour in contours:
        # Approximate the contour to get the shape type
        perimeter = cv2.arcLength(contour, True)
        epsilon = 0.01 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Get the number of sides of the shape
        sides = len(approx)

        if sides == 3:
            # Fill the triangle contour on the mask
            cv2.drawContours(mask, [contour], 0, 255, -1)
        elif sides >= 4:
            # Fill the rectangle contour on the mask
            cv2.drawContours(mask, [contour], 0, 255, -1)
        else:
            # Fill the circle contour on the mask
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(mask, center, radius, 255, -1)

    # Apply the mask to the original image to extract the foreground (shape) pixels
    result = cv2.bitwise_and(img_array, img_array, mask=mask)

    # Add an additional dimension to the image array
    result = np.expand_dims(result, axis=-1)

    return result

def _predict_shape(image, model):
  image = preprocess_shape_image(image)
  image = np.array(image)
  resized_image = resize(image, (224, 224, 1))
  expanded_image = resized_image[np.newaxis, ...] * 255.0
  my_prediction = model.predict(expanded_image)
  prediction = 0
  label = 0
  for i in range(my_prediction.shape[1]):
    if my_prediction[0][i] > prediction:
      prediction = my_prediction[0][i]
      label = i
  return (label)

def detect_shape(segmented_images, paths):
    try:
        shape_model = load_shape_model(app.root_path)
        fraction_model = load_math_model(app.root_path)
        equation = ''

        # Predict shape part
        shape_image = segmented_images[0]
        shape_prediction = _predict_shape(shape_image, shape_model)
        shape_prediction = [value for value in SHAPE_MODEL_LABELS if SHAPE_MODEL_LABELS[value] == shape_prediction][0]

        # Predict fraction part
        fraction_image = segmented_images[1]

        numerator_img = fraction_image.crop((0, 0, fraction_image.width, fraction_image.height/2))
        denomenator_img = fraction_image.crop((0, fraction_image.height/2, fraction_image.width, fraction_image.height))
        numerator_img = numerator_img.resize((28, 28))
        denomenator_img = denomenator_img.resize((28, 28))
        numerator_img = np.asarray(numerator_img)
        denomenator_img = np.asarray(denomenator_img)
        numerator_img = np.reshape(numerator_img, (1, 28, 28, 1))
        denomenator_img = np.reshape(denomenator_img, (1, 28, 28, 1))
        fraction_prediction = labels[np.argmax(fraction_model.predict(numerator_img))]
        fraction_prediction += "/"
        fraction_prediction += labels[np.argmax(fraction_model.predict(denomenator_img))]

        # Build equation
        equation = str(fraction_prediction) + "=" + str(shape_prediction)
        return equation
    except Exception as e:
        print(e)
        return "error parsing question"


def detect_equation(segmented_images):
    model = load_math_model(app.root_path)
    equation = ''

    knn_model = joblib.load(open(app.root_path + FRACTION_MODEL_PATH, 'rb'))

    for i in segmented_images:
        fraction_image = resize_image(i)
        fraction_image = hog_image(fraction_image)
        features = np.array(fraction_image).shape[0] * np.array(fraction_image).shape[1]
        flattened = np.array(fraction_image).reshape(1, features)
        predict = knn_model.predict(flattened)
        print("predict: " + str(FRACTION_MODEL_LABELS[predict[0]]))
        if FRACTION_MODEL_LABELS[predict[0]] != "fraction":
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

def detect(segmented_equation_path, is_shape):
    segmented_images = []
    paths = []
    files = [f for r, d, f in os.walk(segmented_equation_path)][0]
    for f in files:
        im = Image.open(os.path.join(segmented_equation_path, f))
        segmented_images.append(im)
        paths.append(f)

    if is_shape:
        return detect_shape(segmented_images, paths)
    else:
        return detect_equation(segmented_images)
