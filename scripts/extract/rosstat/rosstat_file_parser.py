import pandas as pd

# def parse(path):
#     data = {}
#     sheet_names = pd.ExcelFile(path).sheet_names
<<<<<<< HEAD
=======
#     #region_name = os.path.basename(file_path.split('_')[-1]).replace('.xlsx', '')
#     #data['Область']['Название'] = region_name
>>>>>>> 1008506 (no message)
#
#     solo_city = True
#
#     try:
#             df_table3 = pd.read_excel(path, sheet_name=sheet_names[-1], header=None)
<<<<<<< HEAD
=======
#             cities = []
>>>>>>> 1008506 (no message)
#             if 'городов' in df_table3.iloc[0][0].lower():
#                 solo_city = False
#
#             if not solo_city:
#                 cities = []
#
#                 for s in df_table3.iloc[2]:
#                     if pd.notna(s):
#                         if s.endswith(')'):
#                             cities.append(s[:-2])
#                         else:
#                             cities.append(s)
#
#                 #data['Города']['Названия'] = cities
#
#                 for i in range(len(cities)):
#                     data[cities[i]] = {
#                         'Население': str(df_table3.iloc[5][(i + 1) * 2])[:-2] if str(df_table3.iloc[5][(i + 1) * 2]).endswith(')') else df_table3.iloc[5][(i + 1) * 2],
#                         'Рождаемость': str(df_table3.iloc[11][(i + 1) * 2])[:-2] if str(df_table3.iloc[11][(i + 1) * 2]).endswith(')') else df_table3.iloc[11][(i + 1) * 2],
#                         'Смертность': str(df_table3.iloc[12][(i + 1) * 2])[:-2] if str(df_table3.iloc[12][(i + 1) * 2]).endswith(')') else df_table3.iloc[12][(i + 1) * 2],
#                         'Численность сотрудников': str(df_table3.iloc[16][(i + 1) * 2])[:-2] if str(df_table3.iloc[16][(i + 1) * 2]).endswith(')') else df_table3.iloc[16][(i + 1) * 2],
#                         'Зарплата': str(df_table3.iloc[20][(i + 1) * 2])[:-2] if str(df_table3.iloc[20][(i + 1) * 2]).endswith(')') else df_table3.iloc[20][(i + 1) * 2],
#                         'Пенсия': str(df_table3.iloc[21][(i + 1) * 2])[:-2] if str(df_table3.iloc[21][(i + 1) * 2]).endswith(')') else df_table3.iloc[21][(i + 1) * 2],
#                         'Инвестиции': str(df_table3.iloc[25][(i + 1) * 2])[:-2] if str(df_table3.iloc[25][(i + 1) * 2]).endswith(')') else df_table3.iloc[25][(i + 1) * 2],
#                     }
<<<<<<< HEAD
#             return data
#     except Exception as e:
#         print(f"Ошибка при парсинге 'Таблица 3' в файле {path}: {e}")
#
#     return None
=======
#     except Exception as e:
#         print(f"Ошибка при парсинге 'Таблица 3' в файле {path}: {e}")
#
#
>>>>>>> 1008506 (no message)
#     pd.set_option('display.max_rows', None)  # Показать все строки
#     pd.set_option('display.max_columns', None)  # Показать все столбцы
#     pd.set_option('display.width', None)  # Автоматическая ширина колонок
#     pd.set_option('display.max_colwidth', None)  # Показать полное содержимое ячеек
#
#     df = pd.DataFrame(data)
#     print(df)

<<<<<<< HEAD
def parse_new(path):
    df_table3 = pd.read_excel(path, header=None)

    columns = [
        'Название',
        'Население', 
        'Рождаемость',
        'Смертность',
        'Численность сотрудников',
        'Зарплата',
        'Инвестиции',
        'Оборот'
    ]
    
    data = pd.DataFrame(columns=columns)
=======
def parse_new(path) -> dict:
    df_table3 = pd.read_excel(path, header=None)

    data = {}
>>>>>>> 1008506 (no message)

    index = 2
    while True:
        year = df_table3.iloc[-index][0]
        if year[0].isdigit():
            break

<<<<<<< HEAD
        new_row = {
            'Название': df_table3.iloc[-index][0],
=======
        data[df_table3.iloc[-index][0]] = {
>>>>>>> 1008506 (no message)
            'Население': df_table3.iloc[-index][1],
            'Рождаемость': df_table3.iloc[-index][2],
            'Смертность': df_table3.iloc[-index][3],
            'Численность сотрудников': df_table3.iloc[-index][4],
            'Зарплата': df_table3.iloc[-index][5],
            'Инвестиции': df_table3.iloc[-index][9],
            'Оборот': df_table3.iloc[-index][18],
        }
<<<<<<< HEAD
        
        data = pd.concat(
            [data, pd.DataFrame([new_row])]
        )
        
=======
>>>>>>> 1008506 (no message)
        index += 1

    return data

