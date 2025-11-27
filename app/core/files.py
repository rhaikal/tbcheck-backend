import os
import shutil
import tempfile
from fastapi import UploadFile


def save_file(source: UploadFile | bytes, extension: str, **params) -> str:
    if "suffix" in params:
        params["suffix"] = f"{params['suffix']}.{extension}"
    else:
        params["suffix"] = f".{extension}"

    with tempfile.NamedTemporaryFile(delete=False, **params) as f:
        if isinstance(source, bytes):
            f.write(source)
        else:
            f.write(source.file.read())
        return f.name


def cleanup_file(filepath: str) -> None:
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass


def cleanup_files(filepaths: list[str]) -> None:
    for filepath in filepaths:
        cleanup_file(filepath)


def move_temp_file(temp_path: str, dest_dir: str, new_name: str) -> str:
    if not os.path.exists(temp_path):
        raise FileNotFoundError(f"Temporary file {temp_path} does not exist.")

    if not os.path.splitext(new_name)[1]:
        ext = os.path.splitext(temp_path)[1]
        new_name = f"{new_name}{ext}"

    dest_path = os.path.join(dest_dir, new_name).replace("\\", "/")
    shutil.move(temp_path, dest_path)

    cleanup_file(temp_path)
    return dest_path
