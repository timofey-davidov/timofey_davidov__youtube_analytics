import os, json
from googleapiclient.discovery import build
class Channel:
    """
    Класс для работы с каналами сервиса Youtube.
    """

    # API-ключ для работы с YouTube: YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv("YT_API_KEY")

    # создаем специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.channel_id,
                                      part='snippet,statistics').execute()
    def print_info(self):
        """
        Функция, которая выводит информацию по указанному каналу
        :return: dict
        """
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
