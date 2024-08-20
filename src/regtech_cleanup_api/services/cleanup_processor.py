from http import HTTPStatus
from regtech_api_commons.api.exceptions import RegTechHttpException

from regtech_cleanup_api.services import file_handler
from regtech_cleanup_api.services.validation import is_valid_cleanup_lei


def delete_from_storage(period_code: str, lei: str) -> None:
    try:
        file_handler.delete(f"upload/{period_code}/{lei}/")
    except Exception as e:
        raise RegTechHttpException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            name="Delete Failure",
            detail="Failed to delete file",
        ) from e
