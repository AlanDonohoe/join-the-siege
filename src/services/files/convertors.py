from typing import List
from werkzeug.datastructures import FileStorage
import io

from PIL import Image
# from spire.doc import *
# from spire.doc.common import *
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

# def word_doc_to_images(file: FileStorage) -> List:
#     images = []
#     # file_pdf = pymupdf.Document(stream=file.read())

#     # for page in file_pdf:
#     #     pix = page.get_pixmap()
#     #     img_data = pix.tobytes("jpg")
#     #     img = Image.open(io.BytesIO(img_data))
#     #     images.append(img)

#     document = Document()
#     # Load a Word DOCX file
#     document.LoadFromFile("Sample.docx")
#     # Or load a Word DOC file
#     #document.LoadFromFile("Sample.doc")

#     # Convert the document to a list of image streams
#     image_streams = document.SaveImageToStreams(ImageType.Bitmap)

#     # Incremental counter
#     i = 1

#     # Save each image stream to a PNG file
#     for image in image_streams:
#         image_name = str(i) + ".png"
#         with open(image_name,'wb') as image_file:
#             image_file.write(image.ToArray())
#         i += 1

#     # Close the document
#     document.Close()

#     return images
