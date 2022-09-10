import pytest
import random
import os
from src.orm import metadata, start_mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session


@pytest.fixture
def test_file():
    yield 'tests/files/test_file.docx'


@pytest.fixture
def test_template_file():
    yield 'tests/files/test_template.docx'


@pytest.fixture
def test_template_file_fail():
    yield 'tests/files/test_template_fail.docx'


@pytest.fixture
def db():
    engine = create_engine('sqlite:///database', echo=True)
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def session(db) -> Session:
    start_mapper()
    session = sessionmaker(bind=db)()
    yield session
    session.close()
    clear_mappers()

