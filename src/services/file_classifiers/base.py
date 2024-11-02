from abc import ABC, abstractmethod
from werkzeug.datastructures import FileStorage


class Base(ABC):
    @staticmethod
    @abstractmethod
    def classify(file: FileStorage) -> str:
        raise NotImplementedError
