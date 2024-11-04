from werkzeug.datastructures import FileStorage

from src.services.files.classifiers.base import Base

class Classifier(Base):
    """
    V1 Classifier: A Classifier based solely on file name
    """

    @staticmethod
    def classify(file: FileStorage) -> str:
        filename = file.filename.lower()
        # file_bytes = file.read()

        if "drivers_license" in filename:
            return "drivers_license"

        if "bank_statement" in filename:
            return "bank_statement"

        if "invoice" in filename:
            return "invoice"

        return "unknown file"
