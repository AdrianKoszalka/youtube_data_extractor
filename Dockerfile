FROM python:3.9.4-slim

# Set work directory
WORKDIR /code

# Install psycopg2
RUN apt update -y && apt install -y build-essential libpq-dev
RUN pip install psycopg2-binary --no-binary psycopg2-binary

# Copy and install all dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm ./requirements.txt

# Copy source files
COPY youtube_extraction.py .
COPY youtube_extractor youtube_extractor

ENTRYPOINT ["python", "/code/youtube_extraction.py"]