import logging

from concurrent.futures import ProcessPoolExecutor
from fastapi import Depends, Request
from regtech_api_commons.api.router_wrapper import Router
from regtech_cleanup_api.entities.engine.engine import get_institution_session
from regtech_cleanup_api.entities.repos import user_fi_repo as repo
from sqlalchemy.orm import Session
from regtech_api_commons.api.dependencies import verify_user_lei_relation
from regtech_user_fi_management.entities.models.dto import (
    FinancialInstitutionWithRelationsDto,
)
from regtech_api_commons.api.exceptions import RegTechHttpException
from http import HTTPStatus
from regtech_api_commons.oauth2.oauth2_admin import OAuth2Admin
from regtech_user_fi_management.config import kc_settings
from regtech_cleanup_api.services.validation import is_valid_cleanup_lei

logger = logging.getLogger(__name__)
oauth2_admin = OAuth2Admin(kc_settings)


async def set_db(request: Request, session: Session = Depends(get_institution_session)):
    request.state.db_session = session


executor = ProcessPoolExecutor()
router = Router(dependencies=[Depends(set_db), Depends(verify_user_lei_relation)])


@router.get(
    "/{lei}",
    response_model=FinancialInstitutionWithRelationsDto,
    dependencies=[Depends(verify_user_lei_relation)],
)
def delete_institution(request: Request, lei: str):
    if not is_valid_cleanup_lei(lei):
        raise RegTechHttpException(
            HTTPStatus.NOT_ACCEPTABLE,
            name="Not Test LEI",
            detail=f"{lei} not valid test lei.",
        )
    else:
        delete_domains = repo.delete_domains_by_lei(request.state.db_session, lei)
        if delete_domains:
            logger.log(f"Deleted domain(s) for LEI {lei}")

        delete_sbl_type = repo.delete_sbl_type_by_lei(request.state.db_session, lei)
        if delete_sbl_type:
            logger.log(f"Deleted sbl type(s) for LEI {lei}")

        res = repo.delete_institution(request.state.db_session, lei)
        if not res:
            raise RegTechHttpException(
                HTTPStatus.NOT_FOUND,
                name="Institution to be deleted Not Found",
                detail=f"{lei} not found.",
            )
        else:
            oauth2_admin.delete_group(lei)

        return res
