import pandas as pd

# Парсинг файла со статистикой
def parse(path):
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

    index = 2
    while True:
        try:
            year = df_table3.iloc[-index][0]
            if year[0].isdigit():
                break

            new_row = {
                'Название': df_table3.iloc[-index][0],
                'Население': df_table3.iloc[-index][1],
                'Рождаемость': df_table3.iloc[-index][2],
                'Смертность': df_table3.iloc[-index][3],
                'Численность сотрудников': df_table3.iloc[-index][4],
                'Зарплата': df_table3.iloc[-index][5],
                'Инвестиции': df_table3.iloc[-index][9],
                'Оборот': df_table3.iloc[-index][18],
            }

            data = pd.concat(
                [data, pd.DataFrame([new_row])]
            )

            index += 1
        except Exception as e:
            print(e)

    return data
