from src.adapters import repository
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from src import config
import abc


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        url=config.get_sqlite_uri()
    )
)


class UserUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.repo: repository.UserRepository = repository.UserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *argc):
        super().__exit__(*argc)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
