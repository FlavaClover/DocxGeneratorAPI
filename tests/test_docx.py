import pytest
import io
from tests.conftest import test_file
from src.model import Docx, User


def test_create_docx(test_file):
    with open(test_file, 'rb') as file:
        doc = Docx("test.file", file.read(), User(login='login1', password='pass1',
                                                  first_name='Zaurbek', second_name='Tedeev', middle_name=None))

    first_paragraph = doc.document.paragraphs[0]

    assert first_paragraph.text.lower() == "файл для тестирования", first_paragraph.text



