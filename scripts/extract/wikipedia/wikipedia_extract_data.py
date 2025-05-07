import requests
from bs4 import BeautifulSoup

# Парсинг страницы с таблицой по городам России
def extract_data():
    headers = {
        "User-Agent": "RussianCitiesParser/1.0 (contact@example.com)"
    }

    url = "https://ru.wikipedia.org/wiki/Список_городов_России"
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text)

        table = soup.find('table')

        cities_dicts = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 6:
                city_data = {
                    'Название': cols[2].text.strip(),
                    'Регион': cols[3].text.strip(),
                    'Федеральный округ': cols[4].text.strip(),
                    'Население': cols[5].text.strip(),
                    'Год основания': cols[6].text.strip(),
                }
                cities_dicts.append(city_data)
        return cities_dicts
    except Exception as e:
        print(e)
        return None
