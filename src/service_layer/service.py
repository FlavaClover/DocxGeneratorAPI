from src.service_layer import unit_of_work
from src.adapters import repository
from src.domain import schema, exceptions
from copy import deepcopy, copy
import abc


def get_user(uow: unit_of_work.AbstractUnitOfWork, id_user: int):
    with uow:
        user = deepcopy(uow.repo.get_by_id(id_user))
        if user is None:
            raise exceptions.UserDoesNotExists(
                f'User with id {id_user} does not exists'
            )
    return user


def create_user(uow: unit_of_work.AbstractUnitOfWork, user: schema.User, ):
    with uow:
        uow.repo.add(user)
        uow.commit()


def get_all_users(uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        result = deepcopy(uow.repo.all())
    return result





