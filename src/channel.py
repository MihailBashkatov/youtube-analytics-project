import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id: str = channel_id

        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.url = channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def __repr__(self):
        """ Возвращает название канала и url ссылку"""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """ Возвращает сумму подписчиков двух каналов """
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """ Возвращает разность подписчиков двух каналов """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """ Возвращает True если количество подписчиков первого канала больше, чем у второго """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """ Возвращает True если количество подписчиков первого канала больше или равно, чем у второго """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """ Возвращает True если количество подписчиков первого канала меньше, чем у второго """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """ Возвращает True если количество подписчиков первого канала меньше или равно, чем у второго """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """ Возвращает True если количество подписчиков первого канала равно количеству подписчиков второго канала """
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_name):
        """ Сохраняет в файл значения атрибутов экземпляра `Channel`"""

        dict_attributes = {
                           'channel_id': self.__channel_id,
                           'title': self.title,
                           'url': self.url,
                           'subscriber_count': self.subscriber_count,
                           'video_count': self.video_count,
                           'view_count': self.view_count,
                          }
        with open(file_name, 'w') as outfile:
            json.dump(dict_attributes, outfile, indent=4, ensure_ascii=False)
