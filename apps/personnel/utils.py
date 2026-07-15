from pathlib import Path


def person_photo_upload_path(instance, filename: str) -> str:
    """
    Формує шлях для фотографії військовослужбовця.
    """
    extension = Path(filename).suffix.lower()

    return f"persons/{instance.service_number}/photo{extension}"
