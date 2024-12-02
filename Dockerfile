FROM --platform=amd64 ghcr.io/cfpb/regtech/sbl/python-ubi8:3.12

ENV UVICORN_LOG_LEVEL=info

WORKDIR /usr/app
RUN pip install poetry

COPY --chown=sbl:sbl poetry.lock pyproject.toml README.md ./

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root

COPY --chown=sbl:sbl ./src ./src

WORKDIR /usr/app/src

EXPOSE 8888

USER sbl

CMD uvicorn regtech_cleanup_api.main:app --host 0.0.0.0 --port 8888 --log-config log-config.yml --log-level $UVICORN_LOG_LEVEL
