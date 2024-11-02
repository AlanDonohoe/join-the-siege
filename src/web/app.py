from flask import Flask, request, Response, jsonify

from src.services.file_classifiers.classifier import Classifier
from src.web.validators.file_name import FileNameValidator

app = Flask(__name__)

@app.route("/classify_file", methods=["POST"])
def classify_file_route() -> Response:
    file_name_validation = FileNameValidator.call(request.files)

    if not file_name_validation.valid:
        return jsonify({"error": file_name_validation.error_message}), 400

    file_class = Classifier.classify(request.files["file"])

    return jsonify({"file_class": file_class}), 200


if __name__ == "__main__":
    app.run(debug=True)
