from io import BytesIO

import rarfile
import requests
import pandas as pd

from data.rosstat.rosstat_config import rosstat_urls, rosstat_path
from scripts.extract.rosstat.rosstat_file_parser import parse_new

def download_data():
    for i in range(len(rosstat_urls)):
        url = rosstat_urls[i]
        response = requests.get(url)

        if response.status_code != 200:
            print(f'Ошибка: {response.status_code}')
            break

        rar_path = f'{rosstat_path}temp{i}.rar'
        print(f'Загрузка файла: {rar_path}, URL: {url}')
        with open(rar_path, 'wb') as f:
            f.write(response.content)

def extract_data():
    data_final = pd.DataFrame()
    rarfile.UNRAR_TOOL = "unrar\\UnRAR.exe"
    for i in range(len(rosstat_urls)):
        archive_path = f'{rosstat_path}temp{i}.rar'
        try:
            with rarfile.RarFile(archive_path) as rar:
                file_list = rar.namelist()
                xlsx_files = [f for f in file_list if f.lower().endswith('.xlsx')]
                if not xlsx_files:
                    print('Error in archive not found files!')
                xlsx_file = list(filter(lambda s: '01' in s, xlsx_files))[0]
                try:
                    file_data = BytesIO(rar.read(xlsx_file))
                    data = parse_new(file_data)
                    df_final = pd.concat([df_final, data])
                except Exception as e:
                    print(f'File: {xlsx_file}')
                    print(f'Error: {e}')
        except Exception as e:
            print(f'File: {xlsx_file}')
            print(f'Error: {e}')
    return df_final



