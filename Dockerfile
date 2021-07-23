FROM python:3.8.11-alpine3.13
MAINTAINER aaraujo@protonmail.ch

RUN apk add --update --no-cache gcc musl-dev libffi-dev openssl-dev mariadb-client curl
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

COPY . .
RUN python -m pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec python backup.py
