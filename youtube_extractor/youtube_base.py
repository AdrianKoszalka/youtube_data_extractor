import os
from abc import ABC
from urllib.parse import urljoin, quote_plus

import requests
from sqlalchemy import Table, Column, MetaData, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from .youtube_meta import MetaYouTubeExtractor


class YouTubeExtractorBase(MetaYouTubeExtractor, ABC):
    _instance = None
    channel_video_ids = list()
    channel_upload_playlist_id = list()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(YouTubeExtractorBase, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key, channel_id, schema):
        self.get_base_url: str = f"https://youtube.googleapis.com/youtube/v3/"
        self.api_key = api_key
        self.channel_id = channel_id

        self.engine = None
        self.connection = None

        self.schema = schema

        if self.table_name:
            self.table = Table(
                self.table_name,
                MetaData(schema=schema),
                Column("raw_data", JSONB),
                Column("arguments", JSONB),
            )

    def __enter__(self):
        self.create_engine()

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

        self.session = None
        self.connection = None
        self.session = None

        print(f"\t- Successfully extracted data for: {type(self).__name__}")

    @staticmethod
    def split_data_into_chunks(data_list, chunk_size):
        for data_chunk in range(0, len(data_list), chunk_size):
            yield data_list[data_chunk : data_chunk + chunk_size]

    def create_engine(self):
        if all(
            [
                db_user := os.getenv("POSTGRES_USER"),
                db_password := quote_plus(os.getenv("POSTGRES_PASSWORD")),
                db_host := os.getenv("POSTGRES_HOST"),
                db_port := os.getenv("POSTGRES_PORT"),
                db_name := os.getenv("POSTGRES_DB"),
            ]
        ):
            connection_string = (
                f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )
        else:
            raise Exception

        self.engine = create_engine(connection_string)
        self.connection = self.engine.connect()

    def get_additional_data(self, response):
        pass

    def extract_data(self):
        print(f"\nExtraction started for {type(self).__name__}:")
        url = urljoin(self.get_base_url, self.endpoint)
        data_chunks = ["no_chunks"]

        if self.parent_instance:
            parent_instance = self.parent_instance(
                self.api_key, self.channel_id, self.schema
            )
            print(
                f"\t- Successfully created a parent instance for parent class: {self.parent_instance.__name__}"
            )
            parent_resource = getattr(parent_instance, self.parent_resource)

            if self.chunked_data:
                data_chunks = list(
                    self.split_data_into_chunks(parent_resource, self.data_chunk)
                )

        for index, data_chunk in enumerate(data_chunks):
            payload = self.payload(data_chunk)
            payload["key"] = self.api_key

            page = 1
            next_page = True

            while next_page:
                response = self.session.get(url, params=payload)
                self.get_additional_data(response)

                if "nextPageToken" in response.json().keys():
                    payload["pageToken"] = response.json()["nextPageToken"]
                    page += 1
                else:
                    next_page = False

                if response.status_code == 200:
                    if self.table_name:
                        self.load_to_db(response.json())
                else:
                    print(
                        f"\n\t*There was a problem with getting data from API. Response code: {response.status_code}"
                    )
                    print(f"\t*URL of failed request: {url}")
                    print(f"\t*Payload of failed request: {payload}\n")

    def load_to_db(self, data):
        self.connection.execute(
            self.table.insert(),
            {"raw_data": data, "arguments": {"project": self.schema}},
        )
