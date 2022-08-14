import pytest
import random
import os


@pytest.fixture
def test_file():
    yield 'tests/files/test_file.docx'


@pytest.fixture
def test_template_file():
    yield 'tests/files/test_template.docx'
