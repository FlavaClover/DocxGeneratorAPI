from src.domain import schema, exceptions
from sqlalchemy import text
import pytest


def test_create_user_raw_sql(session):
    stm = text('INSERT INTO users (login, password, first_name, second_name, middle_name) '
               'values (:login, :password, :first_name, :second_name, :middle_name)').bindparams(
        **{
            'login': 'login1', 'password': 'pass1', 'first_name': 'first1', 'second_name': 'second1',
            'middle_name': 'middle1'
        }
    )

    session.execute(stm)

    expected = [
        schema.User(login='login1', password='pass1', first_name='first1', second_name='second1', middle_name='middle1')
    ]

    actual = session.query(schema.User).all()
    assert actual == expected, actual


def test_create_user(session):
    session.add(
        schema.User(login='login1', password='pass1', first_name='first1',
                    second_name='second1', middle_name='middle1')
    )

    session.add(
        schema.User(login='login2', password='pass2', first_name='first2',
                    second_name='second2', middle_name='middle2')
    )

    expected = [
        schema.User(login='login1', password='pass1', first_name='first1',
                    second_name='second1', middle_name='middle1'),
        schema.User(login='login2', password='pass2', first_name='first2',
                    second_name='second2', middle_name='middle2')
    ]

    actual = session.query(schema.User).all()

    assert actual == expected, actual


def create_user(session):
    user = schema.User(login='login1', password='pass1', first_name='first1', second_name='second1',
                       middle_name='middle1')
    session.add(user)

    return session.get(schema.User, 1)


def test_create_template_fields(session, test_template_file):
    user: schema.User = create_user(session)
    template = schema.Template('template1', test_template_file)
    user.add_template(template)
    template.add_field('___field___')

    with pytest.raises(exceptions.TemplateDoesNotContainsSpecificField, match='Template does not contains this field'):
        template.add_field('___unexpected_field___')
    session.add(template)
    session.commit()

    actual = session.get(schema.User, 1)._templates[0].template_fields
    expected = template.template_fields

    assert actual == expected, actual

    template.add_field('___field1___')
    session.add(template)
    session.commit()

    actual = session.get(schema.User, 1)._templates[0].template_fields
    expected = template.template_fields

    assert actual == expected, actual

    actual = session.get(schema.User, 1)._templates
    expected = 1

    assert len(actual) == expected, actual


def test_add_template_to_user(session, test_template_file):
    user: schema.User = create_user(session)

    template1 = schema.Template('template1', test_template_file, user)
    user.add_template(template1)

    session.add(user)
    session.commit()

    actual = len(session.query(schema.User).all())
    expected = 1

    assert actual == expected, actual

    actual = len(session.get(schema.User, 1)._templates)
    expected = 1
    assert actual == expected, actual

    template2 = schema.Template('template2', test_template_file, user)
    user.add_template(template2)

    session.add(user)
    session.commit()

    actual = len(session.get(schema.User, 1)._templates)
    expected = 2

    assert actual == expected, actual

    actual = len(session.query(schema.TemplateField).all())
    expected = 12

    assert actual == expected, actual


def test_remove_template_from_user(session, test_template_file):
    user: schema.User = create_user(session)

    template1 = schema.Template('template1', test_template_file)
    template2 = schema.Template('template2', test_template_file)
    template3 = schema.Template('template3', test_template_file)

    user.add_template(template1, template2, template3)
    session.add(user)
    session.commit()

    actual = len(session.query(schema.Template).all())
    expected = 3

    assert actual == expected, actual

    user: schema.User = session.get(schema.User, 1)

    actual = user._templates
    expected = [template1, template2, template3]

    assert actual == expected, actual

    actual = len(session.query(schema.TemplateField).all())
    expected = 18

    assert actual == expected

    actual = user._templates
    non_expected = [template1]

    assert actual != non_expected, actual

    user.remove_template(template1)

    session.add(user)
    session.commit()

    user: schema.User = session.get(schema.User, 1)

    actual = user._templates
    expected = [template2, template3]

    assert actual == expected

