from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core.config import DATABASE_URL

# Create the base class
Base = declarative_base()

# Database ENGINE - Configure async connection
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Enable SQL query logging
    pool_size=10,
    max_overflow=20
)

# AsyncSessionLocal
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db():
    """Dependency for getting async DB session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()