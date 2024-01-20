import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_data = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel_data['items'][0]['snippet']['title']
        self.description = self.channel_data['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = self.channel_data['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_data['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_data['items'][0]['statistics']['subscriberCount']
        self.new_data = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subs_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }

    def __str__(self):
        """Возвращает строку с названием и ссылкой на канал."""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Сложение каналов по кол-ву подписчиков."""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Вычитание каналов по кол-ву подписчиков."""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """Сравнение, является ли кол-во подписчиков текущего канала больше, чем у другого."""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Сравнение, является ли кол-во подписчиков текущего канала больше или равно кол-ву у другого."""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        """Сравнение каналов по подписчикам."""
        return int(self.subscriber_count) == int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_channel_id):
        if new_channel_id:
            self.__channel_id = new_channel_id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_name):
        json_data = json.dumps(self.new_data, ensure_ascii=False)

        with open(f"../homework-2/{file_name}", 'w', encoding='windows-1251') as file:
            file.write(json_data)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        print(response)
