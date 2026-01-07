from typing import Optional

from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

class UserCreated(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserToken(BaseModel):
    access_token: str
    token_type: str

class Note(BaseModel):
    id: int
    owner_id: int
    title: str
    content: Optional[str] = Field(default = None)
    created_at: datetime

    class Config:
        from_attributes = True


class NoteCreated(Note):
    pass

class NoteOut(Note):
    pass

class NoteUpdated(Note):
    updated_at: datetime

class NoteReadAccess(BaseModel):
    user_id: int
    note_owner_id: int
    note_id: int
    granted_at: datetime

    class Config:
        from_attributes = True

class NoteWithReadAccess(Note):
    pass