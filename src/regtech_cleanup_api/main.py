import logging

from fastapi import FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.exceptions import HTTPException

from regtech_api_commons.oauth2.oauth2_backend import BearerTokenAuthBackend
from regtech_api_commons.oauth2.oauth2_admin import OAuth2Admin
from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.exception_handlers import (
    regtech_http_exception_handler,
    request_validation_error_handler,
    http_exception_handler,
    general_exception_handler,
)
import uvicorn

from regtech_cleanup_api.routers.filing_cleanup import router as filing_cleanup
from regtech_cleanup_api.routers.institution_cleanup import router as institution_cleanup
from regtech_cleanup_api.routers.cleanup import router as cleanup_router
from regtech_cleanup_api.config import kc_settings

log = logging.getLogger()

app = FastAPI()


app.add_exception_handler(RegTechHttpException, regtech_http_exception_handler)  # type: ignore[type-arg]  # noqa: E501
app.add_exception_handler(RequestValidationError, request_validation_error_handler)  # type: ignore[type-arg]  # noqa: E501
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[type-arg]  # noqa: E501
app.add_exception_handler(Exception, general_exception_handler)  # type: ignore[type-arg]  # noqa: E501


token_bearer = OAuth2AuthorizationCodeBearer(
    authorizationUrl=kc_settings.auth_url.unicode_string(),
    tokenUrl=kc_settings.token_url.unicode_string(),
)

app.add_middleware(
    AuthenticationMiddleware,
    backend=BearerTokenAuthBackend(token_bearer, OAuth2Admin(kc_settings)),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cleanup_router, prefix="/v1/cleanup")
app.include_router(filing_cleanup, prefix="/v1/cleanup/filing")
app.include_router(institution_cleanup, prefix="/v1/cleanup/institution")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888)
