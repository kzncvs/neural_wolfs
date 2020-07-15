import vk_api
import config
import json


def get_vk_session():
    vk_session = vk_api.VkApi(config.vk_phone_number, config.vk_password)
    vk_session.auth()
    return vk_session.get_api()


def get_max_size_link(album_item):
    sizes = album_item['sizes']
    max_height = 0
    max_height_link = None
    for size in sizes:
        if size['height'] > max_height:
            max_height = size['height']
            max_height_link = size['url']
    return max_height_link


def prepare_album_item(album_item):
    link = get_max_size_link(album_item)
    likes_count = album_item['likes']['count']
    date = album_item['date']
    public_id = album_item['owner_id']
    return {
        'link': link,
        'likes_count': likes_count,
        'date': date,
        'public_id': public_id
    }


vk = get_vk_session()
prepared_photos = []
for public_id in config.wolf_meme_public_ids:
    photos_handled = 0
    offset = 0
    while True:
        album_photos_slice = vk.photos.get(
            owner_id=public_id,
            album_id='wall',
            count=1000,
            photo_sizes=1,
            extended=1,
            offset=offset
        )
        for album_photo in album_photos_slice['items']:
            prepared_photos.append(prepare_album_item(album_photo))
            photos_handled += 1
        if photos_handled >= album_photos_slice['count']:
            break
        offset += 1


with open(config.wolfs_from_vk_file, 'w') as file:
    file.write(json.dumps(prepared_photos, indent=2, ensure_ascii=False))
