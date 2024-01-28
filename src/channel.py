import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_data = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel_data['items'][0]['snippet']['title']
        self.description = self.channel_data['items'][0]['snippet']['description']
        self.url = f"https://www.youtube/channels/{self.__channel_id}"
        self.subscriber_count = int(self.channel_data['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel_data['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel_data['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f"{self.title}({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel_id = 'UCwHL6WHUarjGfUM_586me8w'
        dict_to_print = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_channel_id):
        if new_channel_id:
            print("AttributeError: property 'channel_id' of 'Channel' object has no setter")
            self.__channel_id = self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_json):
        new_data = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'views_count': self.view_count,
        }

        json_data = json.dumps(new_data, ensure_ascii=False)

        with open(file_json, 'w', encoding='windows-1251') as file:
            file.write(json_data)
