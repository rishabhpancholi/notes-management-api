from typing import Dict

from fastapi import (
    HTTPException,
    status
)
from fastapi.security.oauth2 import OAuth2PasswordRequestFormStrict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import utils
from app.database import models
from app.schemas import user_schemas
from app.core.security import create_access_token

async def signup(
        user: user_schemas.UserCreate, 
        db: AsyncSession
)-> models.User:

    existing_user = (
        await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this email already exists"
        )
    
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def login(
        user_credentials: OAuth2PasswordRequestFormStrict,
        db: AsyncSession
)-> Dict:
    
    user = (
        await db.execute(
            select(models.User).where(models.User.email == user_credentials.username)
        )
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )

    token = create_access_token(
        {
            "id": user.id,
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

async def delete(
        user_credentials: OAuth2PasswordRequestFormStrict,
        db: AsyncSession
)-> None:
    user = (
        await db.execute(
            select(models.User).where(models.User.email == user_credentials.username)
        )
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )
    
    await db.delete(user)
    await db.commit()