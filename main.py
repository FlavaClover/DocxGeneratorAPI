from fastapi import FastAPI, Response, HTTPException
from src import config
from src.adapters import orm
from src.domain import schema, exceptions
from src.service_layer import unit_of_work
from typing import List
from src.service_layer import service

orm.start_mapper()
app = FastAPI()


@app.post('/user/create')
async def create_user(user: schema.User):
    user_uow = unit_of_work.UserUnitOfWork()
    service.create_user(user_uow, user)

    return Response(status_code=200)


@app.get('/user/get/{id_user}', response_model=schema.User)
async def get_user(id_user: int):
    user_uow = unit_of_work.UserUnitOfWork()
    try:
        user = service.get_user(user_uow, id_user)
    except exceptions.UserDoesNotExists as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return user


@app.get('/user/all', response_model=List[schema.User])
async def get_all_user():
    user_uow = unit_of_work.UserUnitOfWork()
    users = service.get_all_users(user_uow)
    return users
