import json
from unittest.mock import Mock, ANY

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from pytest_mock import MockerFixture
from regtech_api_commons.api.exceptions import RegTechHttpException

from regtech_cleanup_api.routers.filing_cleanup import delete_helper


def test_unauthed_delete_filing(app_fixture: FastAPI):
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/filing/123456E2ETESTBANK123/2024")
    assert res.status_code == 403


def test_delete_filing(app_fixture: FastAPI, mocker: MockerFixture, authed_user_mock: Mock):
    delete_helper_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.delete_helper")
    delete_helper_mock.return_value = None
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/filing/123456E2ETESTBANK123/2024")
    delete_helper_mock.assert_called_with("123456E2ETESTBANK123", "2024", ANY)
    assert res.status_code == 204

    # Test with errors
    delete_helper_mock.side_effect = IOError("Test")
    res = client.delete("/v1/cleanup/filing/123456E2ETESTBANK123/2024")
    res_text = json.loads(res.text)
    assert res.status_code == 500
    assert res_text["error_name"] == "Delete Filing Server Error"
    assert res_text["error_detail"] == "Server error while trying to delete filing for LEI 123456E2ETESTBANK123."


def test_filing_delete_helper(app_fixture: FastAPI, mocker: MockerFixture):
    session_mock = Mock()
    delete_contact_info_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.delete_contact_info")
    delete_contact_info_mock.return_value = None
    user_action_ids_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.get_user_action_ids")
    user_action_ids_mock.return_value = ["1", "2"]
    delete_submissions_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.delete_submissions")
    delete_submissions_mock.return_value = None
    delete_filing_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.delete_filing")
    delete_filing_mock.return_value = None
    delete_user_actions_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.delete_user_actions")
    delete_user_actions_mock.return_value = None
    delete_from_storage_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.delete_from_storage")
    delete_from_storage_mock.return_value = None

    # No errors test
    delete_helper("123456E2ETESTBANK123", "2024", session_mock)
    delete_contact_info_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123", "2024")
    user_action_ids_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123", "2024")
    delete_submissions_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123", "2024")
    delete_filing_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123", "2024")
    delete_user_actions_mock.assert_called_once_with(ANY, ["1", "2"])
    delete_from_storage_mock.assert_called_once_with("2024", "123456E2ETESTBANK123")

    test_error = IOError("Test")

    # Delete Contact Info Fail Test
    delete_contact_info_mock.side_effect = test_error
    with pytest.raises(Exception) as e:
        delete_helper("123456E2ETESTBANK123", "2024", session_mock)
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "Contact Info Delete Failed"
    assert e.value.detail == "Failed to delete contact info for LEI 123456E2ETESTBANK123"

    # Get User Action IDs Fail
    delete_contact_info_mock.side_effect = None
    user_action_ids_mock.side_effect = test_error
    with pytest.raises(Exception) as e:
        delete_helper("123456E2ETESTBANK123", "2024", session_mock)
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "Missing User Action Data"
    assert e.value.detail == "Failed to get user action data for LEI 123456E2ETESTBANK123"

    # Delete Submissions Fail
    user_action_ids_mock.side_effect = None
    delete_submissions_mock.side_effect = test_error
    with pytest.raises(Exception) as e:
        delete_helper("123456E2ETESTBANK123", "2024", session_mock)
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "Submission Delete Failed"
    assert e.value.detail == "Failed to delete submission data for LEI 123456E2ETESTBANK123"

    # Delete Filing Fail
    delete_submissions_mock.side_effect = None
    delete_filing_mock.side_effect = test_error
    with pytest.raises(Exception) as e:
        delete_helper("123456E2ETESTBANK123", "2024", session_mock)
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "Filing Delete Failed"
    assert e.value.detail == "Failed to delete filing data for LEI 123456E2ETESTBANK123"

    # Delete User Actions Fail
    delete_filing_mock.side_effect = None
    delete_user_actions_mock.side_effect = test_error
    with pytest.raises(Exception) as e:
        delete_helper("123456E2ETESTBANK123", "2024", session_mock)
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "User Action Delete Failed"
    assert e.value.detail == "Failed to delete user action data for LEI 123456E2ETESTBANK123"


def test_unauthed_delete_submissions(app_fixture: FastAPI):
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/filing/submissions/123456E2ETESTBANK123/2024")
    assert res.status_code == 403


def test_delete_submissions(app_fixture: FastAPI, mocker: MockerFixture, authed_user_mock: Mock):
    user_action_ids_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.get_user_action_ids")
    user_action_ids_mock.return_value = ["1", "2"]
    delete_submissions_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.delete_submissions")
    delete_submissions_mock.return_value = None
    delete_user_actions_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.repo.delete_user_actions")
    delete_user_actions_mock.return_value = None
    delete_from_storage_mock = mocker.patch("regtech_cleanup_api.routers.filing_cleanup.delete_from_storage")
    delete_from_storage_mock.return_value = None
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/filing/submissions/123456E2ETESTBANK123/2024")

    # No Errors Test
    user_action_ids_mock.assert_called_with(ANY, lei="123456E2ETESTBANK123", period_code="2024", just_submissions=True)
    delete_submissions_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123", "2024")
    delete_user_actions_mock.assert_called_once_with(ANY, ["1", "2"])
    delete_from_storage_mock.assert_called_once_with("2024", "123456E2ETESTBANK123")
    assert res.status_code == 204

    test_error = IOError("Test")

    # Get User Action IDs fail
    user_action_ids_mock.side_effect = test_error
    res = client.delete("/v1/cleanup/filing/submissions/123456E2ETESTBANK123/2024")
    res_text = json.loads(res.text)
    assert res.status_code == 500
    assert res_text["error_name"] == "Missing User Action Data"
    assert res_text["error_detail"] == "Failed to get user action data for LEI 123456E2ETESTBANK123"

    # Delete Submissions Fail
    user_action_ids_mock.side_effect = None
    delete_submissions_mock.side_effect = test_error
    res = client.delete("/v1/cleanup/filing/submissions/123456E2ETESTBANK123/2024")
    res_text = json.loads(res.text)
    assert res.status_code == 500
    assert res_text["error_name"] == "Submission Delete Failed"
    assert res_text["error_detail"] == "Failed to delete submission data for LEI 123456E2ETESTBANK123"

    # Delete User Actions Fail
    delete_submissions_mock.side_effect = None
    delete_user_actions_mock.side_effect = test_error
    res = client.delete("/v1/cleanup/filing/submissions/123456E2ETESTBANK123/2024")
    res_text = json.loads(res.text)
    assert res.status_code == 500
    assert res_text["error_name"] == "User Action Delete Failed"
    assert res_text["error_detail"] == "Failed to delete user action data for LEI 123456E2ETESTBANK123"
