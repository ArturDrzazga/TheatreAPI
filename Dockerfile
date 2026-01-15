FROM python:3.12-slim
LABEL maintainer="arturdrzazga.dev@example.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN adduser --disabled-password --no-create-home django-user
USER django-user