FROM python:3.11-slim
LABEL maintainer="Dmitry Titenkov <lt200711@yandex.ru>"
LABEL version="1.0"
LABEL description="Satire Pulp parser"
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .
