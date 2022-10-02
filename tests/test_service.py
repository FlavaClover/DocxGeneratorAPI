from src.service_layer import service
from src.domain.schema import User
from src.service_layer import unit_of_work
from src.adapters.repository import AbstractRepository
from src.service_layer.unit_of_work import AbstractUnitOfWork


class FakeRepository(AbstractRepository):
    def __init__(self):
        self.objs = list()

    def get_by_id(self, id_obj):
        for i in self.objs:
            if i.id == id_obj:
                return i

    def get_by_login(self, login: str):
        for i in self.objs:
            if i.login == login:
                return i

    def all(self):
        return self.objs

    def add(self, obj):
        self.objs.append(obj)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.repo = FakeRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_create_user():
    uow = FakeUnitOfWork()
    service.create_user(uow, User(login='login', password='password',
                                  first_name='name', second_name='name_s', middle_name='name_m'))
    assert uow.repo.get_by_login('login') is not None
    assert uow.committed
