import pandas as pd
import re

#TODO: Убрать в финальной версии, нужно только для дебага
pd.set_option('display.max_rows', None)  # Показать все строки
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', None)  # Автоматическая ширина колонок
pd.set_option('display.max_colwidth', None)  # Показать полное содержимое ячеек

def reformat_wiki_year(wiki_data):
    for city in wiki_data:
        if not str(city['Год основания']).isdigit():
            match = re.match(r'^(-?\d{1,4})[^\d]*', city['Год основания'])
            if match:
                city['Год основания'] = int(match.group(1))
    return wiki_data

def reformat_rosstat_population(rosstat_data):
    rosstat_data['Население'] = pd.to_numeric(rosstat_data['Население'] * 1000, errors='coerce').fillna(0).astype(int)
    return rosstat_data


def transform_data(rosstat_data, wiki_data):
    wiki = reformat_wiki_year(wiki_data)
    rosstat = reformat_rosstat_population(rosstat_data)
    df_rosstat = pd.DataFrame(rosstat)
    df_wiki = pd.DataFrame(wiki)
    
    df_rosstat = df_rosstat.drop_duplicates(subset=['Название'], keep='first')
    df_wiki = df_wiki.drop_duplicates(subset=['Название'], keep='first')
    
    df_wiki = df_wiki[['Название', 'Регион', 'Федеральный округ', 'Год основания']]
    
    merged_df = df_rosstat.merge(df_wiki, left_on='Название', right_on='Название', how='left')
    print(merged_df)
    
    
    
    
    
    
        
    






