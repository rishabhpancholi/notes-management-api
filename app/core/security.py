from datetime import (
    datetime,
    timezone,
    timedelta
)

from typing import Dict

from jose import (
    JWTError,
    ExpiredSignatureError,
    jwt 
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.schemas import user_schemas
from app.core.config import app_config

SECRET_KEY = app_config.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: Dict)-> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

async def verify_access_token(
        token: str, 
        db: AsyncSession,
        credential_exception: Exception
)-> user_schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        id = payload.get("id")
        email = payload.get("email")

        if id is None:
            raise credential_exception
        
        user = (
            await db.execute(
                select(models.User).where(models.User.id == id)
            )
        ).scalar_one_or_none()

        if not user:
            raise credential_exception
        
        token_data = user_schemas.TokenData(
            id = id,
            email = email
        )

        return token_data
    except JWTError:
        raise credential_exception
    except ExpiredSignatureError:
        raise credential_exception