from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from .settings import settings


engine: AsyncEngine = create_async_engine(settings.database_url, echo=True,pool_pre_ping=True)

async def get_session():
    async with AsyncSession(engine) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
        