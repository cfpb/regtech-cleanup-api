import logging
from typing import List
from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    SblTypeMappingDao,
)
from sqlalchemy.orm import Session
from sqlalchemy import text
from regtech_cleanup_api.entities.repos import repo_utils

logger = logging.getLogger(__name__)


def delete_domains_by_lei(session: Session, lei: str) -> List[FinancialInstitutionDomainDao] | None:
    repo_utils.delete_helper(session, FinancialInstitutionDomainDao, lei)


def delete_sbl_type_by_lei(session: Session, lei: str) -> List[SblTypeMappingDao] | None:
    stmt = session.query(SblTypeMappingDao).filter(SblTypeMappingDao.lei == lei)
    sbl_types = session.execute(stmt)

    if sbl_types:
        repo_utils.delete_helper(session, SblTypeMappingDao, lei)
        # deleting from history tables
        del_hist_stmt = text("DELETE from fi_to_type_mapping_history where fi_id = :fi_id")
        session.execute(del_hist_stmt, {"fi_id": lei})
        session.commit()
    else:
        logger.warning(f"No Domain(s) for LEI {lei} found.")


def delete_institution(session: Session, lei: str) -> FinancialInstitutionDao | None:
    stmt = session.query(FinancialInstitutionDao).filter(FinancialInstitutionDao.lei == lei).delete()
    fi = session.execute(stmt)

    if fi:
        repo_utils.delete_helper(session, FinancialInstitutionDao, lei)
        # deleting from history tables
        del_hist_stmt = text("DELETE from financial_institutions_history where lei = :lei")
        session.execute(del_hist_stmt, {"lei": lei})
        session.commit()
    else:
        logger.warning(f"No sbl type(s) for LEI {lei} found.")
