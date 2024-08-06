from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.pool import NullPool
from asyncio import current_task
from regtech_cleanup_api.config import user_fi_settings, filing_settings

user_fi_engine = create_async_engine(
    user_fi_settings.conn.unicode_string(),
    echo=user_fi_settings.user_fi_db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: user_fi_settings.user_fi_db_schema})
InstitutionSessionLocal = async_scoped_session(
    async_sessionmaker(user_fi_engine, expire_on_commit=False), current_task
)

filing_engine = create_async_engine(
    filing_settings.conn.unicode_string(),
    echo=filing_settings.filing_db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: filing_settings.filing_db_schema})
FilingSessionLocal = async_scoped_session(
    async_sessionmaker(filing_engine, expire_on_commit=False), current_task
)


async def get_institution_session():
    session = InstitutionSessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def get_filing_session():
    session = FilingSessionLocal()
    try:
        yield session
    finally:
        await session.close()
