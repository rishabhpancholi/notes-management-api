from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from app.core.config import app_config

engine = create_async_engine(
    app_config.postgres_uri,
    future = True
)

AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    autoflush = False,
    expire_on_commit = False
)