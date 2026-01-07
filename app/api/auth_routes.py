from fastapi import (
    APIRouter,
    Depends,
    status
)
from fastapi.security.oauth2 import OAuth2PasswordRequestFormStrict

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.utils import responses
from app.schemas import user_schemas
from app.services import auth_service

auth_router = APIRouter(tags = ["Authentication"])

@auth_router.post(
    "/auth/signup",
    response_model = responses.UserCreated,
    status_code = status.HTTP_201_CREATED
)
async def signup(
    user: user_schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    new_user =  await auth_service.signup(user, db)
    return new_user

@auth_router.post(
    "/auth/login",
    response_model = responses.UserToken
)
async def login(
    user_credentials: OAuth2PasswordRequestFormStrict = Depends(),
    db: AsyncSession = Depends(get_db)
):
    generated_token_response = await auth_service.login(user_credentials, db)
    return generated_token_response

@auth_router.delete(
    "/auth/delete",
    status_code = status.HTTP_204_NO_CONTENT
)
async def delete(
    user_credentials: OAuth2PasswordRequestFormStrict = Depends(),
    db: AsyncSession = Depends(get_db)
):
    await auth_service.delete(user_credentials, db)