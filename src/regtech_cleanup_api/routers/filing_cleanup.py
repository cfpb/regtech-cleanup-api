import logging

from concurrent.futures import ProcessPoolExecutor
from http import HTTPStatus

from fastapi import Depends, Request, Response, status
from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.router_wrapper import Router
from typing import Annotated

from regtech_cleanup_api.entities.engine.engine import get_filing_session

from sqlalchemy.orm import Session

from regtech_api_commons.api.dependencies import verify_user_lei_relation

import regtech_cleanup_api.entities.repos.filing_repo as repo
from regtech_cleanup_api.services.cleanup_processor import delete_from_storage
from regtech_cleanup_api.services.validation import is_valid_cleanup_lei

logger = logging.getLogger(__name__)


def set_db(request: Request, session: Annotated[Session, Depends(get_filing_session)]):
    request.state.db_session = session


executor = ProcessPoolExecutor()
router = Router(dependencies=[Depends(set_db), Depends(verify_user_lei_relation)])


@router.delete("/institutions/{lei}/filings/{period_code}")
def delete_filing(request: Request, lei: str, period_code: str):
    if is_valid_cleanup_lei(lei):
        try:
            session = request.state.db_session
            try:
                repo.delete_contact_info(session, lei, period_code)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Contact Info Delete Failed",
                    detail="Failed to delete contact info",
                ) from e

            try:
                user_action_ids = repo.get_user_action_ids(session, lei, period_code)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Missing User Action Data",
                    detail="Failed to get user action data",
                ) from e

            try:
                repo.delete_submissions(session, lei, period_code)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Submission Delete Failed",
                    detail="Failed to delete submission data",
                ) from e

            try:
                repo.delete_filing(session, lei, period_code)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Filing Delete Failed",
                    detail="Failed to delete filing data",
                ) from e

            try:
                repo.delete_user_actions(session, user_action_ids)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="User Action Delete Failed",
                    detail="Failed to delete user action data",
                ) from e

            delete_from_storage(period_code, lei)

        except Exception as e:
            raise e
    else:
        raise RegTechHttpException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            name="Invalid LEI",
            detail="Not a valid LEI",
        )
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/institutions/{lei}/submissions/{period_code}")
def delete_submissions(request: Request, lei: str, period_code: str):
    if is_valid_cleanup_lei(lei):
        try:
            session = request.state.db_session
            try:
                user_action_ids = repo.get_user_action_ids(
                    session, lei=lei, period_code=period_code, submissions=True
                )
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Missing User Action Data",
                    detail="Failed to get user action data",
                ) from e
            try:
                repo.delete_submissions(session, lei, period_code)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Submission Delete Failed",
                    detail="Failed to delete submission data",
                ) from e
            try:
                repo.delete_user_actions(session, user_action_ids)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="User Action Delete Failed",
                    detail="Failed to delete user action data",
                ) from e
        except Exception as e:
            raise e
    else:
        raise RegTechHttpException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            name="Invalid LEI",
            detail="Not a valid LEI",
        )
    return Response(status_code=status.HTTP_202_ACCEPTED)
