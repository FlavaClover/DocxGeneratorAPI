from src.domain.schema import Docx


def test_create_docx(test_file):
    with open(test_file, 'rb') as file:
        doc = Docx("test.file", file.read())

    first_paragraph = doc.document.paragraphs[0]

    assert first_paragraph.text.lower() == "файл для тестирования", first_paragraph.text



