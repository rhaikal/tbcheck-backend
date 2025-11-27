import os
import gdown

from config import settings


def setup_model() -> None:
    os.makedirs(settings.detection_raw_path, exist_ok=True)
    os.makedirs(settings.detection_processed_path, exist_ok=True)
    os.makedirs(settings.detection_model_dir, exist_ok=True)

    model_path = os.path.join(
        settings.detection_model_dir, settings.detection_model_filename
    )
    if not os.path.exists(model_path):
        fetch_model(model_path)


def fetch_model(model_path) -> None:
    gdown.download(
        settings.detection_model_gdrive_url,
        model_path,
        quiet=False,
        fuzzy=True,
    )
