from werkzeug.datastructures import FileStorage
import os

from fastai.learner import load_learner
from fastai.vision.core import PILImage
from PIL import Image

from src.services.files.classifiers.base import Base
from src.services.files.convertors import pdf_to_images


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_ROOT, "model.pkl")

model_v2 = load_learner(MODEL_PATH)


class Classifier(Base):
    """
    V2 Classifier: A Classifier using a fine-tuned CNN (resnet-18) model
    """

    IMAGE_DIMENSIONS_MODEL_V2 = (192, 192)

    @classmethod
    def classify(cls, file: FileStorage) -> str:
        if file.content_type == "application/pdf":
            img = pdf_to_images(file)[0]
        else:
            img = PILImage.create(file.stream)

        img.thumbnail(cls.IMAGE_DIMENSIONS_MODEL_V2, Image.Resampling.LANCZOS)

        file_type,_,probability = model_v2.predict(img)

        print(f"This is a: {file_type}. Probabilities: {probability[0]:.8f}")

        return cls._file_type_mapped(file_type)

    @classmethod
    def _file_type_mapped(cls, file_type_raw: str) -> str:
        file_type_mapped_dict = {
            "driving license US": "drivers_license",
            "bank statement US PDF": "bank_statement",
            "invoice US PDF": "invoice"
        }

        return file_type_mapped_dict.get(file_type_raw, "Unknown")
