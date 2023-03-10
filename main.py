from classes import Channel, Video, PLVideo, PlayList


# # тест по видео и плэйлистам
pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
print(pl.title)
print(pl.url)
print(pl.get_videos_duration) # длительность плейлиста в формате ЧЧ:ММ:СС
print(type(pl.get_videos_duration)) # тип данных для вывожа длительности
print(pl.get_videos_duration.total_seconds()) # длительность в секундах
print(pl.show_best_video()) # ссылка на лучшее видео