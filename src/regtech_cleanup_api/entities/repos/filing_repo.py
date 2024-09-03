
from typing import TypeVar, Any
from sbl_filing_api.entities.models.dao import (
    UserActionDAO,
    FilingDAO,
    SubmissionDAO,
    ContactInfoDAO,
)
from sbl_filing_api.entities.repos import submission_repo
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def get_user_action_ids(
    session: AsyncSession, lei: str = None, period_code: str = None
):
    filing = await submission_repo.get_filing(session, lei, period_code)
    submissions = await submission_repo.get_submissions(session, lei, period_code)
    user_action_ids = list(
        set(
            [s.submitter_id for s in submissions if s.submitter_id is not None]
            + [a.accepter_id for a in submissions if a.accepter_id is not None]
            + [filing.creator_id]
            if filing.creator_id is not None
            else []
        )
    )
    return user_action_ids


async def get_contact_info(
    session: AsyncSession, lei: str = None, period_code: str = None
):
    filing = await submission_repo.get_filing(session, lei, period_code)
    if filing and filing.contact_info:
        return filing.contact_info


async def delete_user_action(session: AsyncSession, user_action_id: int):
    await delete_helper(session, UserActionDAO, user_action_id)


async def delete_user_actions(session: AsyncSession, user_action_ids):
    [await delete_user_action(session, ua) for ua in user_action_ids]


async def delete_filing(
    session: AsyncSession, lei: str = None, period_code: str = None
):
    filing = await submission_repo.get_filing(session, lei, period_code)
    if filing:
        await delete_helper(session, FilingDAO, filing.id)
    else:
        logger.info(f"No filing data to be deleted for LEI {lei}")


async def delete_submission(session: AsyncSession, submission_id: int):
    await delete_helper(session, SubmissionDAO, submission_id)


async def delete_submissions(
    session: AsyncSession, lei: str = None, period_code: str = None
):
    submissions = await submission_repo.get_submissions(session, lei, period_code)
    if submissions:
        [await delete_submission(session, s.id) for s in submissions]
    else:
        logger.info(f"No submission data to be deleted for LEI {lei}")


async def delete_contact_info(
    session: AsyncSession, lei: str = None, period_code: str = None
):
    contact_info = await get_contact_info(session, lei, period_code)
    if contact_info:
        await delete_helper(session, ContactInfoDAO, contact_info.id)
    else:
        logger.info(f"No contact info to be deleted for LEI {lei}")


async def delete_helper(session: AsyncSession, table_obj: T, table_id: Any):
    stmt = (
        delete(table_obj)
        .filter(table_obj.id == table_id)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt)
    await session.commit()
