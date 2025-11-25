import io

from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Response

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
from app.modules.detection_explainer import (
    generate_explanation_heatmap,
    generate_overlay,
)

router = APIRouter()


@router.post("/image/predict")
async def predict(
    file: UploadFile,
    user: Annotated[User, Depends(require_auth)],
) -> Response:
    filepath = save_upload_file(file)

    try:
        img_array = preprocess_image(filepath)

        # prediction
        model = load_prediction_model()
        prediction = predict_image(img_array, model)
        result = get_prediction_result(prediction)

        # explain prediction
        heatmap = generate_explanation_heatmap(
            model, img_array, layer_name="custom_block1_conv"
        )
        overlay_bytes = generate_overlay(filepath, heatmap)

        return Response(
            content=overlay_bytes,
            headers={
                "X-Predicted-Class": result["predicted_class"],
                "X-Positive-Score": str(result["predicted_score"]["positive"]),
                "X-Negative-Score": str(result["predicted_score"]["negative"]),
            },
            media_type="image/png",
        )

    finally:
        cleanup_file(filepath)
