import logging
from typing import List, TypeVar
from copy import deepcopy
from sbl_filing_api.entities.models.dao import (
    FilingDAO,
    FilingTaskProgressDAO,
    FilingTaskDAO,
    SubmissionDAO,
)
from sbl_filing_api.entities.models.model_enums import FilingTaskState
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

T = TypeVar("T")


def get_filing(session: Session, lei: str, filing_period: str) -> FilingDAO:
    result = query_helper(session, FilingDAO, lei=lei, filing_period=filing_period)
    if result:
        result = populate_missing_tasks(session, result)
    return result[0] if result else None


def query_helper(session: Session, table_obj: T, **filter_args) -> List[T]:
    # remove empty args
    filter_args = {k: v for k, v in filter_args.items() if v is not None}
    if filter_args:
        return session.query(table_obj).filter_by(**filter_args).all()
    return session.query(table_obj).all()


def populate_missing_tasks(session: Session, filings: List[FilingDAO]):
    filing_tasks = get_filing_tasks(session)
    filings_copy = deepcopy(filings)
    for f in filings_copy:
        tasks = [t.task.name for t in f.tasks]
        missing_tasks = [t for t in filing_tasks if t.name not in tasks]
        for mt in missing_tasks:
            f.tasks.append(
                FilingTaskProgressDAO(
                    filing=f.id,
                    task_name=mt.name,
                    task=mt,
                    state=FilingTaskState.NOT_STARTED,
                    user="",
                )
            )

    return filings_copy


def get_filing_tasks(session: Session) -> List[FilingTaskDAO]:
    return query_helper(session, FilingTaskDAO)


def get_submissions(
    session: Session, lei: str = None, filing_period: str = None
) -> List[SubmissionDAO]:
    filing_id = None
    if lei and filing_period:
        filing = get_filing(session, lei=lei, filing_period=filing_period)
        filing_id = filing.id
    return query_helper(session, SubmissionDAO, filing=filing_id)
