FROM python:3.12.1-alpine

RUN adduser -D railwayjaguar

RUN apk add musl-dev gcc librdkafka librdkafka-dev

COPY . /app
WORKDIR /app
RUN chown -R railwayjaguar:root /app
RUN pip3 install -r requirements.txt


USER railwayjaguar
CMD [ "python3", "main.py", "worker" ]
