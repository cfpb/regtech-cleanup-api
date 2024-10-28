from unittest.mock import Mock, ANY

from fastapi.testclient import TestClient
from fastapi import FastAPI
from pytest_mock import MockerFixture


def test_unauthed_delete_all_things(app_fixture: FastAPI):
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/123456E2ETESTBANK123")
    assert res.status_code == 403


def test_delete_all_things(app_fixture: FastAPI, mocker: MockerFixture, get_filings_mock: Mock, authed_user_mock: Mock):
    institution_delete_mock = mocker.patch("regtech_cleanup_api.routers.cleanup.institution_delete_helper")
    institution_delete_mock.return_value = None
    filing_delete_mock = mocker.patch(("regtech_cleanup_api.routers.cleanup.filing_delete_helper"))
    filing_delete_mock.return_value = None
    client = TestClient(app_fixture)
    res = client.delete("/v1/cleanup/123456E2ETESTBANK123")
    institution_delete_mock.assert_called_once_with("123456E2ETESTBANK123", ANY)
    filing_delete_mock.assert_called_with("123456E2ETESTBANK123", "2024", ANY)
    assert res.status_code == 204
