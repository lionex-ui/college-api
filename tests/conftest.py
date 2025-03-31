from pathlib import Path

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.config import db_config
from app.db.session import get_session
from app.main import app


@pytest.fixture(scope="session")
def init_db():
    base_dir = Path(__file__).resolve().parent.parent

    test_db_url = db_config.database_url.replace("+asyncpg", "") + "-test"

    base_url = test_db_url.rsplit("/", 1)[0]
    engine = create_engine(base_url)

    if not database_exists(test_db_url):
        create_database(test_db_url)

    alembic_cfg = Config(str(base_dir / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    alembic_cfg.set_main_option("script_location", str(base_dir / "migrations"))

    command.upgrade(alembic_cfg, "head")

    yield

    command.downgrade(alembic_cfg, "base")

    engine.dispose()
    if database_exists(test_db_url):
        drop_database(test_db_url)


@pytest_asyncio.fixture(scope="function")
async def db_session(init_db):
    engine = create_async_engine(db_config.database_url + "-test", echo=True)
    testing_session_local = async_sessionmaker(bind=engine)

    async with testing_session_local() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):

    async def override_get_db():
        async with db_session as session:
            yield session

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
