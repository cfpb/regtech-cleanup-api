import logging

from concurrent.futures import ProcessPoolExecutor
from http import HTTPStatus

from fastapi import Depends, Request
from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.router_wrapper import Router
from typing import Annotated

from regtech_cleanup_api.entities.engine.engine import get_filing_session


from regtech_cleanup_api.entities.repos import filing_repo

from sqlalchemy.ext.asyncio import AsyncSession

from regtech_api_commons.api.dependencies import verify_user_lei_relation

from regtech_cleanup_api.services.cleanup_processor import delete_from_storage
from regtech_cleanup_api.services.validation import is_valid_cleanup_lei

logger = logging.getLogger(__name__)


async def set_db(
    request: Request, session: Annotated[AsyncSession, Depends(get_filing_session)]
):
    request.state.db_session = session


executor = ProcessPoolExecutor()
router = Router(dependencies=[Depends(set_db), Depends(verify_user_lei_relation)])


@router.get("/institutions/{lei}/filings/{period_code}")
def delete_filing(request: Request, lei: str, period_code: str):
    if is_valid_cleanup_lei(lei):
        delete_from_storage(period_code, lei)
    else:
        raise RegTechHttpException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            name="Invalid LEI",
            detail="Not a valid LEI",
        )
