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
    "/{lei}",
    response_model=FinancialInstitutionWithRelationsDto,
    dependencies=[Depends(verify_user_lei_relation)],
)
def delete_institution(request: Request, lei: str):
    if not is_valid_cleanup_lei(lei):
        raise RegTechHttpException(
            HTTPStatus.NOT_ACCEPTABLE,
            name="Invalid LEI",
            detail=f"Not a valid LEI {lei}",
        )
    else:
        return delete_helper(lei, request.state.db_session)


def delete_helper(lei: str, session: Session):
    try:
        repo.delete_domains_by_lei(session, lei)
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="Domains Delete Failed",
            detail=f"Failed to delete domains for LEI {lei}",
        ) from e

    try:
        repo.delete_sbl_type_by_lei(session, lei)
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="Sbl Type Delete Failed",
            detail=f"Failed to delete sbl_types for LEI {lei}",
        ) from e

    res = repo.delete_institution(session, lei)
    if not res:
        raise RegTechHttpException(
            HTTPStatus.NOT_FOUND,
            name="Institution Delete Failed",
            detail=f"Institution LEI {lei} not found.",
        )
    else:
        try:
            oauth2_admin.delete_group(lei)
        except Exception:
            raise RegTechHttpException(
                HTTPStatus.NOT_FOUND,
                name="Group Delete Failed",
                detail=f"The group associated with LEI {lei} not found.",
            )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
