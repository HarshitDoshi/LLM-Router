FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev file make

RUN pip install --upgrade pip
COPY . .
RUN pip install poetry
RUN python -m poetry install

RUN sed -i 's/\r$//g' /entrypoint.development.sh
RUN chmod +x /entrypoint.development.sh

ENTRYPOINT ["/entrypoint.development.sh"]