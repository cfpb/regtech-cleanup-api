from sqlalchemy.pool import NullPool
from regtech_cleanup_api.config import user_fi_settings, filing_settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

user_fi_engine = create_engine(
    user_fi_settings.conn.unicode_string(),
    echo=user_fi_settings.user_fi_db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: user_fi_settings.user_fi_db_schema})
InstitutionSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=user_fi_engine
)


filing_engine = create_engine(
    filing_settings.conn.unicode_string(),
    echo=filing_settings.filing_db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: filing_settings.filing_db_schema})
FilingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=filing_engine)


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
