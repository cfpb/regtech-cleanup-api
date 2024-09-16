"""
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.pool import NullPool
from asyncio import current_task
from regtech_cleanup_api.config import institution_settings, filing_settings

user_fi_engine = create_async_engine(
    str(institution_settings.inst_conn),
    echo=institution_settings.db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: institution_settings.inst_db_schema})
InstitutionSessionLocal = async_scoped_session(
    async_sessionmaker(user_fi_engine, expire_on_commit=False), current_task
)

filing_engine = create_async_engine(
    filing_settings.conn.unicode_string(),
    echo=filing_settings.db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: filing_settings.db_schema})
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
"""

from sqlalchemy.pool import NullPool
from regtech_cleanup_api.config import institution_settings, filing_settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

user_fi_engine = create_engine(
    str(institution_settings.inst_conn),
    echo=institution_settings.db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: institution_settings.inst_db_schema})
InstitutionSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=user_fi_engine)


filing_engine = create_engine(
    filing_settings.conn.unicode_string(),
    echo=filing_settings.db_logging,
    poolclass=NullPool,
).execution_options(schema_translate_map={None: filing_settings.db_schema})
FilingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=filing_engine)


def get_institution_session():
    session = InstitutionSessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_filing_session():
    session = FilingSessionLocal()
    try:
        yield session
    finally:
        session.close()
