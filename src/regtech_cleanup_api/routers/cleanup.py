import logging

from concurrent.futures import ProcessPoolExecutor
from fastapi import Depends, Request
from regtech_api_commons.api.router_wrapper import Router
from typing import Annotated

from sbl_filing_api.entities.engine.engine import get_session


from regtech_cleanup_api.entities.repos import user_fi_repo, filing_repo

from sqlalchemy.ext.asyncio import AsyncSession

from regtech_api_commons.api.dependencies import verify_user_lei_relation
from regtech_user_fi_management.entities.models.dto import (
    FinancialInstitutionWithRelationsDto,
)

logger = logging.getLogger(__name__)


async def set_db(
    request: Request, session: Annotated[AsyncSession, Depends(get_session)]
):
    request.state.db_session = session


executor = ProcessPoolExecutor()
router = Router(dependencies=[Depends(set_db), Depends(verify_user_lei_relation)])


@router.get(
    "/{lei}",
    response_model=FinancialInstitutionWithRelationsDto,
    dependencies=[Depends(verify_user_lei_relation)],
)
def delete_institution(request: Request):
    pass


@router.get("/institutions/{lei}/filings/{period_code}")
def delete_filing(request: Request):
    pass
