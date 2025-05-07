import requests
from bs4 import BeautifulSoup
from data.models.city import City
import pandas as pd

# Настраиваем User-Agent (обязательно!)
headers = {
    "User-Agent": "RussianCitiesParser/1.0 (contact@example.com)"
}

url = "https://ru.wikipedia.org/wiki/Список_городов_России"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text)


# Находим таблицу с городами (обычно это первая таблица класса 'wikitable')
table = soup.find('table')

# Извлекаем данные
cities = []
cities_dicts = []
for row in table.find_all('tr')[1:]:  # Пропускаем заголовок
    cols = row.find_all('td')
    if len(cols) >= 6:  # Проверяем, что строка содержит данные
        city = City(cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip())
        city_data = {
            'Название': cols[1].text.strip(),
            'Регион': cols[2].text.strip(),
            'Население': cols[3].text.strip(),
            'Год основания': cols[4].text.strip(),
            'Координаты': cols[5].text.strip(),
            # Доп. поля (если есть)
            'Статус': cols[0].text.strip() if len(cols) > 6 else None,
        }
        cities.append(city)
        cities_dicts.append(city_data)

# Сохраняем в DataFrame
df = pd.DataFrame(cities_dicts)
print(df.head())

print()
