FROM python:3.9.4-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm ./requirements.txt

COPY youtube_extraction.py .
COPY youtube_extractor youtube_extractor

RUN apt update -y && apt install -y build-essential libpq-dev
RUN pip install psycopg2-binary --no-binary psycopg2-binary