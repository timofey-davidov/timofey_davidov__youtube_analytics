import pytest
from classes import Channel, Video, PLVideo, PlayList


@pytest.fixture
def item1():
    return Channel("UCMCgOm8GZkHp8zJ6l7_hIuA")


@pytest.fixture
def item2():
    return Channel("UC1eFXmJNkjITxPFWTy6RsWg")


@pytest.fixture
def video1():
    return Video('9lO06Zxhu88')

@pytest.fixture
def video2():
    return PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')

@pytest.fixture
def video3():
    return Video('broken_video')


@pytest.fixture
def playlist1():
    return PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')


def test_Channel(item1, item2):
    assert item1.description == "Здесь задают вопросы"
    assert item1.url == "https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA"
    assert item1.subscriberCount == 10_300_000
    assert item1.videoCount == 165
    assert item1.viewCount == 1_964_001_481
    item1.to_json()
    assert item1.__str__() == "Youtube-канал: вДудь"
    assert item1.__gt__(item2) == True
    assert item1.__le__(item2) == False
    assert item1 + item2 == 14_010_000
    assert item2 + item1 == 14_010_000


def test_Video(video1, video3):
    assert video1.__str__() == "Как устроена IT-столица мира / Russian Silicon Valley (English subs)"
    assert video3.video_title is None
    assert video3.video_like_count is None


def test_PLVideo(video2):
    assert video2.__str__() == "Пушкин: наше все? (Литература)"

def test_PlayList(playlist1):
    assert playlist1.title == "Редакция. АнтиТревел"
    assert playlist1.url == "https://www.youtube.com/playlist?list=PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb"
    assert playlist1.get_videos_duration.total_seconds() == 13261.0
    assert playlist1.show_best_video() == "https://youtu.be/S7Ri5-9WHQY"