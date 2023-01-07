def question_list(tag, fromdate, todate):
    site = 'https://api.stackexchange.com/2.3/questions'
    params = {
        'fromdate': fromdate,
        'todate': todate,
        'order': 'desc',
        'sort': 'activity',
        'tagged': tag,
        'site': 'stackoverflow'
    }

    response = requests.get(site, params=params)
    dict_json = response.json()

    print(f"Список запросов с тэгом - {tag}:\n")
    for question in dict_json['items']:
        print(f"- {question['title']}")
        print(question['link'], "\n")

if __name__ == '__main__':
    import time
    import requests

    current_time = int(time.time())
    two_days = 172800
    start_time = current_time - two_days
    tag = 'Python'

    question_list(tag, start_time, current_time)