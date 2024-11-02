from io import BytesIO

import pytest
from src.web.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_no_file_in_request(client):
    response = client.post("/classify_file")
    assert response.status_code == 400


def test_no_selected_file(client):
    data = {"file": (BytesIO(b""), "")}  # Empty filename
    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400


def test_success_bank_statement(client):
    data = {"file": (BytesIO(b"dummy content"), "alans bank_statement.pdf")}

    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.get_json() == {"file_class": "bank_statement"}


def test_success_drivers_license(client):
    data = {"file": (BytesIO(b"dummy content"), "alans drivers_license.pdf")}

    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.get_json() == {"file_class": "drivers_license"}


def test_success_invoice(client):
    data = {"file": (BytesIO(b"dummy content"), "alans invoice.pdf")}

    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.get_json() == {"file_class": "invoice"}
