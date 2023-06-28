FROM python:3.10.2-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY templates/ templates/
COPY db/ db/
COPY app.py .
COPY wsgi.py .
COPY pyproject.toml .
COPY poetry.lock .
COPY .env .

RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    gcc

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD [ "gunicorn", "--bind", "0.0.0.0:3000", "wsgi:flask_app" ]
