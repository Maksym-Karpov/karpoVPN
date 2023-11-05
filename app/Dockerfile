FROM python:3.11.4-alpine


ENV APP_HOME=/code/app/web
RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/code/app/web/entrypoint.sh"]
