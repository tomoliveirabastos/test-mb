FROM python:3.10-alpine3.20

WORKDIR app

COPY . .

RUN apk add curl

RUN pip install -r requirements.txt