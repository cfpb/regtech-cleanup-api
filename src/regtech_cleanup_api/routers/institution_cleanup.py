import logging

from concurrent.futures import ProcessPoolExecutor
from fastapi import Depends, Request, status
from fastapi.responses import Response
from regtech_api_commons.api.router_wrapper import Router
from regtech_cleanup_api.entities.engine.engine import get_institution_session
from regtech_cleanup_api.entities.repos import institution_repo as repo
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


def set_db(request: Request, session: Session = Depends(get_institution_session)):
    request.state.db_session = session


executor = ProcessPoolExecutor()
router = Router(dependencies=[Depends(set_db), Depends(verify_user_lei_relation)])


@router.delete(
    "/institution/{lei}",
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
        return delete_helper(lei, request.state.db_session)


def delete_helper(lei: str, session: Session):
    delete_domains = repo.delete_domains_by_lei(session, lei)
    if not delete_domains:
        logger.error(f"Domain(s) for LEI {lei} not deleted.")

    delete_sbl_type = repo.delete_sbl_type_by_lei(session, lei)
    if not delete_sbl_type:
        logger.error(f"sbl type(s) for LEI {lei} not deleted.")

    res = repo.delete_institution(session, lei)
    if not res:
        raise RegTechHttpException(
            HTTPStatus.NOT_FOUND,
            name="Institution to be deleted Not Found",
            detail=f"{lei} not found.",
        )
    else:
        try:
            oauth2_admin.delete_group(lei)
        except Exception:
            raise RegTechHttpException(
                HTTPStatus.NOT_FOUND,
                name="Group Not Found",
                detail=f"The group to be deleted {lei} not found.",
            )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
