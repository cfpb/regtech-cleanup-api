import pytest
from unittest.mock import Mock, ANY

from fastapi.responses import Response
from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from pytest_mock import MockerFixture
from regtech_api_commons.api.exceptions import RegTechHttpException

from regtech_cleanup_api.routers.institution_cleanup import delete_helper


def test_unauthed_delete_institutions(app_fixture: FastAPI):
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/institution/123456E2ETESTBANK123")
    assert res.status_code == 403


def test_delete_institutions(app_fixture: FastAPI, mocker: MockerFixture, authed_user_mock: Mock):
    delete_helper_mock = mocker.patch("regtech_cleanup_api.routers.institution_cleanup.delete_helper")
    delete_helper_mock.return_value = Response(status_code=status.HTTP_204_NO_CONTENT)
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/institution/123456E2ETESTBANK123")
    delete_helper_mock.assert_called_once_with("123456E2ETESTBANK123", ANY)
    assert res.status_code == 204


def test_institution_delete_helper(app_fixture: FastAPI, mocker: MockerFixture, caplog):
    session_mock = Mock()
    ok_res = {"OK": True}
    delete_domains_mock = mocker.patch("regtech_cleanup_api.routers.institution_cleanup.repo.delete_domains_by_lei")
    delete_domains_mock.return_value = ok_res
    delete_sbl_type_mock = mocker.patch("regtech_cleanup_api.routers.institution_cleanup.repo.delete_sbl_type_by_lei")
    delete_sbl_type_mock.return_value = ok_res
    delete_institution_mock = mocker.patch("regtech_cleanup_api.routers.institution_cleanup.repo.delete_institution")
    delete_institution_mock.return_value = ok_res
    delete_group_mock = mocker.patch("regtech_cleanup_api.routers.institution_cleanup.oauth2_admin.delete_group")
    delete_group_mock.return_value = {"123456E2ETESTBANK123": "test"}

    # No errors test
    delete_helper("123456E2ETESTBANK123", session_mock)
    delete_domains_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123")
    delete_sbl_type_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123")
    delete_institution_mock.assert_called_once_with(ANY, "123456E2ETESTBANK123")
    delete_group_mock.assert_called_once_with("123456E2ETESTBANK123")

    # Delete Domains Fail
    delete_domains_mock.return_value = None
    delete_helper("123456E2ETESTBANK123", session_mock)
    assert "Domain(s) for LEI 123456E2ETESTBANK123 not deleted." in caplog.text

    # Delete SBL Type Fail
    delete_domains_mock.return_value = ok_res
    delete_sbl_type_mock.return_value = None
    delete_helper("123456E2ETESTBANK123", session_mock)
    assert "sbl type(s) for LEI 123456E2ETESTBANK123 not deleted." in caplog.text

    # Delete Institution Fail
    delete_sbl_type_mock.return_value = ok_res
    delete_institution_mock.return_value = None
    with pytest.raises(Exception) as e:
        delete_helper("123456E2ETESTBANK123", session_mock)
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "Institution to be deleted Not Found"

    # Delete Group Fail
    delete_institution_mock.return_value = ok_res
    delete_group_mock.side_effect = IOError("test")
    with pytest.raises(Exception) as e:
        delete_helper("123456E2ETESTBANK123", session_mock)
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "Group Not Found"
