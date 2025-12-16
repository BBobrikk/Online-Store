from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Application.core.connection import session
from fastapi.security import OAuth2PasswordRequestForm


async def get_session():
    async with session.begin() as sess:
        yield sess


SessionDep = Annotated[AsyncSession, Depends(get_session)]
