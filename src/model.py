import io
from typing import List
from docx import Document
from docx.document import Document as DocumentObject
from src.exceptions import TemplateDoesNotContainsFields
from dataclasses import dataclass
import re
import datetime


@dataclass
class Field:
    name: str
    value: str


@dataclass
class Author:
    name: str


class Docx:
    def __init__(self, name: str, content: bytes, author: Author,
                 created_datetime: datetime.datetime = datetime.datetime.now()):
        self._content_bytes = content
        self.document: DocumentObject = Document(io.BytesIO(content))
        self._name = name
        self._created_datetime = created_datetime
        self._author = author

    @property
    def created_datetime(self):
        return self._created_datetime

    @property
    def name(self):
        return self._name + '.docx'


class Template(Docx):
    def __init__(self, name: str, content: bytes, author: Author,
                 created_datetime: datetime.datetime = datetime.datetime.now()):
        super().__init__(name, content, author, created_datetime=created_datetime)

        if not self._is_have_template_fields():
            raise TemplateDoesNotContainsFields()

    def _is_have_template_fields(self):
        is_have = False

        paragraphs = [p.text for p in self._get_all_paragraphs() + self._get_all_cells_paragraphs() if p.text != '']

        for paragraph in paragraphs:
            if len(re.findall(r'___\S+___', paragraph)) > 0:
                is_have = True
                break

        return is_have

    def _get_all_cells_paragraphs(self):
        paragraphs = []

        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    paragraphs += cell.paragraphs

        return paragraphs

    def _get_all_paragraphs(self):
        paragraphs = []

        for paragraph in self.document.paragraphs:
            paragraphs.append(paragraph)

        return paragraphs

    @property
    def fields(self):
        pass

    @property
    def paragraphs(self):
        return self._get_all_paragraphs() + self._get_all_cells_paragraphs()

