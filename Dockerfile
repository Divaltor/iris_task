FROM python:3.10-slim-buster

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:/code:$PATH"

WORKDIR /code

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-dev

COPY . /code