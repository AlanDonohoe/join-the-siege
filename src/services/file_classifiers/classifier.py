from werkzeug.datastructures import FileStorage

from .heron_data.classifier import Classifier as HeronDataClassifier


class Classifier:
    @staticmethod
    def classify(file: FileStorage) -> str:
        return HeronDataClassifier().classify(file)
