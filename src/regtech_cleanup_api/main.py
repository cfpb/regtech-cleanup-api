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

from regtech_cleanup_api.routers.filing_cleanup import router as filing_router
from regtech_cleanup_api.routers.user_fi_cleanup import router as user_fi_router
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


app.include_router(user_fi_router, prefix="/v1/user_fi_cleanup")
app.include_router(filing_router, prefix="/v1/filing_cleanup")
