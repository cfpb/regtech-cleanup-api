from http import HTTPStatus
from regtech_api_commons.api.exceptions import RegTechHttpException

from regtech_cleanup_api.services import file_handler


def delete_from_storage(period_code: str, lei: str) -> None:
    try:
        file_handler.delete(f"upload/{period_code}/{lei}/")
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="File Delete Failure",
            detail=f"Failed to delete file(s) for LEI {lei}",
        ) from e
