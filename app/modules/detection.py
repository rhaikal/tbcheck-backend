import os
import numpy as np
from fastapi import UploadFile
from keras.models import load_model
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img

from config import settings

PREDICTION_THRESHOLD = 0.5


def save_upload_file(file: UploadFile) -> str:
    filepath = f"{settings.detection_upload_path}/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    return filepath


def preprocess_image(filepath: str) -> np.ndarray:
    img = load_img(filepath, target_size=(299, 299))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)


def cleanup_file(filepath: str) -> None:
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass


def load_prediction_model() -> object:
    return load_model(
        f"{settings.detection_model_dir}/{settings.detection_model_filename}"
    )


def predict_image(img_array: np.ndarray, model: object) -> np.ndarray:
    return model.predict(img_array)


def get_prediction_result(prediction: np.ndarray) -> dict:
    prediction_value = float(prediction[0][0])
    predicted_class = (
        "negative" if prediction_value <= PREDICTION_THRESHOLD else "positive"
    )
    return {
        "predicted_class": predicted_class,
        "predicted_score": {
            "positive": prediction_value,
            "negative": 1.0 - prediction_value,
        },
    }
