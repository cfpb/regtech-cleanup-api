import pytest
import datetime
from sbl_filing_api.entities.models.dao import UserActionDAO, FilingPeriodDAO, FilingDAO, SubmissionDAO, ContactInfoDAO
from sbl_filing_api.entities.models.model_enums import UserActionType, FilingType, SubmissionState
from regtech_cleanup_api.entities.repos import filing_repo as repo
from regtech_cleanup_api.entities.repos import submission_repo as sub_repo
from sqlalchemy.orm import Session, scoped_session
from datetime import datetime as dt


class TestFilingRepo:
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

    def test_get_user_action_ids(self, query_session: Session):
        res = repo.get_user_action_ids(query_session, "1234567890", "2024")

        assert len(res) == 2
        assert res[0] == 2
        assert res[1] == 4

    def test_get_contact_info(self, query_session: Session):
        res = sub_repo.get_filing(session=query_session, lei="ABCDEFGHIJ", filing_period="2024")

        assert res.contact_info.id == 2
        assert res.contact_info.filing == 2
        assert res.contact_info.first_name == "test_first_name_2"
        assert res.contact_info.last_name == "test_last_name_2"
        assert res.contact_info.hq_address_street_1 == "address street 2"
        assert res.contact_info.hq_address_street_2 == ""
        assert res.contact_info.hq_address_street_3 == ""
        assert res.contact_info.hq_address_street_4 == ""
        assert res.contact_info.hq_address_city == "Test City 2"
        assert res.contact_info.hq_address_state == "TS"
        assert res.contact_info.hq_address_zip == "12345"
        assert res.contact_info.phone_number == "212-345-6789"
        assert res.contact_info.phone_ext == "x54321"
        assert res.contact_info.email == "test2@cfpb.gov"

    def test_delete_user_action(self, transaction_session: Session, query_session: Session):
        repo.delete_user_action(transaction_session, 4)
        res = query_session.query(UserActionDAO).all()
        res_ids = [i.id for i in res]
        assert 1 in res_ids
        assert 2 in res_ids
        assert 3 in res_ids
        assert 4 not in res_ids

    def test_delete_user_actions(self, transaction_session: Session, query_session: Session):
        repo.delete_user_actions(transaction_session, [2, 4])
        res = query_session.query(UserActionDAO).all()
        res_ids = [i.id for i in res]
        assert 1 in res_ids
        assert 3 in res_ids
        assert 2 not in res_ids
        assert 4 not in res_ids

    def test_delete_filing(self, transaction_session: Session, query_session: Session):
        repo.delete_filing(transaction_session, "1234567890", "2024")
        res = query_session.query(FilingDAO).all()
        res_leis = [fd.lei for fd in res]
        assert "1234567890" not in res_leis
        assert "ABCDEFGHIJ" in res_leis
        assert "ZYXWVUTSRQP" in res_leis

    def test_delete_submission(self, transaction_session: Session, query_session: Session):
        repo.delete_submissions(transaction_session, "1234567890", "2024")
        res = query_session.query(SubmissionDAO).all()
        res_sub_ids = [s.submitter_id for s in res]
        assert 1 not in res_sub_ids
        assert 2 in res_sub_ids
        assert 3 not in res_sub_ids
        assert 4 not in res_sub_ids

    def test_delete_submissions(self, transaction_session: Session, query_session: Session):
        repo.delete_submissions(transaction_session, "1234567890", "2024")
        res = query_session.query(SubmissionDAO).all()
        res_sub_ids = [s.submitter_id for s in res]
        assert 1 not in res_sub_ids
        assert 2 in res_sub_ids
        assert 3 not in res_sub_ids
        assert 4 not in res_sub_ids

    def test_delete_contact_info(self, transaction_session: Session, query_session: Session):
        repo.delete_contact_info(transaction_session, "1234567890", "2024")
        res = query_session.query(ContactInfoDAO).all()
        res_names = [n.first_name for n in res]
        assert "test_first_name_1" not in res_names
        assert "test_first_name_2" in res_names
