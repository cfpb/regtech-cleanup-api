import logging
from typing import TypeVar, Any
from sbl_filing_api.entities.models.dao import (
    UserActionDAO,
    FilingDAO,
    SubmissionDAO,
    ContactInfoDAO,
)

from sqlalchemy.orm import Session

from regtech_cleanup_api.entities.repos import submission_repo

logger = logging.getLogger(__name__)

T = TypeVar("T")


def get_user_action_ids(
    session: Session,
    lei: str = None,
    period_code: str = None,
    just_submissions: bool = False,
):
    filing_user_action_id = []
    if not just_submissions:
        filing = submission_repo.get_filing(session, lei, period_code)
        filing_user_action_id = [filing.creator_id] if filing.creator_id else []
    submissions = submission_repo.get_submissions(session, lei, period_code)
    user_action_ids = list(
        set(
            [s.submitter_id for s in submissions if s.submitter_id is not None]
            + [a.accepter_id for a in submissions if a.accepter_id is not None]
            + filing_user_action_id
        )
    )
    return user_action_ids


def get_contact_info(session: Session, lei: str = None, period_code: str = None):
    filing = submission_repo.get_filing(session, lei, period_code)
    if filing and filing.contact_info:
        return filing.contact_info


def delete_user_action(session: Session, user_action_id: int):
    delete_helper(session, UserActionDAO, user_action_id)


def delete_user_actions(session: Session, user_action_ids):
    [delete_user_action(session, ua) for ua in user_action_ids]


def delete_filing(session: Session, lei: str = None, period_code: str = None):
    filing = submission_repo.get_filing(session, lei, period_code)
    if filing:
        delete_helper(session, FilingDAO, filing.id)
    else:
        logger.info(f"No filing data to be deleted for LEI {lei}")


def delete_submission(session: Session, submission_id: int):
    delete_helper(session, SubmissionDAO, submission_id)


def delete_submissions(session: Session, lei: str = None, period_code: str = None):
    submissions = submission_repo.get_submissions(session, lei, period_code)
    if submissions:
        [delete_submission(session, s.id) for s in submissions]
    else:
        logger.info(f"No submission data to be deleted for LEI {lei}")


def delete_contact_info(session: Session, lei: str = None, period_code: str = None):
    contact_info = get_contact_info(session, lei, period_code)
    if contact_info:
        delete_helper(session, ContactInfoDAO, contact_info.id)
    else:
        logger.info(f"No contact info to be deleted for LEI {lei}")


def delete_helper(session: Session, table_obj: T, table_id: Any):
    session.query(table_obj).filter(table_obj.id == table_id).delete(synchronize_session="fetch")
    session.commit()
