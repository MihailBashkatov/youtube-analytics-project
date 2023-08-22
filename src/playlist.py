import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для плейлиста"""

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется по id плейлиста."""
        self.playlist_id: str = playlist_id

        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        playlists = youtube.playlists().list(id='PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw',
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()

        self.title: str = playlists['items'][0]['snippet']['title']
        self.url: str = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def total_duration(self):
        """ Возвращает суммарное время всех роликов плейлиста """
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total_duration = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            total_duration += isodate.parse_duration(iso_8601_duration)
        return total_duration

    def show_best_video(self):
        """ Возвращает видео с макимальным количеством лайков"""
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response: dict = youtube.videos().list(part='contentDetails,statistics',
                                                     id=','.join(video_ids)
                                                     ).execute()

        max_like: int = 0
        video_id: dict = {}

        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like:
                max_like = like_count
                video_id['max_like'] = video['id']
        video_url: str = 'https://youtu.be/' + video_id['max_like']
        return video_url
