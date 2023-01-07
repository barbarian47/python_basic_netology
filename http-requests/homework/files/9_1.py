def hero_iq(heroes, link):
    iq = 0
    smart_hero = list()
    for hero in heroes:
        url = link + hero
        req = requests.get(url)
        hero_info = req.json()
        if int(hero_info['results'][0]['powerstats']['intelligence']) > iq:
            iq = int(hero_info['results'][0]['powerstats']['intelligence'])
            smart_hero.clear()
            smart_hero.append(hero_info['results'][0]['name'])
        elif int(hero_info['results'][0]['powerstats']['intelligence']) == iq:
            smart_hero.append(hero_info['results'][0]['name'])

    return smart_hero, iq

def main():
    heroes = ['Hulk', 'Captain America', 'Thanos']
    site = 'https://www.superheroapi.com/api/'
    api = '2619421814940190'
    link = site + api + '/search/'

    smart_hero, iq = hero_iq(heroes, link)

    print(f"Максимальный показатель интеллекта {iq}: ")
    for name in smart_hero:
        print(name)

if __name__ == '__main__':
    import requests
    main()