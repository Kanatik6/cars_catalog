FROM python:3

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .


RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . .
