import os
import gdown

from config import settings


def setup_model() -> None:
    model_path = os.path.join(
        settings.detection_model_dir, settings.detection_model_filename
    )
    if not os.path.exists(model_path):
        gdown.download(
            settings.detection_model_gdrive_url,
            model_path,
            quiet=False,
            fuzzy=True,
        )
