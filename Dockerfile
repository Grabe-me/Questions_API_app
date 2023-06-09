FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
