import logging


from typing import TypeVar, List
from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    SblTypeMappingDao,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def delete_domains_by_lei(
    session: AsyncSession, lei: str
) -> List[FinancialInstitutionDomainDao] | None:
    stmt = delete(FinancialInstitutionDomainDao).where(
        FinancialInstitutionDomainDao.lei == lei
    )

    await session.execute(stmt)
    await session.commit()
    return await session.deleted


async def delete_sbl_type_by_lei(
    session: AsyncSession, lei: str
) -> List[SblTypeMappingDao] | None:
    stmt = delete(SblTypeMappingDao).where(SblTypeMappingDao.lei == lei)

    await session.execute(stmt)
    await session.commit()
    return await session.deleted


async def delete_institution(
    session: AsyncSession, lei: str
) -> FinancialInstitutionDao | None:
    stmt = delete(FinancialInstitutionDao).where(FinancialInstitutionDao.lei == lei)

    await session.execute(stmt)
    await session.commit()
    return await session.deleted
