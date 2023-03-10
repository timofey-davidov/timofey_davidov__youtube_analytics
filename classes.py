import os, json, isodate, datetime
from googleapiclient.discovery import build

class MixinYoutube:
    """
    Класс-миксин, возвращающий объект для работы с сервисом youtube
    """
    # API-ключ для работы с YouTube: YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv("YT_API_KEY")

    # создаем специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)
    def get_service(self):
        """Метод, возвращающий объект, содержащий ВСЮ информацию о канале из API"""
        cls = type(self)
        return cls.youtube



class Channel(MixinYoutube):
    """
    Класс для работы с каналами сервиса Youtube.
    """

    def __init__(self, channel_id: str):
        # уникальный id канала
        self.__channel_id = channel_id

        # объект с данными канала (сниппеты, статистика)
        self.channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()

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


class Video(MixinYoutube):
    """
    Класс для работы с видео сервиса Youtube.
    """

    def __init__(self, video_id: str, playlist_id: str = None):
        # формируем id видео
        self._video_id = video_id

        # объект для работы с данными видео (сниппеты, статистика)
        self.video_response = self.get_service().videos().list(part='snippet,statistics', id=self._video_id).execute()

        # преобразуем в читаемый формат
        self.video_info = json.dumps(self.video_response, indent=2, ensure_ascii=False)

        # заголовок видео
        self.video_title = self.video_response["items"][0]["snippet"]["title"]

        # количество просмотров видео
        self.video_view_count: int = self.video_response['items'][0]['statistics']['viewCount']

        # количество лайков под видео
        self.video_like_count: int = self.video_response['items'][0]['statistics']['likeCount']

        # количество комментариев под видео
        self.video_comment_count: int = self.video_response['items'][0]['statistics']['commentCount']

        # ссылка на видео
        self.video_link: str = f"https://youtu.be/{self._video_id}"
        
        if playlist_id is not None:
            super().__init__(playlist_id)

    def __str__(self):
        return self.video_title


class PlayList(MixinYoutube):
    def __init__(self, playlist_id: str = None):
        if playlist_id is not None:
            self._playlist_id = playlist_id
            # объект для работы с данными плейлиста (сниппеты, статистика)
            self.playlist_response = self.get_service().playlists().list(id=self._playlist_id, part='snippet',
                                                              maxResults=50).execute()

            # преобразуем в читаемый формат
            self.playlist_info = json.dumps(self.playlist_response, indent=2, ensure_ascii=False)

            # заголовок плейлиста
            self.playlist_title = self.playlist_response["items"][0]["snippet"]["title"]

            # url-ссылка
            self.url = f"https://www.youtube.com/playlist?list={self._playlist_id}"  # ссылка на плейлист
    @property
    def title(self):
        return self.playlist_title
    @property
    def get_videos_id(self):
        """
        Функция для получения id видео в данном плейлисте
        :return: list
        """
        # объект для работы с данными видео плейлиста (контент)
        playlist_videos = self.get_service().playlistItems().list(playlistId=self._playlist_id, part='contentDetails', maxResults=50).execute()
        # преобразуем в читаемый формат
        self.playlist_videos = json.dumps(self.playlist_response, indent=2, ensure_ascii=False)
        # получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def get_videos_duration(self):
        """
        Функция для получения продолэительности видео в плейлисте
        :return:
        """
        # объект для работы с данными видео плейлиста (контент с длительностью)
        video_response = self.get_service().videos().list(part='contentDetails,statistics', id=','.join(self.get_videos_id)).execute()

        # суммарная длительность видео
        duration = datetime.timedelta(0)

        # перебор видео и подсчет суммарной длительности
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        videos_list = [Video(id) for id in self.get_videos_id]
        return max(videos_list, key=lambda item: item.video_like_count).video_link

class PLVideo(Video, PlayList):
    def __init__(self, video_id: str, playlist_id: str = None):
        super().__init__(video_id, playlist_id)

    def __str__(self):
        return f"{self.video_title} ({self.playlist_title})"


if __name__ == '__main__':
    video1 = Video('9lO06Zxhu88')
    video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    print(video1)
    print(video2)
    pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    print(pl.title)
    print(pl.url)
    print(pl.get_videos_duration)
    print(type(pl.get_videos_duration))
    print(pl.get_videos_duration.total_seconds())
    print(pl.show_best_video())
    item_1 = Channel("UCMCgOm8GZkHp8zJ6l7_hIuA")
    item_2 = Channel("UC1eFXmJNkjITxPFWTy6RsWg")
    print(item_1)
