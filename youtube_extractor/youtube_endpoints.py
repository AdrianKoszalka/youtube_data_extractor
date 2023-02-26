from .youtube_base import YouTubeExtractorBase


class YouTubeChannels(YouTubeExtractorBase):
    endpoint = "channels"
    table_name = "raw_youtube_channels"
    parent_instance = None
    parent_resource = None
    chunked_data = False
    data_chunk = 0

    def payload(self, data_chunk):
        payload = {
            "part": "snippet,contentDetails,statistics",
            "id": f"{self.channel_id}",
        }

        return payload

    def get_additional_data(self, response):
        # Collect upload playlist ID and store it as channel_upload_playlist_id
        channels = response.json()["items"]

        for channel in channels:
            self.channel_upload_playlist_id.append(
                channel["contentDetails"]["relatedPlaylists"]["uploads"]
            )


class YouTubeChannelVideos(YouTubeExtractorBase):
    endpoint = "playlistItems"
    table_name = None
    parent_instance = YouTubeChannels
    parent_resource = "channel_upload_playlist_id"
    chunked_data = True
    data_chunk = 1

    def payload(self, data_chunk):
        payload = {
            "part": "snippet",
            "playlistId": data_chunk[0],
            "maxResults": 50,
        }

        return payload

    def get_additional_data(self, response):
        # Collect videos IDs and store them in list called channel_video_ids
        videos = response.json()["items"]

        for video in videos:
            self.channel_video_ids.append(video["snippet"]["resourceId"]["videoId"])


class YouTubeVideoDetails(YouTubeExtractorBase):
    endpoint = "videos"
    table_name = "raw_youtube_videos"
    parent_instance = YouTubeChannels
    parent_resource = "channel_video_ids"
    chunked_data = True
    data_chunk = 50

    def payload(self, data_chunk):
        payload = {
            "part": "contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails",
            "id": ",".join(data_chunk),
            "maxResults": 50,
        }

        return payload


class YouTubeVideoComments(YouTubeExtractorBase):
    endpoint = "commentThreads"
    table_name = "raw_youtube_video_comments"
    parent_instance = YouTubeChannels
    parent_resource = "channel_video_ids"
    chunked_data = True
    data_chunk = 1

    def payload(self, data_chunk):
        payload = {
            "part": "snippet,replies",
            "videoId": data_chunk[0],
            "maxResults": 50,
        }

        return payload
