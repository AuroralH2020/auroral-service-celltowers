# CREATE PYTHON VIRTUAL ENV
FROM --platform=$BUILDPLATFORM python:3.10.10-slim as base

# create workdir for python virual env
RUN mkdir /cell_towers_coverage
WORKDIR /cell_towers_coverage

# install dependencies
RUN apt update && apt install -y libpq-dev python3-dev
RUN python -m venv env
COPY ./requirements.txt ./
RUN ./env/bin/pip install --no-cache-dir -r requirements.txt


# DEPLOY PHASE
FROM python:3.10.10-slim

WORKDIR /cell_towers_coverage

# copy virtual env from base
COPY --from=base /cell_towers_coverage/env ./env
COPY ./app/ ./app/

# copy .env from host
COPY ./.env ./.env

# LABEL
LABEL maintaner="jorge.almela@bavenir.eu"
ENTRYPOINT ["bash"]
# ENTRYPOINT ["./env/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080"]
# START
EXPOSE 8080
STOPSIGNAL SIGQUIT
USER $UID