from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from app.dependencies.auth import require_auth
from app.models import User
from app.modules.detection import (
    cleanup_file,
    get_prediction_result,
    load_prediction_model,
    predict_image,
    preprocess_image,
    save_upload_file,
)

router = APIRouter()


@router.post("/image/predict")
async def predict(
    file: UploadFile,
    user: Annotated[User, Depends(require_auth)],
) -> dict:
    filepath = save_upload_file(file)

    try:
        img_array = preprocess_image(filepath)
        model = load_prediction_model()
        prediction = predict_image(img_array, model)
        return get_prediction_result(prediction)
    finally:
        cleanup_file(filepath)
