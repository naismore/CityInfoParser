import scripts.extract.rosstat.rosstat_extract_data as rosstat
import scripts.extract.wikipedia.wikipedia_extract_data as wikipedia
from scripts.load.load_to_db import load_data
from scripts.transform.transform_data import transform_data

try:
    rosstat.download_data()
    print('Файлы успешно загружены. Парсим...')
    rosstat_raw_data = rosstat.extract_data()
    print('Парсинг сайта Wikipedia...')
    wiki_raw_data = wikipedia.extract_data()
    print('Приведение к общему формату...')
    data = transform_data(rosstat_raw_data, wiki_raw_data)
    print('Загрузка в базу данных...')
    load_data(data)
    print('Успешно')
except Exception as e:
    print(e)