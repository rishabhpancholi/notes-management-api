from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas import (
    crud_schemas,
    user_schemas
)
from app.utils import responses
from app.services import crud_service

crud_router = APIRouter(tags = ["CRUD"])

@crud_router.post(
    "/notes/create",
    status_code = status.HTTP_201_CREATED,
    response_model = responses.NoteCreated
)
async def create_note(
    note: crud_schemas.CreateNote,
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    new_note = await crud_service.create_note(note, current_user, db)
    return new_note
    
@crud_router.get(
    "/notes/read",
    response_model = responses.NoteOut
)
async def read_note(
    id: int = Query(..., ge = 1),
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    note = await crud_service.read_note(id, current_user, db)
    return note

@crud_router.get(
    "/notes/read-all",
    response_model = List[responses.NoteOut]
)
async def read_all_notes(
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    notes = await crud_service.read_all_notes(current_user, db)
    return notes

@crud_router.put(
    "/notes/update",
    response_model = responses.NoteUpdated
)
async def update_note(
    note: crud_schemas.UpdateNote,
    id: int = Query(..., ge = 1),
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    updated_note = await crud_service.update_note(id, note, current_user, db)
    return updated_note

@crud_router.delete(
    "/notes/delete",
    status_code = status.HTTP_204_NO_CONTENT
)
async def delete_note(
    id: int = Query(..., ge = 1),
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    await crud_service.delete_note(id, current_user, db)

@crud_router.post(
    "/notes/give-read-access",
    status_code = status.HTTP_201_CREATED,
    response_model = responses.NoteReadAccess
)
async def give_read_access(
    note_read_access: crud_schemas.CreateNoteReadAccess,
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    new_note_read_access = await crud_service.give_read_access(note_read_access, current_user, db)
    return new_note_read_access

@crud_router.delete(
    "/notes/revoke-read-access",
    status_code = status.HTTP_204_NO_CONTENT,
)
async def revoke_read_access(
    note_read_access: crud_schemas.DeleteNoteReadAccess,
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    await crud_service.revoke_read_access(note_read_access, current_user, db)

@crud_router.post(
    "/notes/read-note-with-access",
    response_model = responses.NoteWithReadAccess
)
async def read_note_with_access(
    note: crud_schemas.ReadableNote,
    current_user: user_schemas.TokenData = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
):
    note_with_access = await crud_service.read_note_with_access(note, current_user, db)
    return note_with_access