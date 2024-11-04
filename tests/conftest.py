import os

import pytest


@pytest.fixture
def test_base_path():
    yield os.path.dirname(os.path.realpath(__file__))
