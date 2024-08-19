from pytest_mock import MockerFixture

from regtech_cleanup_api.services import cleanup_processor


def test_upload(mocker: MockerFixture):
    delete_mock = mocker.patch("regtech_cleanup_api.services.file_handler.delete")
    cleanup_processor.delete_from_storage("test_period", "test")
    delete_mock.assert_called_once_with(path="upload/{period_code}/{lei}/")
