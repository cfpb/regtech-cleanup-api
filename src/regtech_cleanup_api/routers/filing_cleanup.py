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


@router.delete("/{lei}/{period_code}")
def delete_filing(request: Request, lei: str, period_code: str):
    if not is_valid_cleanup_lei(lei):
        raise RegTechHttpException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            name="Invalid LEI",
            detail=f"Not a valid LEI {lei}",
        )
    else:
        try:
            session = request.state.db_session
            delete_helper(lei, period_code, session)

        except Exception as e:
            raise RegTechHttpException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                name="Delete Filing Server Error",
                detail=f"Server error while trying to delete filing for LEI {lei}.",
            ) from e
        return Response(status_code=status.HTTP_204_NO_CONTENT)


def delete_helper(lei: str, period_code: str, session: Session):
    try:
        repo.delete_contact_info(session, lei, period_code)
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="Contact Info Delete Failed",
            detail=f"Failed to delete contact info for LEI {lei}",
        ) from e

    try:
        user_action_ids = repo.get_user_action_ids(session, lei, period_code)
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="Missing User Action Data",
            detail=f"Failed to get user action data for LEI {lei}",
        ) from e

    try:
        repo.delete_submissions(session, lei, period_code)
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="Submission Delete Failed",
            detail=f"Failed to delete submission data for LEI {lei}",
        ) from e

    try:
        repo.delete_filing(session, lei, period_code)
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="Filing Delete Failed",
            detail=f"Failed to delete filing data for LEI {lei}",
        ) from e

    try:
        repo.delete_user_actions(session, user_action_ids)
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="User Action Delete Failed",
            detail=f"Failed to delete user action data for LEI {lei}",
        ) from e

    delete_from_storage(period_code, lei)


@router.delete("/submissions/{lei}/{period_code}")
def delete_submissions(request: Request, lei: str, period_code: str):
    if is_valid_cleanup_lei(lei):
        try:
            session = request.state.db_session
            try:
                user_action_ids = repo.get_user_action_ids(
                    session, lei=lei, period_code=period_code, just_submissions=True
                )
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Missing User Action Data",
                    detail=f"Failed to get user action data for LEI {lei}",
                ) from e
            try:
                repo.delete_submissions(session, lei, period_code)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="Submission Delete Failed",
                    detail=f"Failed to delete submission data for LEI {lei}",
                ) from e
            try:
                repo.delete_user_actions(session, user_action_ids)
            except Exception as e:
                raise RegTechHttpException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    name="User Action Delete Failed",
                    detail=f"Failed to delete user action data for LEI {lei}",
                ) from e

            delete_from_storage(period_code, lei)

        except Exception as e:
            raise e
    else:
        raise RegTechHttpException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            name="Invalid LEI",
            detail=f"Not a valid LEI {lei}",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
