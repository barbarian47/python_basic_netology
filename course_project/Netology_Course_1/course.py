import requests
import json
from tqdm import tqdm
import hashlib
import token_47

"""Создает json файл с информацией о загруженных фото"""
def create_json(photos_info, id, count):
    to_json = []
    for key, value in photos_info.items():
        photo_name = key + '.jpg'
        info = {'file_name': photo_name, 'size': value[1]}
        if len(to_json) < count:
            to_json.append(info)

    file_name = f'{id}_info.json'
    with open (file_name, 'w') as file:
        json.dump(to_json, file)

    print("Файл с информацией готов!")

"""Получает id пользователя"""
def vk_profile_info(token, v):
    api = 'https://api.vk.com/method/'
    method = 'account.getProfileInfo'
    params = {
            'access_token': token,
            'v': v
    }
    url = api + method
    response = requests.get(url, params=params)
    id = response.json()['response']['id']
    return id

"""Получает фотографии с максимальным разрешением"""
def vk_high_size(sizes):
    max_size = 0
    photo_url = ''
    photo_size = ''

    for size in sizes:
        if size['height'] * size['width'] > max_size:
            max_size = size['height'] * size['width']
            photo_url = size['url']
            photo_size = size['type']

    return photo_url, photo_size

"""Создает словарь с ссылками на фото"""
def vk_get_photo(id, token, v, album_id='profile'):
    api = 'https://api.vk.com/method/'
    method = 'photos.get'
    params = {
            'access_token': token,
            'v': v,
            'owner_id': id,
            'album_id': album_id,
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1,
    }
    url = api + method
    response = requests.get(url, params=params)
    photo_list = response.json()['response']['items']
    photo_filter = {}

    for photo in photo_list:
        photo_name = str(photo['likes']['count'])
        if photo_name in photo_filter:
            photo_name = photo_name + '_' + str(photo['date'])
        photo_url, photo_size = vk_high_size(photo['sizes'])
        photo_filter[photo_name] = [photo_url, photo_size]

    return photo_filter

"""Получает список альбомов аккаунта"""
def ok_get_album(id, app_key, token, sess_secr_key):
    url = "https://api.ok.ru/fb.do"
    params = {
        "application_key": app_key,
        "fid": id,
        "format": "json",
        "access_token": token
    }
    method = "photos.getAlbums"
    row = f"application_key={app_key}fid={id}format=jsonmethod={method}{sess_secr_key}"
    sig = hashlib.md5(row.encode('utf-8')).hexdigest()
    params_delta = {"method": method, "sig": sig}
    response = requests.get(url, params={**params, **params_delta}).json()

    album_list = {}
    albums = response['albums']
    for album in albums:
        album_list[album['title']] = album['aid']

    return album_list

"""Получает id альбома из которго скачиваем фото"""
def get_aid(albums):
    print('Список альбомов пользователя:')
    for key in albums:
        print(f'- {key}')
    album_name = input('Название альбома из которого хотите скчать фото: ')
    if album_name in albums:
        aid = albums[album_name]
    else:
        print(f'Альбома {album_name} нет в списке!')
        get_aid(albums)

    return aid

"""Получает фотографии с максимальным разрешением"""
def ok_high_size(sizes):
    max_size = 0
    photo_url = ''
    photo_size = ''
    for key in sizes:
        if 'pic' in key:
            pic = key.strip('pic').split('x')
            if int(pic[0]) * int(pic[1]) > max_size:
                max_size = int(pic[0]) * int(pic[1])
                photo_url = sizes[key]
                photo_size = f'{pic[0]}x{pic[1]}'
    high_size = [photo_url, photo_size]

    return high_size

"""Создает словарь с ссылками на фото"""
def ok_get_photo(id, app_key, token, sess_secr_key, aid=None):
    url = 'https://api.ok.ru/fb.do'
    params = {
        "application_key": app_key,
        "fid": id,
        "format": "json",
        "access_token": token
    }
    method = "photos.getPhotos"
    if aid:
        row = f"aid={aid}application_key={app_key}fid={id}format=jsonmethod={method}{sess_secr_key}"
    else:
        row = f"application_key={app_key}fid={id}format=jsonmethod={method}{sess_secr_key}"

    sig = hashlib.md5(row.encode('utf-8')).hexdigest()
    params_delta = {"method": method, "sig": sig, "aid": aid}
    response = requests.get(url, params={**params, **params_delta}).json()

    photo_list = response['photos']
    photo_filter = {}

    for photo in photo_list:
        photo_filter[photo['id']] = ok_high_size(photo)

    return photo_filter

"""Создает папку в облаке для загрузки"""
def create_folder(id, token):
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(token)
    }
    params = {'path': id}
    response = requests.put(url, headers=headers, params=params)
    if response.status_code == 201:
        print(f'Папка "{id}" создана на Яндекс.Диск!')
    elif response.status_code == 409:
        print(f'Папка "{id}" уже есть на Яндекс.Диск!')
    else:
        print("Что-то пошло не так!")

"""Загружает фото в созданную папку"""
def to_ya_disk(id, token, photos_info, count=5):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(token)
    }
    if count > len(photos_info):
        pbar = tqdm(total=len(photos_info))
    else:
        pbar = tqdm(total=count)
    for key, value in photos_info.items():
        params = {'path': f"{id}/{key}.jpg", 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        href_json = response.json()
        href = href_json['href']
        photo = requests.get(value[0])
        upl_file = requests.put(href, data=photo)
        upl_file.raise_for_status()
        if upl_file.status_code == 201:
            count -= 1
            pbar.update()
            if count == 0:
                break
    pbar.close()
    print(f"Загрузка на Яндекс.Диск завершена!")


if __name__ == '__main__':
    while True:
        vk_social = ['VK', 'vk', 'vkontakte', 'VKontakte', 'Vkontakte', 'ВК', 'вк', 'ВКонтакте',
                     'вконтакте', 'Вконтакте', 'BK', 'контакт', 'Контакт']
        ok_social = ['Одноклассники', 'одноклассники', 'ОК', 'ок', 'Ок', 'OK', 'ok', 'Ok']
        social = input("Введите название соц.сети: ")

        if social in vk_social:
            S_TOKEN = token_47.vk_token
            vk_v = 5.131
            id = input("Введите id пользователя: ")
            photos_info = vk_get_photo(id=id, token=S_TOKEN, v=vk_v, album_id='profile')

        elif social in ok_social:
            APPLICATION_KEY = token_47.ok_application_key
            S_TOKEN = token_47.ok_access_token
            SESSION_SECRET_KEY = token_47.ok_session_secret_key
            id = input("Введите id пользователя: ")
            albums = ok_get_album(id=id, app_key=APPLICATION_KEY, token=S_TOKEN, sess_secr_key=SESSION_SECRET_KEY)
            if albums:
                aid = get_aid(albums)
                photos_info = ok_get_photo(id=id, app_key=APPLICATION_KEY, token=S_TOKEN, sess_secr_key=SESSION_SECRET_KEY,
                                           aid=aid)
            else:
                photos_info = ok_get_photo(id=id, app_key=APPLICATION_KEY, token=S_TOKEN, sess_secr_key=SESSION_SECRET_KEY)
        else:
            print('На данный момент программа не работает с этой соц.сетью.')
            break

        count = int(input("Сколько фотографий вы хотите загрузить: "))

        yandex_cloud = ['Яндекс.Диск', 'яндекс.диск', 'ЯндексДиск', 'яндексдиск', 'Яндекс', 'яндекс', 'я',
                        'Я', 'Yandex.Disk', 'YandexDisk', 'yandex.disk', 'yandexdisk', 'Yandex', 'yandex',
                        'Ya', 'ya']
        google_cloud = ['Google.Drive', 'GoogleDrive', 'google.drive', 'googledrive', 'Drive', 'Google',
                        'Гугл.Драйв', 'Гугл.Диск', 'ГуглДиск', 'ГуглДрайв', 'google', 'гугл', 'Гугл']
        cloud = input("Веедите название облака: ")

        if cloud in yandex_cloud:
            C_TOKEN = input("Введите токен облака: ")
            create_folder(id, token=C_TOKEN)
            to_ya_disk(id=id, token=C_TOKEN, photos_info=photos_info, count=count)
        else:
            print('На данный момент программа не работает с этим облаком.')
            break

        create_json(photos_info, id, count)
        break