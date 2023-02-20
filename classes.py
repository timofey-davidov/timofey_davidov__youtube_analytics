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
        self.__channel_id = channel_id                                              # уникальный id канала
        self.channel = Channel.youtube.channels().list(id=self.channel_id,
                                      part='snippet,statistics').execute()          # объект с данными канала (сниппеты, статистика)
        self.channel_info = json.dumps(self.channel, indent=2, ensure_ascii=False)  # преобразуем в читаемый формат
        self.title = self.channel["items"][0]["snippet"]["title"]                   # заголовок канала
        self.description = self.channel["items"][0]["snippet"][
            "description"]                                                          # описание канала
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"             # ссылка на канал
        self.subscriberCount = int(self.channel["items"][0]["statistics"][
            "subscriberCount"])                                                     # количество подписчиков
        self.videoCount = int(self.channel["items"][0]["statistics"][
            "videoCount"])                                                          # количество видео на канале
        self.viewCount = int(self.channel["items"][0]["statistics"][
            "viewCount"])                                                           # количество просмотров
    def print_info(self):
        """
        Функция, которая выводит информацию по указанному каналу
        :return: dict
        """
        return self.channel_info

    @property
    def channel_id(self):
        """Метод, возвращающий id канала"""
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Метод, возвращающий объект, содержащий ВСЮ информацию о канале из API"""
        return cls.youtube

    def to_json(self, filename="channel.json"):
        """Метод, записывающий информацию о канале в отдельный файл"""
        data = {"channel": {"id": self.channel_id, "title": self.channel["items"][0]["snippet"]["title"], "description": self.description, "url": self.url, "subscriberCount": self.subscriberCount, "viewCount": self.viewCount, "videoCount": self.videoCount}}
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
