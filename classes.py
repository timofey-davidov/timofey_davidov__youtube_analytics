import os, json
from googleapiclient.discovery import build

# API-ключ для работы с YouTube: YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv("YT_API_KEY")

# создаем специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """
    Класс для работы с каналами сервиса Youtube.
    """

    def __init__(self, channel_id: str):
        # уникальный id канала
        self.__channel_id = channel_id

        # объект с данными канала (сниппеты, статистика)
        self.channel = youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics').execute()

        # преобразуем в читаемый формат
        self.channel_info = json.dumps(self.channel, indent=2, ensure_ascii=False)

        # заголовок канала
        self.title = self.channel["items"][0]["snippet"]["title"]

        # описание канала
        self.description = \
            self.channel["items"][0]["snippet"]["description"]

        # url-ссылка
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"  # ссылка на канал

        # количество подписчиков
        self.subscriberCount = int(
            self.channel["items"][0]["statistics"][
                "subscriberCount"])

        # количество видео на канале
        self.videoCount = int(
            self.channel["items"][0]["statistics"][
                "videoCount"])

        # количество просмотров
        self.viewCount = int(
            self.channel["items"][0]["statistics"][
                "viewCount"])

    def __str__(self):
        """Строковое описание канала"""
        return f"Youtube-канал: {self.title}"

    def __lt__(self, other):
        """Сравнение на <"""
        if isinstance(other, Channel) and self.subscriberCount < other.subscriberCount:
            return True
        return False

    def __gt__(self, other):
        """Сравнение на >"""
        if isinstance(other, Channel) and self.subscriberCount > other.subscriberCount:
            return True
        return False

    def __le__(self, other):
        """Сравнение на <="""
        if isinstance(other, Channel) and self.subscriberCount <= other.subscriberCount:
            return True
        return False

    def __ge__(self, other):
        """Сравнение на >="""
        if isinstance(other, Channel) and self.subscriberCount >= other.subscriberCount:
            return True
        return False

    def __add__(self, other):
        """Сложение подписчиков каналов (исходный канал – ЛЕВЫЙ ОПЕРАНД)"""
        if isinstance(other, Channel):
            return other.subscriberCount + self.subscriberCount

    def __radd__(self, other):
        """Сложение подписчиков каналов (исходный канал – ПРАВЫЙ ОПЕРАНД)"""
        return self.__add__(other)

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
        return youtube

    def to_json(self, filename="channel.json"):
        """Метод, записывающий информацию о канале в отдельный файл"""
        data = {"channel": {"id": self.channel_id, "title":
            self.channel["items"][0]["snippet"]["title"],
                            "description": self.description,
                            "url": self.url,
                            "subscriberCount": self.subscriberCount,
                            "viewCount": self.viewCount,
                            "videoCount": self.videoCount}}
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=2,
                      ensure_ascii=False)


class Video:
    """
    Класс для работы с видео сервиса Youtube.
    """

    # API-ключ для работы с YouTube: YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv("YT_API_KEY")

    # создаем специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str, playlist_id: str = None):
        # формируем id видео
        self._video_id = video_id

        # объект для работы с данными видео (сниппеты, статистика)
        self.video_response = youtube.videos().list(part='snippet,statistics', id=self._video_id).execute()

        # преобразуем в читаемый формат
        self.video_info = json.dumps(self.video_response, indent=2, ensure_ascii=False)

        # заголовок видео
        self.video_title = self.video_response["items"][0]["snippet"]["title"]

        # количество просмотров видео
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']

        # количество лайков под видео
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

        # количество комментариев под видео
        self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.video_title
class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str = None):

        super().__init__(video_id)

        # формируем id плейлиста
        self._playlist_id = playlist_id

        if self._playlist_id is not None:

            # объект для работы с данными плейлиста (сниппеты, статистика)
            self.playlist_response = youtube.playlists().list(id=self._playlist_id, part='snippet', maxResults=50).execute()

            # преобразуем в читаемый формат
            self.playlist_info = json.dumps(self.playlist_response, indent=2, ensure_ascii=False)

            # заголовок плейлиста
            self.playlist_title = self.playlist_response["items"][0]["snippet"]["title"]

    def __str__(self):
        return f"{self.video_title} ({self.playlist_title})"


if __name__ == '__main__':
    video1 = Video('9lO06Zxhu88')
    video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    print(video1)
    print(video2)
