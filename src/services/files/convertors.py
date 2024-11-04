from typing import List
from werkzeug.datastructures import FileStorage
import io

from PIL import Image
import pymupdf


def pdf_to_images(file: FileStorage) -> List:
    images = []
    file_pdf = pymupdf.Document(stream=file.read())

    for page in file_pdf:
        pix = page.get_pixmap()
        img_data = pix.tobytes("jpg")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)

    return images
