import abc
from src.domain import schema
from sqlalchemy.orm import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, obj):
        pass

    @abc.abstractmethod
    def get_by_id(self, id_obj):
        pass

    @abc.abstractmethod
    def all(self):
        pass


class UserRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj):
        self.session.add(obj)

    def get_by_id(self, id_obj):
        return self.session.get(schema.User, id_obj)

    def all(self):
        return self.session.query(schema.User).all()
