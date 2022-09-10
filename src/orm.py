from sqlalchemy import Table, MetaData, Column, INTEGER, BINARY, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
from src import model

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', INTEGER, primary_key=True, autoincrement=True),
    Column('login', String(128), nullable=False, unique=True),
    Column('password', String(128), nullable=False),
    Column('first_name', String(128), nullable=False),
    Column('second_name', String(128), nullable=False),
    Column('middle_name', String(128), nullable=True)
)

templates = Table(
    'templates',
    metadata,
    Column('id', INTEGER, primary_key=True, autoincrement=True),
    Column('content', BINARY, nullable=False),
    Column('user_id', INTEGER, ForeignKey('users.id'))
)

template_fields = Table(
    'template_fields',
    metadata,
    Column('id', INTEGER, primary_key=True, autoincrement=True),
    Column('field_name', String(64), nullable=False),
    Column('template_id', INTEGER, ForeignKey('templates.id'))
)

documents = Table(
    'documents',
    metadata,
    Column('id', INTEGER, primary_key=True, autoincrement=True),
    Column('content', BINARY, nullable=False),
    Column('template_id', INTEGER, ForeignKey('templates.id')),
    Column('user_id', INTEGER, ForeignKey('users.id'))
)


def start_mapper():
    documents_mapper = mapper(model.Docx, documents)
    templates_mapper = mapper(model.Template, templates)
    users_mapper = mapper(
        model.User,
        users,
        properties={
            '_templates': relationship(
                model.Template, collection_class=list,
            ),
            '_documents': relationship(
                model.Docx, collection_class=list,
            )
        }
    )
