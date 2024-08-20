import shutil
from http import HTTPStatus

import boto3
from regtech_api_commons.api.exceptions import RegTechHttpException

from regtech_cleanup_api.config import filing_settings
from sbl_filing_api.config import FsProtocol


def delete(path: str):
    if filing_settings.fs_upload_config.protocol == FsProtocol.FILE:
        shutil.rmtree(f"{filing_settings.fs_upload_config.root}/{path}")
    else:
        bucket = filing_settings.fs_upload_config.root
        s3 = boto3.resource("s3")
        s3_objects = s3.meta.client.list_objects(Bucket=bucket, Prefix=path)
        if "Contents" in s3_objects:
            object_keys = {
                "Objects": [{"Key": k["Key"]} for k in s3_objects["Contents"]]
            }
            s3.meta.client.delete_objects(Bucket=bucket, Delete=object_keys)
        else:
            raise RegTechHttpException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                name="Content Not Available",
                detail="Associated LEI data is not present for removal",
            )
