FROM python:3.8.3-alpine
MAINTAINER aaraujo@protonmail.ch

RUN apk add --update --no-cache gcc musl-dev libffi-dev openssl-dev mariadb-client

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD exec python backup.py
