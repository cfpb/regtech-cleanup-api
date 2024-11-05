import pytest
from pytest_mock import MockerFixture
from regtech_api_commons.api.exceptions import RegTechHttpException

from regtech_cleanup_api.services import cleanup_processor


def test_delete(mocker: MockerFixture):
    delete_mock = mocker.patch("regtech_cleanup_api.services.file_handler.delete")
    cleanup_processor.delete_from_storage("test_period", "test")
    delete_mock.assert_called_once_with("upload/test_period/test/")


def test_delete_failure(mocker: MockerFixture):
    delete_mock = mocker.patch("regtech_cleanup_api.services.file_handler.delete")
    delete_mock.side_effect = IOError("test")
    with pytest.raises(Exception) as e:
        cleanup_processor.delete_from_storage("test_period", "test")
    assert isinstance(e.value, RegTechHttpException)
    assert e.value.name == "File Delete Failure"
