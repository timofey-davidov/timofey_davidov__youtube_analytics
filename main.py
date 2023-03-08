from classes import Channel, Video, PLVideo, PlayList

# пробный тест на примере канала Дудя
item_1 = Channel("UCMCgOm8GZkHp8zJ6l7_hIuA")
item_2 = Channel("UC1eFXmJNkjITxPFWTy6RsWg")
print(item_1.channel_info)
print(item_1.channel_id)
print(item_1.title)
print(item_1.description)
print(item_1.url)
print(item_1.subscriberCount)
print(item_1.videoCount)
print(item_1.viewCount)
# item_1.channel_id = "Новое название"
print(Channel.get_service())
item_1.to_json()
print(item_1)
print(item_1 > item_2)
print(item_1 <= item_2)
print(item_1 + item_2)
print(item_2 + item_1)
# тест по видео и плэйлистам
video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(video1)
print(video2)
pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
print(pl.title)
print(pl.url)
print(pl.get_videos_duration) # длительность плейлиста в формате ЧЧ:ММ:СС
print(type(pl.get_videos_duration)) # тип данных для вывожа длительности
print(pl.get_videos_duration.total_seconds()) # длительность в секундах
print(pl.show_best_video()) # ссылка на лучшее видео