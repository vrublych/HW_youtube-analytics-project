import os
import json
from googleapiclient.discovery import build
import isodate

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        self.channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.refresh_data()

    def refresh_data(self) -> None:
        """Обновляет данные о канале."""
        response = self.youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        channel_data = response.get('items', [])[0]

        self.title = channel_data['snippet']['title']
        self.description = channel_data['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(channel_data['statistics']['subscriberCount'])
        self.video_count = int(channel_data['statistics']['videoCount'])
        self.view_count = int(channel_data['statistics']['viewCount'])

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str) -> None:
        """Сохраняет значения атрибутов экземпляра в файл."""
        data = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))
