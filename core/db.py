from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated
from core.config import get_settings

settings = get_settings()
postgresql_database_url = settings.DATABASE_STRING

engine = create_engine(postgresql_database_url, echo=False)


def initialize_db():
    print("init db")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
