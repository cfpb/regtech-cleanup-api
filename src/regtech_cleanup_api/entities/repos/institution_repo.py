from typing import List
from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    SblTypeMappingDao,
)
from sqlalchemy.orm import Session


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
    session.commit()
    return {"OK": True}


def delete_institution(session: Session, lei: str) -> FinancialInstitutionDao | None:
    session.query(FinancialInstitutionDao).filter(
        FinancialInstitutionDao.lei == lei
    ).delete()
    session.commit()
    return {"OK": True}
