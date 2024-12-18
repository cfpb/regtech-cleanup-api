import pytest
import datetime

from sbl_filing_api.entities.models.dao import UserActionDAO, FilingPeriodDAO, FilingDAO, SubmissionDAO, ContactInfoDAO
from sbl_filing_api.entities.models.model_enums import UserActionType, FilingType, SubmissionState
from sqlalchemy.orm import Session, scoped_session

from datetime import datetime as dt
from regtech_cleanup_api.entities.repos import submission_repo as repo


class TestSubmissionRepo:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, transaction_session: Session, session_generator: scoped_session):
        user_action1 = UserActionDAO(
            id=1,
            user_id="test@local.host",
            user_name="signer name",
            user_email="test@local.host",
            action_type=UserActionType.SIGN,
            timestamp=dt.now(),
        )
        user_action2 = UserActionDAO(
            id=2,
            user_id="test@local.host",
            user_name="submitter name",
            user_email="test@local.host",
            action_type=UserActionType.SUBMIT,
            timestamp=dt.now(),
        )
        user_action3 = UserActionDAO(
            id=3,
            user_id="test@local.host",
            user_name="accepter name",
            user_email="test@local.host",
            action_type=UserActionType.ACCEPT,
            timestamp=dt.now(),
        )
        user_action4 = UserActionDAO(
            id=4,
            user_id="test@local.host",
            user_name="creator name",
            user_email="test@local.host",
            action_type=UserActionType.CREATE,
            timestamp=dt.now(),
        )

        transaction_session.add(user_action1)
        transaction_session.add(user_action2)
        transaction_session.add(user_action3)
        transaction_session.add(user_action4)

        filing_period = FilingPeriodDAO(
            code="2024",
            description="Filing Period 2024",
            start_period=dt.now(),
            end_period=dt.now(),
            due=dt.now(),
            filing_type=FilingType.ANNUAL,
        )
        transaction_session.add(filing_period)

        filing1 = FilingDAO(
            id=1,
            lei="1234567890",
            institution_snapshot_id="Snapshot-1",
            filing_period="2024",
        )
        filing2 = FilingDAO(
            id=2,
            lei="ABCDEFGHIJ",
            institution_snapshot_id="Snapshot-1",
            filing_period="2024",
        )
        filing3 = FilingDAO(
            id=3,
            lei="ZYXWVUTSRQP",
            institution_snapshot_id="Snapshot-1",
            filing_period="2024",
        )
        filing1.creator = user_action4
        filing2.creator = user_action4
        filing3.creator = user_action4

        transaction_session.add(filing1)
        transaction_session.add(filing2)
        transaction_session.add(filing3)

        submission1 = SubmissionDAO(
            id=1,
            filing=1,
            submitter_id=2,
            counter=1,
            state=SubmissionState.SUBMISSION_UPLOADED,
            validation_ruleset_version="v1",
            submission_time=dt.now(),
            filename="file1.csv",
        )

        submission2 = SubmissionDAO(
            id=2,
            filing=2,
            submitter_id=2,
            counter=2,
            state=SubmissionState.SUBMISSION_UPLOADED,
            validation_ruleset_version="v1",
            submission_time=(dt.now() - datetime.timedelta(seconds=200)),
            filename="file2.csv",
        )
        submission3 = SubmissionDAO(
            id=3,
            filing=2,
            submitter_id=2,
            counter=3,
            state=SubmissionState.SUBMISSION_UPLOADED,
            validation_ruleset_version="v1",
            submission_time=dt.now(),
            filename="file3.csv",
        )
        submission4 = SubmissionDAO(
            id=4,
            filing=1,
            counter=4,
            state=SubmissionState.SUBMISSION_UPLOADED,
            validation_ruleset_version="v1",
            submission_time=(dt.now() - datetime.timedelta(seconds=400)),
            filename="file4.csv",
        )
        submission1.submitter = user_action2
        submission2.submitter = user_action2
        submission3.submitter = user_action2
        submission4.submitter = user_action2

        transaction_session.add(submission1)
        transaction_session.add(submission2)
        transaction_session.add(submission3)
        transaction_session.add(submission4)

        contact_info1 = ContactInfoDAO(
            id=1,
            filing=1,
            first_name="test_first_name_1",
            last_name="test_last_name_1",
            hq_address_street_1="address street 1",
            hq_address_street_2="",
            hq_address_street_3="",
            hq_address_street_4="",
            hq_address_city="Test City 1",
            hq_address_state="TS",
            hq_address_zip="12345",
            phone_number="112-345-6789",
            email="test1@cfpb.gov",
        )
        contact_info2 = ContactInfoDAO(
            id=2,
            filing=2,
            first_name="test_first_name_2",
            last_name="test_last_name_2",
            hq_address_street_1="address street 2",
            hq_address_street_2="",
            hq_address_street_3="",
            hq_address_street_4="",
            hq_address_city="Test City 2",
            hq_address_state="TS",
            hq_address_zip="12345",
            phone_number="212-345-6789",
            phone_ext="x54321",
            email="test2@cfpb.gov",
        )
        transaction_session.add(contact_info1)
        transaction_session.add(contact_info2)

        transaction_session.commit()

    def test_get_filing(self, query_session: Session):
        res1 = repo.get_filing(query_session, lei="1234567890", filing_period="2024")
        assert res1.id == 1
        assert res1.filing_period == "2024"
        assert res1.lei == "1234567890"

        res2 = repo.get_filing(query_session, lei="ABCDEFGHIJ", filing_period="2024")
        assert res2.id == 2
        assert res2.filing_period == "2024"
        assert res2.lei == "ABCDEFGHIJ"

    def test_get_filings(self, query_session: Session):
        res = repo.get_filings(query_session, lei="1234567890")
        assert res[0].id == 1
        assert res[0].filing_period == "2024"
        assert res[0].lei == "1234567890"

    def test_get_submissions(self, query_session: Session):
        res = repo.get_submissions(query_session)
        assert len(res) == 4
        assert {1, 2, 3, 4} == set([s.id for s in res])
        assert res[1].filing == 2
        assert res[2].state == SubmissionState.SUBMISSION_UPLOADED

        res = repo.get_submissions(query_session, lei="ABCDEFGHIJ", filing_period="2024")
        assert len(res) == 2
        assert {2, 3} == set([s.id for s in res])
        assert {2} == set([s.filing for s in res])
        assert {SubmissionState.SUBMISSION_UPLOADED} == set([s.state for s in res])

        # verify a filing with no submissions behaves ok
        res = repo.get_submissions(query_session, lei="ZYXWVUTSRQP", filing_period="2024")
        assert len(res) == 0
