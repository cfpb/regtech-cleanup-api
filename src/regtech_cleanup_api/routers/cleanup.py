import logging

from concurrent.futures import ProcessPoolExecutor
from http import HTTPStatus

from fastapi import Depends, Request, Response, status
from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.router_wrapper import Router
from typing import Annotated
from starlette.authentication import requires

from regtech_cleanup_api.entities.engine.engine import (
    get_filing_session,
    get_institution_session,
)

from sqlalchemy.orm import Session

from regtech_api_commons.api.dependencies import verify_user_lei_relation

import regtech_cleanup_api.entities.repos.submission_repo as submission_repo

from regtech_cleanup_api.routers.institution_cleanup import (
    delete_helper as institution_delete_helper,
)
from regtech_cleanup_api.routers.filing_cleanup import (
    delete_helper as filing_delete_helper,
)

from regtech_cleanup_api.services.validation import is_valid_cleanup_lei

logger = logging.getLogger(__name__)


def set_institution_db(request: Request, session: Session = Depends(get_institution_session)):
    request.state.institution_db_session = session


def set_filing_db(request: Request, session: Annotated[Session, Depends(get_filing_session)]):
    request.state.filing_db_session = session


executor = ProcessPoolExecutor()
router = Router(
    dependencies=[
        Depends(set_filing_db),
        Depends(set_institution_db),
        Depends(verify_user_lei_relation),
    ]
)


@router.delete("/{lei}")
@requires("authenticated")
def delete_all_things(request: Request, lei: str):
    if not is_valid_cleanup_lei(lei):
        raise RegTechHttpException(
            HTTPStatus.NOT_ACCEPTABLE,
            name="Invalid LEI",
            detail=f"Not a valid LEI {lei}",
        )
    else:
        institution_delete_helper(lei, request.state.institution_db_session)

        filings = submission_repo.get_filings(request.state.filing_db_session, lei)
        for f in filings:
            filing_delete_helper(f.lei, f.filing_period, request.state.filing_db_session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
