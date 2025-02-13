import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.session import get_session
from app.main import app

BASE_DIR = Path(__file__).resolve().parent.parent
ALEMBIC_INI_PATH = BASE_DIR / "alembic.ini"
MIGRATIONS_PATH = BASE_DIR / "migrations"


TEST_DATABASE_URL = "url"


engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def init_db():
    alembic_cfg = Config(str(ALEMBIC_INI_PATH))
    alembic_cfg.set_main_option(
        "sqlalchemy.url", TEST_DATABASE_URL.replace("+asyncpg", "")
    )
    alembic_cfg.set_main_option("script_location", str(MIGRATIONS_PATH))

    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest_asyncio.fixture(scope="function")
async def db_session(init_db):
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):

    async def override_get_db():
        async with db_session as session:
            yield session

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
