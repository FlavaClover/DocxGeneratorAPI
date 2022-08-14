import pytest
import io
from src.model import Template, Author
from tests.conftest import test_template_file


def test_create_template_with_fields(test_template_file):
    with open(test_template_file, 'rb') as file:
        template = Template('template1', file.read(), Author(name='Zaurbek'))

    first_paragraph = template.document.paragraphs[0]
    assert template._is_have_template_fields(), template._is_have_template_fields()
    assert len(template._get_all_cells_paragraphs()) != 0, template._get_all_cells_paragraphs()
    assert len(template.paragraphs) != 0, template.paragraphs
    assert first_paragraph.text.lower() == 'шаблон для тестирования', first_paragraph.text
