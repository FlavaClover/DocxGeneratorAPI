from fastapi import FastAPI, Response
from src import config
from src.adapters import orm, repository
from src.domain import schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

orm.start_mapper()
engine = create_engine(config.get_sqlite_uri(), echo=True)
orm.metadata.create_all(engine)
get_session = sessionmaker(engine)


app = FastAPI()


@app.post('/user/create')
async def create_user(user: schema.User):
    session = get_session()
    user_repo = repository.UserRepository(session)
    user_repo.add(user)
    session.commit()
    return Response(status_code=200)


@app.get('/user/all', response_model=List[schema.User])
async def all_user():
    user_repo = repository.UserRepository(get_session())
    print(user_repo.all())
    return user_repo.all()


@app.get('/user/get/{id_user}', response_model=schema.User)
async def get_user(id_user: int):
    user_repo = repository.UserRepository(get_session())
    return user_repo.get_by_id(id_user)
