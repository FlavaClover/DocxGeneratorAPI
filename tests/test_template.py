import pytest
import io
from src.model import Template, User
from src.exceptions import TemplateDoesNotContainsFields
from tests.conftest import test_template_file, test_template_file_fail


def test_create_template_with_fields(test_template_file):
    template = Template('template1', test_template_file, User(login='login1', password='pass1', first_name='Zaurbek',
                                                              second_name='Tedeev', middle_name=None))

    first_paragraph = template.document.paragraphs[0]

    assert template._is_have_template_fields(), template._is_have_template_fields()
    assert len(template._get_cells_paragraphs()) != 0, template._get_cells_paragraphs()
    assert len(template.paragraphs) != 0, template.paragraphs
    assert first_paragraph.text.lower() == 'шаблон для тестирования', first_paragraph.text


def test_create_template_fail(test_template_file_fail):
    with pytest.raises(TemplateDoesNotContainsFields, match='Template must be contains any fields'):
        _ = Template('template_fail', test_template_file_fail, User(login='login1', password='pass1',
                                                                    first_name='Zaurbek', second_name='Tedeev',
                                                                    middle_name=None))


def test_template_is_contains_existing_fields(test_template_file):
    template = Template(test_template_file, test_template_file, User(login='login1', password='pass1',
                                                                     first_name='Zaurbek', second_name='Tedeev',
                                                                     middle_name=None))

    assert '___field___' in template.fields, template.fields
    assert '___filedDD___' not in template.fields, template.fields
    assert '___hello field___' in template.fields, template.fields
