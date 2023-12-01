# base image
FROM python:3.10

# enviironment variables
ENV APP_HOME=/etl
ENV GROUP=fastapi
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# enviironment variables
# create app directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN groupadd -r $GROUP && \
    useradd -d $APP_HOME -r -g $GROUP $GROUP && \
    chown $GROUP:$GROUP -R $APP_HOME   

RUN apt-get update && \
    apt-get install -y gettext && \
    apt install -y ncat && \
    python -m pip install --upgrade pip && \
    pip3 install poetry

COPY . $APP_HOME

RUN poetry config virtualenvs.create false
RUN poetry install --without dev

RUN chmod +x ./docker-entrypoint.sh

USER $GROUP


ENTRYPOINT ["./docker-entrypoint.sh"]