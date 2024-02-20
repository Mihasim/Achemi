import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from SQLalchemy.CRUD import Searching
from config import settings

TEST_DB = "testdb"


engine = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRESQL_USERNAME}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOSTNAME}/{settings.POSTGRESQL_DATABASE}",
    echo=True, pool_size=6, max_overflow=10)
session = Session(bind=engine)


@pytest.fixture
def searching_data():
    return Searching()


def test_search_name(searching_data):
    searching_name = searching_data.search_name("Showing Off")
    print(searching_name)
    assert isinstance(searching_name, list)
    assert searching_name != []


def test_search_tags(searching_data):
    assert isinstance(searching_data.search_tags("graphs"), list)
    assert searching_data.search_tags("graphs") != []
