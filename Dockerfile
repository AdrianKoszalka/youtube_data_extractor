FROM python:3.9.4-slim

# Provide all necessary env variables
ARG POSTGRES_HOST
ENV POSTGRES_HOST=$POSTGRES_HOST
ARG POSTGRES_DB
ENV POSTGRES_DB=$POSTGRES_DB
ARG POSTGRES_USER
ENV POSTGRES_USER=$POSTGRES_USER
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ARG POSTGRES_PORT
ENV POSTGRES_PORT=$POSTGRES_PORT
ARG GOOGLE_CLOUD_API_KEY
ENV GOOGLE_CLOUD_API_KEY=$GOOGLE_CLOUD_API_KEY

# Set work directory
WORKDIR /code

# Copy and install all dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm ./requirements.txt

# Copy source files
COPY youtube_extraction.py .
COPY youtube_extractor youtube_extractor

ENTRYPOINT ["python", "/code/youtube_extraction.py"]

# optional
# RUN apt update -y && apt install -y build-essential libpq-dev
# RUN pip install psycopg2-binary --no-binary psycopg2-binary