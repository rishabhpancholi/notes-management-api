from typing import Annotated

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

class UserCreate(BaseModel):
    email: Annotated[EmailStr, Field(max_length = 255)]
    password: Annotated[str, Field(max_length = 255)]

class TokenData(BaseModel):
    id: int
    email: Annotated[EmailStr, Field(max_length = 255)]



