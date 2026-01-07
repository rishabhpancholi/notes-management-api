from typing import (
    Annotated,
    Optional
)

from pydantic import (
    BaseModel,
    Field
)

class CreateNote(BaseModel):
    title: Annotated[str, Field(max_length = 50)]
    content: Optional[str] = Field(default = None)

class UpdateNote(BaseModel):
    title: Optional[str] = Field(default = None, max_length = 50)
    content: Optional[str] = Field(default = None)

class CreateNoteReadAccess(BaseModel):
    user_id: Annotated[int, Field(ge = 1)]
    note_id: Annotated[int, Field(ge = 1)]

class DeleteNoteReadAccess(BaseModel):
    user_id: Annotated[int, Field(ge = 1)]
    note_id: Annotated[int, Field(ge = 1)]

class ReadableNote(BaseModel):
    user_id: Annotated[int, Field(ge = 1)]
    note_id: Annotated[int, Field(ge = 1)]