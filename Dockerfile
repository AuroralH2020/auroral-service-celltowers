FROM python:3.10.10-slim as base

# Install linux libraries
RUN apt update && apt install -y libpq-dev python3-dev build-essential

# create workdir
RUN mkdir /app
WORKDIR /app

# install dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy sources
COPY app/ ./app

# copy .env from host
COPY .env ./.env

EXPOSE 8080
STOPSIGNAL SIGQUIT

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]