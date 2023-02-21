from classes import Channel

# пробный тест на примере канала Дудя
item_1 = Channel("UCMCgOm8GZkHp8zJ6l7_hIuA")
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
