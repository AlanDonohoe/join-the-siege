from werkzeug.datastructures import FileStorage

from .heron_data.v2.classifier import Classifier as HeronDataClassifierV2


class Classifier:
    """
    Public Interface for File Classifiers
    """

    @staticmethod
    def classify(file: FileStorage) -> str:
        return HeronDataClassifierV2().classify(file)
