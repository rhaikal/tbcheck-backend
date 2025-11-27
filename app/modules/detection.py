import numpy as np
from keras.models import load_model
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img

from config import settings

PREDICTION_THRESHOLD = 0.5


def preprocess_image(filepath: str) -> np.ndarray:
    img = load_img(filepath, target_size=(299, 299))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)


def load_prediction_model() -> object:
    return load_model(
        f"{settings.detection_model_dir}/{settings.detection_model_filename}"
    )


def predict_image(img_array: np.ndarray, model: object) -> np.ndarray:
    prediction = model.predict(img_array)
    return float(prediction[0][0])
