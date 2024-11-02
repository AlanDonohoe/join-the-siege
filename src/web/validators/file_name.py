from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class FileNameValidation:
    valid: bool
    error_message: Optional[str] = None


class FileNameValidator:
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg"}

    @classmethod
    def call(cls, files: Dict) -> FileNameValidation:
        file = files.get("file")

        if not file:
            return FileNameValidation(
                valid=False, error_message="No file part in the request"
            )

        if not file.filename:
            return FileNameValidation(valid=False, error_message="No selected file")

        if not cls._allowed_file(file.filename):
            return FileNameValidation(
                valid=False, error_message="File type not allowed"
            )

        return FileNameValidation(valid=True)

    @classmethod
    def _allowed_file(cls, filename: str) -> bool:
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in cls.ALLOWED_EXTENSIONS
        )
