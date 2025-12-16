from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from Application.core.configuration import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.ASYNC_ENGINE_CREATE())

session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass
