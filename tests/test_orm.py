from src import model
from sqlalchemy import text


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
        model.User(login='login1', password='pass1', first_name='first1', second_name='second1', middle_name='middle1')
    ]

    actual = session.query(model.User).all()
    assert actual == expected, actual


def test_create_user(session):
    session.add(
        model.User(login='login1', password='pass1', first_name='first1', second_name='second1', middle_name='middle1')
    )

    session.add(
        model.User(login='login2', password='pass2', first_name='first2', second_name='second2', middle_name='middle2')
    )

    expected = [
        model.User(login='login1', password='pass1', first_name='first1', second_name='second1', middle_name='middle1'),
        model.User(login='login2', password='pass2', first_name='first2', second_name='second2', middle_name='middle2')
    ]

    actual = session.query(model.User).all()

    assert actual == expected, actual


def create_user(session):
    user = model.User(login='login1', password='pass1', first_name='first1', second_name='second1',
                      middle_name='middle1')
    session.add(user)

    return session.get(model.User, 1)


def test_create_template(session, test_template_file):
    user = create_user(session)

    template = model.Template('template1', test_template_file, user)
    assert len(template.fields) != 0, template.fields

    session.add(template)
    session.commit()

    actual = session.get(model.User, 1)._templates
    expected = [
        template,

    ]
    assert actual == expected, actual






