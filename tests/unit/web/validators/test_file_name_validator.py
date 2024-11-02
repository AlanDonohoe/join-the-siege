from io import BytesIO

import pytest

from src.web.validators.file_name import FileNameValidator


class TestFileNameValidator:
    @pytest.mark.skip("Need to implemnet ImmutableMultiDict with <FileStorage object>")
    @pytest.mark.parametrize(
    "file, expected_valid, expected_error_message",
    [
        ({"file": (BytesIO(b"dummy content"), "file.pdf")}, True, None),
        ({"file": (BytesIO(b"dummy content"), "file.png")}, True, None),
        ({"file": (BytesIO(b"dummy content"), "file.jpg")}, True, None),
        ({"file": (BytesIO(b"dummy content"), "file.txt")}, False, "File type not allowed"),
    ]
    )
    def test_call(self, file, expected_valid, expected_error_message) -> None:
        file_name_validation = FileNameValidator.call(file)

        assert file_name_validation.valid == expected_valid
        assert file_name_validation.error_message == expected_error_message
