class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        href_json = response.json()
        href = href_json['href']
        upl_file = requests.put(href, data=open(filename, 'rb'))
        upl_file.raise_for_status()
        if upl_file.status_code == 201:
            print(f"Файл {file_path} загружен на Яндекс.Диск!")


if __name__ == '__main__':
    import requests

    # Получить путь к загружаемому файлу и токен от пользователя
    filename = 'files/9_1.py'
    path_to_file = 'task_9_1.py'
    token = ""
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)