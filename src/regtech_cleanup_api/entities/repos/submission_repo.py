import logging
from typing import List, TypeVar
from sbl_filing_api.entities.models.dao import (
    FilingDAO,
    SubmissionDAO,
)
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

T = TypeVar("T")


def get_filings(session: Session, lei: str) -> List[FilingDAO]:
    return query_helper(session, FilingDAO, lei=lei)


def get_filing(session: Session, lei: str, filing_period: str) -> FilingDAO:
    result = query_helper(session, FilingDAO, lei=lei, filing_period=filing_period)
    return result[0] if result else None


def query_helper(session: Session, table_obj: T, **filter_args) -> List[T]:
    # remove empty args
    filter_args = {k: v for k, v in filter_args.items() if v is not None}
    if filter_args:
        return session.query(table_obj).filter_by(**filter_args).all()
    return session.query(table_obj).all()


def get_submissions(session: Session, lei: str = None, filing_period: str = None) -> List[SubmissionDAO]:
    filing_id = None
    if lei and filing_period:
        filing = get_filing(session, lei=lei, filing_period=filing_period)
        filing_id = filing.id
    return query_helper(session, SubmissionDAO, filing=filing_id)
