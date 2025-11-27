from uuid import uuid4
from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Response, Request

from sqlalchemy.ext.asyncio import AsyncSession

from config import settings

from app.core.database import get_session
from app.core.files import save_file, move_temp_file

from app.dependencies.auth import require_auth
from app.models import User

from app.modules.detection import (
    load_prediction_model,
    predict_image,
    preprocess_image,
)
from app.modules.detection_explainer import (
    generate_explanation_heatmap,
    generate_overlay,
)
from app.modules.exam import save_exam
from app.modules.exam_note import save_exam_notes

from app.schemas.exam import ExamSave

router = APIRouter()


@router.post("/image/predict")
async def predict(
    file: UploadFile, user: Annotated[User, Depends(require_auth)], request: Request
) -> Response:
    inference_id = str(uuid4())

    file_extension = file.filename.split(".")[-1]

    uploaded_filepath = save_file(
        source=file, extension=file_extension, prefix="raw_", suffix=f"_{inference_id}"
    )

    img_array = preprocess_image(uploaded_filepath)

    # prediction
    model = load_prediction_model()
    prediction_score = predict_image(img_array, model)

    # explain prediction
    heatmap = generate_explanation_heatmap(
        model, img_array, layer_name="custom_block1_conv"
    )
    overlay_bytes = generate_overlay(uploaded_filepath, heatmap)
    processed_filepath = save_file(
        source=overlay_bytes,
        extension=file_extension,
        prefix="processed_",
        suffix=f"_{inference_id}",
    )

    request.app.state.inference_store[inference_id] = {
        "raw_image": uploaded_filepath,
        "processed_image": processed_filepath,
        "prediction_score": prediction_score,
    }

    return Response(
        content=overlay_bytes,
        headers={
            "X-Predicted-Score": str(prediction_score),
            "X-Inference-ID": inference_id,
        },
        media_type="image/png",
    )


@router.post("/image/save")
async def save_prediction(
    exam_data: ExamSave,
    user: Annotated[User, Depends(require_auth)],
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    inference_id = exam_data.inference_id
    inference_store = request.app.state.inference_store.get(inference_id)
    if not inference_store:
        return {"error": "Session data not found"}

    inference_store = {
        **inference_store,
        "raw_image": move_temp_file(
            inference_store["raw_image"], settings.detection_raw_path, inference_id
        ),
        "processed_image": move_temp_file(
            inference_store["processed_image"],
            settings.detection_processed_path,
            inference_id,
        ),
    }

    exam = await save_exam(exam_data, user, inference_store, session)
    if exam_data.notes and len(exam_data.notes) > 0:
        await save_exam_notes(exam, exam_data.notes, session)

    del request.app.state.inference_store[inference_id]

    return {"message": "Exam saved successfully", "exam_id": exam.id}
