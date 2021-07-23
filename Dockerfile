FROM python:3.8.11-alpine3.13
MAINTAINER aaraujo@protonmail.ch
ENV PATH="/root/.cargo/bin:${PATH}"

RUN apk add --update --no-cache gcc musl-dev libffi-dev openssl-dev mariadb-client rust cargo

COPY . .
RUN python -m pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec python backup.py
