###################
# BASE 
###################
FROM python:3.11-slim as base

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

COPY ./package[s] ./packages

RUN poetry install  --no-interaction --no-ansi --no-root

COPY ./app ./app

RUN poetry install --no-interaction --no-ansi

###################
# DEVELOPMENT 
###################
FROM base as development

EXPOSE 8080

CMD exec uvicorn app.server:app --reload --host 0.0.0.0 --port 8080

###################
# PRODUCTION 
###################
FROM base as production

EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080