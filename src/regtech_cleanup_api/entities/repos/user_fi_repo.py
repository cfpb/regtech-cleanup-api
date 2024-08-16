import logging


from typing import TypeVar, List
from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    SblTypeMappingDao,
)
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

T = TypeVar("T")


def delete_domains_by_lei(
    session: Session, lei: str
) -> List[FinancialInstitutionDomainDao] | None:
    delete_domains = session.query(FinancialInstitutionDomainDao).filter(
        FinancialInstitutionDomainDao.lei == lei
    )
    if delete_domains:
        delete_domains.delete(synchronize_session=False)
        session.commit()
    return delete_domains


def delete_sbl_type_by_lei(
    session: Session, lei: str
) -> List[SblTypeMappingDao] | None:
    delete_sbl_type = session.query(SblTypeMappingDao).filter(
        SblTypeMappingDao.lei == lei
    )
    if delete_sbl_type:
        delete_sbl_type.delete(synchronize_session=False)
        session.commit()
    return delete_sbl_type


def delete_institution(session: Session, lei: str) -> FinancialInstitutionDao | None:
    delete_institution = (
        session.query(FinancialInstitutionDao)
        .filter(FinancialInstitutionDao.lei == lei)
        .first
    )
    if delete_institution:
        delete_institution.delete(synchronize_session=False)
        session.commit()
    return delete_institution
