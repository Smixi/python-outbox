from os import environ as env

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from python_outbox.sqlalchemy_outbox.sqlalchemy_base import Base
from python_outbox.sqlalchemy_outbox.sqlalchemy_storage_box import (
    SQLAlchemyStorageBoxMixin,
)

POSTGRES_HOST = env.get("POSTGRES_HOST", "postgres")
POSTGRES_PASSWORD = env.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_USER = env.get("POSTGRES_USER", "postgres")
POSTGRES_PORT = env.get("POSTGRES_PORT", "5432")
POSTGRES_TABLE = env.get("POSTGRES_TABLE", "postgres")


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_TABLE}",
        json_serializer=SQLAlchemyStorageBoxMixin.serializer,
    )


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
