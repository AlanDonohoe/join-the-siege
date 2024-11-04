from io import BytesIO
import os

import pytest

from src.web.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def bank_statement_pdf(test_base_path) -> BytesIO:
    with open(f"{test_base_path}/file_fixtures/bank_statements/bank_statement_1.pdf", "rb") as f:
        return BytesIO(f.read())


@pytest.fixture
def drivers_license_jpg(test_base_path) -> BytesIO:
    with open(f"{test_base_path}/file_fixtures/drivers_licenses/drivers_license_1.jpg", "rb") as f:
        return BytesIO(f.read())


@pytest.fixture
def invoice_pdf(test_base_path) -> BytesIO:
    with open(f"{test_base_path}/file_fixtures/invoices/invoice_1.pdf", "rb") as f:
        return BytesIO(f.read())


def test_no_file_in_request(client):
    response = client.post("/classify_file")
    assert response.status_code == 400


def test_no_selected_file(client):
    data = {"file": (BytesIO(b""), "")}  # Empty filename
    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400


def test_success_bank_statement(client, bank_statement_pdf):
    data = {"file": (bank_statement_pdf, "alans bank_statement.pdf")}

    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.get_json() == {"file_class": "bank_statement"}


def test_success_drivers_license(client, drivers_license_jpg):
    data = {"file": (drivers_license_jpg, "alans drivers_license.jpg")}

    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.get_json() == {"file_class": "drivers_license"}


def test_success_invoice(client, invoice_pdf):
    data = {"file": (invoice_pdf, "alans invoice.pdf")}

    response = client.post(
        "/classify_file", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.get_json() == {"file_class": "invoice"}
