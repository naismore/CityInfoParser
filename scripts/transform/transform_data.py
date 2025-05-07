import pandas as pd
import re

# Приведение вида года к единому формату
def reformat_wiki_year(wiki_data):
    for city in wiki_data:
        if not str(city['Год основания']).isdigit():
            match = re.match(r'^(-?\d{1,4})[^\d]*', city['Год основания'])
            if match:
                city['Год основания'] = int(match.group(1))
    return wiki_data

# Приведение типа FLOAT от вида с запятой к виду с точкой
def reformat_rosstat_values(rosstat_data):
    # Заменяем запятые на точки и убираем пробелы для числовых столбцов
    numeric_cols = ['Население', 'Рождаемость', 'Смертность',
                    'Численность сотрудников', 'Зарплата',
                    'Инвестиции', 'Оборот']

    for col in numeric_cols:
        if col in rosstat_data.columns:
            rosstat_data[col] = (
                rosstat_data[col]
                .astype(str)  # Преобразуем в строку на случай, если там уже числа
                .str.replace(',', '.', regex=False)
                .str.strip()
            )

    return rosstat_data

# Удаление лишних пробелов в именах
def reformat_rosstat_names(rosstat_data):
    rosstat_data['Название'] = rosstat_data['Название'].str.strip()
    return rosstat_data

# Замена буквы ё на е и удаление приписки "не призн."
def reformat_wiki_names(wiki_data):
    wiki_data['Название'] = wiki_data['Название'].str.replace('не призн.', '', regex=False).str.strip()
    wiki_data['Название'] = wiki_data['Название'].str.replace('ё', 'е', regex=False).str.strip()
    return wiki_data


def transform_data(rosstat_data, wiki_data):
    wiki = reformat_wiki_year(wiki_data)
    df_rosstat = pd.DataFrame(rosstat_data)
    df_wiki = pd.DataFrame(wiki)

    # Удаляем дубликаты
    df_wiki = df_wiki.drop_duplicates(subset=['Название'], keep='first')
    df_rosstat = df_rosstat.drop_duplicates(subset=['Название'], keep='first')

    # Оставляем только нужные поля
    df_wiki = df_wiki[['Название', 'Регион', 'Федеральный округ', 'Год основания']]

    # Приводим к общему формату
    df_rosstat = reformat_rosstat_names(rosstat_data)
    df_rosstat = reformat_rosstat_values(rosstat_data)

    df_wiki = reformat_wiki_names(df_wiki)

    # Объединяем датафреймы
    merged_df = df_rosstat.merge(df_wiki, left_on='Название', right_on='Название', how='left')
    return merged_df
    
    
    
    
    
    
        
    






