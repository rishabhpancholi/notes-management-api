import hashlib

import bcrypt

from sqlalchemy.ext.asyncio import AsyncEngine

from app.database.models import Base

async def init_db(engine: AsyncEngine)-> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def hash_password(password: str)-> str:
    sha = hashlib.sha256(password.encode("utf-8")).digest()
    hashed = bcrypt.hashpw(sha, bcrypt.gensalt()).decode("utf-8")

    return hashed

def verify_password(plain_password: str, hashed_password: str)-> bool:
    sha = hashlib.sha256(plain_password.encode("utf-8")).digest()

    return bcrypt.checkpw(sha, hashed_password.encode("utf-8"))