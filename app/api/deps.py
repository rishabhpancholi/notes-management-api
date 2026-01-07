from typing import AsyncGenerator

from fastapi import (
    HTTPException,
    Depends,
    status
)
from fastapi.security.oauth2 import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import user_schemas
from app.core.security import verify_access_token
from app.database.connection import AsyncSessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/login")

async def get_db()-> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
)-> user_schemas.TokenData:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    return await verify_access_token(token, db, credentials_exception)