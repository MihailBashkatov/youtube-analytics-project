import os

from googleapiclient.discovery import build


class Video:
    """Класс для видеоролика"""

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется по id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id: str = video_id


        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']

        # url ссылка формируется из двух строк
        self.video_url: str = 'https://www.youtube.com/watch?v=' + self.__video_id
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """ Возвращает название видео"""
        return self.video_title

    @property
    def video_id(self):
        return self.__video_id

class PLVideo(Video):
    """Класс для видеороликов в определенном плэйлисте"""
    def __init__(self, video_id, playlist_id):
        self.__video_id = video_id
        self.playlist_id = playlist_id

        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        #получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # Если ID видеоролика есть в списке видероликов плэйлиста, то экземпляр инициализируется. Иначе выводится сообщение, что такого ролика нет
        flag = False
        for video in video_ids:
            if self.__video_id == video:
                super().__init__(self.__video_id)
                flag = True
        if not flag:
            print('No such video')
            quit()