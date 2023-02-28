import argparse
import os

from youtube_extractor.youtube_endpoints import (
    YouTubeChannels,
    YouTubeChannelVideos,
    YouTubeVideoDetails,
    YouTubeVideoComments,
)


def extract_youtube_data(api_key, channel_id, schema):
    extractors = (
        YouTubeChannels,
        YouTubeChannelVideos,
        YouTubeVideoDetails,
        YouTubeVideoComments,
    )

    for extractor in extractors:
        with extractor(api_key, channel_id, schema) as ext:
            ext.extract_data()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel-id", type=str)

    args = parser.parse_args()

    schema = 'youtube_data'
    channel_id = args.channel_id
    api_key = os.getenv("GOOGLE_CLOUD_API_KEY")

    extract_youtube_data(api_key, channel_id, schema)
