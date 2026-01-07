from typing import List

from fastapi import (
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.schemas import (
    user_schemas,
    crud_schemas
)

async def create_note(
        note: crud_schemas.CreateNote,
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> models.Note:
    
    new_note = models.Note(
        **note.model_dump(),
        owner_id = current_user.id
    )

    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)

    return new_note

async def read_note(
        id: int,
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> models.Note:

   note = (
       await db.execute(
           select(models.Note).where(models.Note.id == id, models.Note.owner_id == current_user.id)
       )
   ).scalar_one_or_none()

   if not note:
       raise HTTPException(
           status_code = status.HTTP_404_NOT_FOUND,
           detail = "Note not found"
       )

   return note

async def read_all_notes(
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> List[models.Note]:
    
    notes = (
        await db.execute(
            select(models.Note).where(models.Note.owner_id == current_user.id)
        )
    ).scalars().all()

    return notes

async def update_note(
        id: int,
        note: crud_schemas.UpdateNote,
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> models.Note:

    note_to_update = (
        await db.execute(
            select(models.Note).where(models.Note.id == id, models.Note.owner_id == current_user.id)
        )
    ).scalar_one_or_none()

    if not note_to_update:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Note not found"
        )

    if note.title:
        note_to_update.title = note.title
    if note.content:
        note_to_update.content = note.content

    await db.commit()
    await db.refresh(note_to_update)

    return note_to_update

async def delete_note(
        id: int,
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> None:
    
    note_to_delete = (
        await db.execute(
            select(models.Note).where(models.Note.id == id, models.Note.owner_id == current_user.id)
        )
    ).scalar_one_or_none()

    if not note_to_delete:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Note not found"
        )
    
    await db.delete(note_to_delete)
    await db.commit()

async def give_read_access(
        note_read_access: crud_schemas.CreateNoteReadAccess,
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> models.NoteReadAccess:
    
    if note_read_access.user_id == current_user.id:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You cannot give read access to yourself"
        )
    
    existing_user = (
        await db.execute(
            select(models.User).where(models.User.id == note_read_access.user_id)
        )
    ).scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exist"
        )
    
    existing_note = (
        await db.execute(
            select(models.Note).where(models.Note.id == note_read_access.note_id)
        )
    ).scalar_one_or_none()

    if not existing_note:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Note does not exist"
    )

    existing_note_read_access = (
        await db.execute(
            select(models.NoteReadAccess).where(models.NoteReadAccess.note_id == note_read_access.note_id, models.NoteReadAccess.user_id == note_read_access.user_id, models.NoteReadAccess.note_owner_id == current_user.id)
        )
    ).scalar_one_or_none()

    if existing_note_read_access:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User already has read access to this note"
        )
    
    new_note_read_access = models.NoteReadAccess(**note_read_access.model_dump(), note_owner_id = current_user.id)

    db.add(new_note_read_access)
    await db.commit()
    await db.refresh(new_note_read_access)

    return new_note_read_access

async def revoke_read_access(
        note_read_access: crud_schemas.DeleteNoteReadAccess,
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> None:
    
    note_to_delete = (
        await db.execute(
            select(models.NoteReadAccess).where(models.NoteReadAccess.note_id == note_read_access.note_id, models.NoteReadAccess.user_id == note_read_access.user_id, models.NoteReadAccess.note_owner_id == current_user.id)
        )
    ).scalar_one_or_none()

    if not note_to_delete:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Note read access not found"
        )
    
    await db.delete(note_to_delete)
    await db.commit()

async def read_note_with_access(
        note: crud_schemas.ReadableNote,
        current_user: user_schemas.TokenData,
        db: AsyncSession
)-> models.Note:
    
    if note.user_id == current_user.id:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You already have access to your own note"
        )
    
    existing_user = (
        await db.execute(
            select(models.User).where(models.User.id == note.user_id)
        )
    ).scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exist"
        )
    
    existing_note = (
        await db.execute(
            select(models.Note).where(models.Note.id == note.note_id)
        )
    ).scalar_one_or_none()

    if not existing_note:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Note does not exist"
    )

    note_read_access = (
        await db.execute(
            select(models.NoteReadAccess).where(models.NoteReadAccess.note_id == note.note_id, models.NoteReadAccess.user_id == current_user.id, models.NoteReadAccess.note_owner_id == note.user_id)
        )
    ).scalar_one_or_none()

    if not note_read_access:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You do not have read access to this note"
        )

    note_with_access = (
        await db.execute(
            select(models.Note).where(models.Note.id == note.note_id, models.Note.owner_id == note.user_id)
        )
    ).scalar_one_or_none()

    if not note_with_access:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Note not found"
        )

    return note_with_access