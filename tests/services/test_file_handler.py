from pytest_mock import MockerFixture
from unittest.mock import Mock
from sbl_filing_api.config import FsProtocol

from regtech_cleanup_api.config import filing_settings
from regtech_cleanup_api.services import file_handler as fh


def test_delete_local_fs(mocker: MockerFixture):
    default_file_proto = filing_settings.fs_upload_config.protocol
    filing_settings.fs_upload_config.protocol = FsProtocol.FILE

    rmtree_mock = mocker.patch("regtech_cleanup_api.services.file_handler.shutil.rmtree")

    path = "test"
    fh.delete(path)
    rmtree_mock.assert_called_with(f"{filing_settings.fs_upload_config.root}/{path}")
    filing_settings.fs_upload_config.protocol = default_file_proto


def test_delete_s3(mocker: MockerFixture):
    default_file_proto = filing_settings.fs_upload_config.protocol
    filing_settings.fs_upload_config.protocol = FsProtocol.S3

    boto3_mock = mocker.patch("regtech_cleanup_api.services.file_handler.boto3")

    resource_mock = Mock()
    objects_mock = Mock()
    objects_mock.return_value = {"Contents": [{"Key": "string"}]}
    delete_mock = Mock()
    boto3_mock.resource.return_value = resource_mock
    resource_mock.meta.client.list_objects = objects_mock
    resource_mock.meta.client.delete_objects = delete_mock

    path = "test"
    bucket = filing_settings.fs_upload_config.root
    fh.delete(path)
    boto3_mock.resource.assert_called_once_with("s3")
    resource_mock.meta.client.list_objects.assert_called_once_with(Bucket=bucket, Prefix=path)
    delete_mock.assert_called_once_with(Bucket="../upload", Delete={"Objects": [{"Key": "string"}]})

    filing_settings.fs_upload_config.protocol = default_file_proto
