import psycopg2
from dotenv import load_dotenv

def load_data(data):
    print(data)
    load_dotenv()
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="cities",
            user="postgres",
            password="123123",
            host="localhost"
        )
        cursor = conn.cursor()

        # Обработка федеральных округов
        federal_districts = data['Федеральный округ'].dropna().unique()
        for fd in federal_districts:
            cursor.execute(
                "INSERT INTO federal_district (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                (fd,)
            )

        # Обработка регионов
        regions = data[['Регион', 'Федеральный округ']].dropna().drop_duplicates()
        for _, row in regions.iterrows():
            cursor.execute(
                """INSERT INTO region (name, id_federal_district)
                   VALUES (%s, (SELECT id_federal_district FROM federal_district WHERE name = %s)) ON CONFLICT (name) DO
                UPDATE SET
                    id_federal_district = EXCLUDED.id_federal_district""",
                (row['Регион'], row['Федеральный округ'])
            )

        # Обработка городов
        for _, row in data.iterrows():
            cursor.execute(
                """INSERT INTO city (name, population, birth_rate, mortality_rate, employees_number,
                                     salary, investments, turnover, foundation_year, id_region, id_federal_district)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                           (SELECT id_region FROM region WHERE name = %s),
                           (SELECT id_federal_district FROM federal_district WHERE name = %s)) ON CONFLICT (name, id_region) DO
                UPDATE SET
                    population = EXCLUDED.population,
                    birth_rate = EXCLUDED.birth_rate,
                    mortality_rate = EXCLUDED.mortality_rate,
                    employees_number = EXCLUDED.employees_number,
                    salary = EXCLUDED.salary,
                    investments = EXCLUDED.investments,
                    turnover = EXCLUDED.turnover,
                    foundation_year = EXCLUDED.foundation_year,
                    id_federal_district = EXCLUDED.id_federal_district""",
                (
                    row['Название'], row['Население'], row['Рождаемость'], row['Смертность'],
                    row['Численность сотрудников'], row['Зарплата'], row['Инвестиции'],
                    row['Оборот'], row['Год основания'], row['Регион'], row['Федеральный округ']
                )
            )

        # Фиксируем изменения и закрываем соединение
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)