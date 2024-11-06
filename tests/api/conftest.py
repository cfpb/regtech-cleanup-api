from datetime import datetime

import pytest
from unittest.mock import Mock

from fastapi import FastAPI
from pytest_mock import MockerFixture
from regtech_api_commons.models.auth import AuthenticatedUser
from sbl_filing_api.entities.models.dao import FilingDAO, ContactInfoDAO, UserActionDAO
from sbl_filing_api.entities.models.model_enums import UserActionType
from starlette.authentication import AuthCredentials


@pytest.fixture
def app_fixture() -> FastAPI:
    from regtech_cleanup_api.main import app

    return app


@pytest.fixture
def auth_mock(mocker: MockerFixture) -> Mock:
    return mocker.patch("regtech_api_commons.oauth2.oauth2_backend.BearerTokenAuthBackend.authenticate")


@pytest.fixture
def authed_user_mock(auth_mock: Mock) -> Mock:
    claims = {
        "name": "test",
        "preferred_username": "test_user",
        "email": "test@local.host",
        "sub": "testuser123",
    }
    auth_mock.return_value = (
        AuthCredentials(["manage-account", "query-groups", "manage-users", "authenticated"]),
        AuthenticatedUser.from_claim(claims),
    )
    return auth_mock


@pytest.fixture
def get_filings_mock(mocker: MockerFixture) -> Mock:
    mock = mocker.patch("regtech_cleanup_api.routers.cleanup.submission_repo.get_filings")
    mock.return_value = [
        FilingDAO(
            id=1,
            lei="123456E2ETESTBANK123",
            filing_period="2024",
            institution_snapshot_id="v1",
            contact_info=ContactInfoDAO(
                id=1,
                filing=1,
                first_name="test_first_name_1",
                last_name="test_last_name_1",
                hq_address_street_1="address street 1",
                hq_address_street_2="address street 2",
                hq_address_city="Test City",
                hq_address_state="TS",
                hq_address_zip="12345",
                phone_number="112-345-6789",
                email="test1@cfpb.gov",
            ),
            creator_id=1,
            creator=UserActionDAO(
                id=1,
                user_id="123456-7890-ABCDEF-GHIJ",
                user_name="test submitter",
                user_email="test@local.host",
                action_type=UserActionType.SUBMIT,
                timestamp=datetime.now(),
            ),
        ),
        FilingDAO(
            id=1,
            lei="123456E2ETESTBANK123",
            filing_period="2024",
            institution_snapshot_id="v1",
            contact_info=ContactInfoDAO(
                id=1,
                filing=1,
                first_name="test_first_name_1",
                last_name="test_last_name_1",
                hq_address_street_1="address street 1",
                hq_address_street_2="address street 2",
                hq_address_city="Test City",
                hq_address_state="TS",
                hq_address_zip="12345",
                phone_number="112-345-6789",
                email="test1@cfpb.gov",
            ),
            creator_id=1,
            creator=UserActionDAO(
                id=1,
                user_id="123456-7890-ABCDEF-GHIJ",
                user_name="test submitter",
                user_email="test@local.host",
                action_type=UserActionType.SUBMIT,
                timestamp=datetime.now(),
            ),
        ),
        FilingDAO(
            id=1,
            lei="123456E2ETESTBANK123",
            filing_period="2024",
            institution_snapshot_id="v1",
            contact_info=ContactInfoDAO(
                id=1,
                filing=1,
                first_name="test_first_name_1",
                last_name="test_last_name_1",
                hq_address_street_1="address street 1",
                hq_address_street_2="address street 2",
                hq_address_city="Test City",
                hq_address_state="TS",
                hq_address_zip="12345",
                phone_number="112-345-6789",
                email="test1@cfpb.gov",
            ),
            creator_id=1,
            creator=UserActionDAO(
                id=1,
                user_id="123456-7890-ABCDEF-GHIJ",
                user_name="test submitter",
                user_email="test@local.host",
                action_type=UserActionType.SUBMIT,
                timestamp=datetime.now(),
            ),
        ),
    ]
    return mock
