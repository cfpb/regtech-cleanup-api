from typing import List
from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    SblTypeMappingDao,
)
from sqlalchemy.orm import Session
from sqlalchemy import text


def delete_domains_by_lei(
    session: Session, lei: str
) -> List[FinancialInstitutionDomainDao] | None:
    session.query(FinancialInstitutionDomainDao).filter(
        FinancialInstitutionDomainDao.lei == lei
    ).delete()
    session.commit()
    return {"OK": True}


def delete_sbl_type_by_lei(
    session: Session, lei: str
) -> List[SblTypeMappingDao] | None:
    session.query(SblTypeMappingDao).filter(SblTypeMappingDao.lei == lei).delete()
    # deleting from history tables
    del_hist_stmt = text("DELETE from fi_to_type_mapping_history where fi_id = :fi_id")
    session.execute(del_hist_stmt, {"fi_id": lei})
    session.commit()
    return {"OK": True}


def delete_institution(session: Session, lei: str) -> FinancialInstitutionDao | None:
    session.query(FinancialInstitutionDao).filter(
        FinancialInstitutionDao.lei == lei
    ).delete()

    # deleting from history tables
    del_hist_stmt = text("DELETE from financial_institutions_history where lei = :lei")
    session.execute(del_hist_stmt, {"lei": lei})
    session.commit()
    return {"OK": True}
