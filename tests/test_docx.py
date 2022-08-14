import pytest
import io
from tests.conftest import test_file
from src.model import Docx, Author


def test_create_docx(test_file):
    with open(test_file, 'rb') as file:
        doc = Docx("test.file", file.read(), Author(name='Zaurbek'))

    first_paragraph = doc.document.paragraphs[0]

    assert first_paragraph.text.lower() == "файл для тестирования", first_paragraph.text



