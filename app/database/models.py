from typing import List

from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Text,
    DateTime,
    func
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    email: Mapped[str] = mapped_column(String(255), unique = True, index = True, nullable = False)
    password: Mapped[str] = mapped_column(String(255), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), server_default = func.now())

    notes: Mapped[List["Note"]] = relationship(
        back_populates = "user", 
        cascade = "all, delete-orphan"
    )

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key = True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    title: Mapped[str] = mapped_column(String(50), nullable = False)
    content: Mapped[str] = mapped_column(Text, nullable = True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), server_default = func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), server_default = func.now(), onupdate = func.now())

    user: Mapped["User"] = relationship(
        back_populates = "notes"
    )


class NoteReadAccess(Base):
    __tablename__ = "note_read_access"
 
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(Integer, nullable = False)
    note_owner_id: Mapped[int] = mapped_column(Integer, nullable = False)
    note_id: Mapped[int] = mapped_column(Integer, nullable = False)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), server_default = func.now())








































    