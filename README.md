# Программа для парсинга информации по городам из открытых источников (Росстат и Википедия)
## Парсинг
Основная информация берется из файлов Росстата и дополняется данными с Википедии

## Дамп БД
Полный файл дампа находится в файле database/dump.sql

Дамп таблицы "Города"
```SQL
CREATE TABLE city (
    id_city SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    population INTEGER,
    birth_rate FLOAT,
    mortality_rate FLOAT,
    employees_number FLOAT,
    salary FLOAT,
    investments FLOAT,
    turnover FLOAT,
    foundation_year INTEGER,
    id_region INTEGER NOT NULL,
    id_federal_district INTEGER NOT NULL,
    CONSTRAINT fk_city_region 
        FOREIGN KEY (id_region) 
        REFERENCES region(id_region)
        ON DELETE CASCADE,
    CONSTRAINT fk_city_federal_district 
        FOREIGN KEY (id_federal_district) 
        REFERENCES federal_district(id_federal_district)
        ON DELETE CASCADE,
    CONSTRAINT uq_city_region UNIQUE (name, id_region) -- Один город с одним именем в одном регионе
);
```

Индексы для таблицы городов:
```SQL
CREATE INDEX idx_city_name ON city(name);
CREATE INDEX idx_city_region ON city(id_region);
CREATE INDEX idx_city_federal_district ON city(id_federal_district);
```

Таблица "Регионы"
```SQL
CREATE TABLE region (
    id_region SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    id_federal_district INTEGER NOT NULL,
    CONSTRAINT fk_region_federal_district 
        FOREIGN KEY (id_federal_district) 
        REFERENCES federal_district(id_federal_district)
        ON DELETE CASCADE
);
```

Индексы для таблицы "Регионы"
```SQL
CREATE INDEX idx_region_name ON region(name);
CREATE INDEX idx_region_federal_district ON region(id_federal_district);
```

Таблица "Федеральные округа"
```SQL
CREATE TABLE federal_district (
    id_federal_district SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
```

Индекс для таблицы "Федеральные округа"
```SQL
CREATE INDEX idx_federal_district_name ON federal_district(name);
```

Пример селекта из базы данных (Выбирает все данные по Москве)
```SQL
SELECT city.name AS name, city.population, city.birth_rate, 
	city.mortality_rate, city.employees_number, city.salary, city.investments, 
	turnover, foundation_year, federal_district.name AS federal_district, region.name AS region FROM city
JOIN federal_district ON city.id_federal_district = federal_district.id_federal_district
JOIN region on city.id_region = region.id_region
WHERE city.name = 'Москва'
```
## Архитектура базы данных

### Описание таблиц

#### 1. Таблица `federal_district`

- **Описание**: Хранит информацию о федеральных округах.
- **Ключи**:
  - `id_federal_district`: PRIMARY KEY, уникальный идентификатор федерального округа.
- **Индексы**:
  - `idx_federal_district_name`: Индекс для быстрого поиска по имени федерального округа.

#### 2. Таблица `region`

- **Описание**: Хранит информацию о регионах, связанных с федеральными округами.
- **Ключи**:
  - `id_region`: PRIMARY KEY, уникальный идентификатор региона.
  - `id_federal_district`: FOREIGN KEY, ссылается на `id_federal_district` в таблице `federal_district`.
- **Индексы**:
  - `idx_region_name`: Индекс для быстрого поиска по имени региона.
  - `idx_region_federal_district`: Индекс для быстрого поиска по идентификатору федерального округа.

#### 3. Таблица `city`

- **Описание**: Хранит информацию о городах, связанных с регионами и федеральными округами.
- **Ключи**:
  - `id_city`: PRIMARY KEY, уникальный идентификатор города.
  - `id_region`: FOREIGN KEY, ссылается на `id_region` в таблице `region`.
  - `id_federal_district`: FOREIGN KEY, ссылается на `id_federal_district` в таблице `federal_district`.
  - `uq_city_region`: UNIQUE CONSTRAINT, обеспечивает уникальность названия города в пределах одного региона.
- **Индексы**:
  - `idx_city_name`: Индекс для быстрого поиска по имени города.
  - `idx_city_region`: Индекс для быстрого поиска по идентификатору региона.
  - `idx_city_federal_district`: Индекс для быстрого поиска по идентификатору федерального округа.

### Хранение данных

- **Тип хранения**: Строковое хранение. Все таблицы используют строковое хранение для текстовых данных.
- **Типы данных**:
  - `SERIAL`: Автоинкрементные целые числа для идентификаторов.
  - `VARCHAR`: Строки фиксированной длины для имен.
  - `INTEGER`: Целые числа для числовых значений.
  - `FLOAT`: Числа с плавающей запятой для показателей.

## Источники
- **Росстат**: Население, Рождаемость, Смертность, Количество работников, Зарплата, Инвестиции, Оборот
- **Википедия**: Регион, Федеральный округ, год основания

## Шаги ETL
- **Extract**: Загрузка архивов с таблицами с сайта Росстата, парсинг их в DataFrame. Парсинг таблицы городов с сайта Википедия
- **Transform**: Преобразование данных. Удаление лишних пробелов и примечаний из названия городов, приведение годов и данных к единому формату.
- **Load**: Загрузка данных в базу данных (PostgreSQL)

## Схема БД
### 1. `federal_district` (Федеральные округа)
Хранит информацию о федеральных округах РФ.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id_federal_district` | SERIAL | Уникальный идентификатор | PRIMARY KEY |
| `name` | VARCHAR(100) | Название округа | NOT NULL, UNIQUE |


### 2. `region` (Регионы)
Содержит данные о регионах (субъектах РФ) и их принадлежности к округам.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id_region` | SERIAL | Уникальный идентификатор | PRIMARY KEY |
| `name` | VARCHAR(100) | Название региона | NOT NULL, UNIQUE |
| `id_federal_district` | INTEGER | Ссылка на федеральный округ | FOREIGN KEY, NOT NULL |

### 3. `city` (Города)
Основная таблица с подробной информацией о городах.

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id_city` | SERIAL | Уникальный идентификатор | PRIMARY KEY |
| `name` | VARCHAR(100) | Название города | NOT NULL |
| `population` | FLOAT | Численность населения | |
| `birth_rate` | FLOAT | Уровень рождаемости | |
| `mortality_rate` | FLOAT | Уровень смертности | |
| `employees_number` | FLOAT | Численность сотрудников | |
| `salary` | FLOAT | Средняя зарплата | |
| `investments` | FLOAT | Объем инвестиций | |
| `turnover` | FLOAT | Оборот предприятий | |
| `foundation_year` | INTEGER | Год основания | |
| `id_region` | INTEGER | Ссылка на регион | FOREIGN KEY, NOT NULL |
| `id_federal_district` | INTEGER | Ссылка на федеральный округ | FOREIGN KEY, NOT NULL |

## Архитектура проека
- **data**: Хранит необходимые данные для загрузки файлов и парсинга. Также содержит сами файлы.
- **database**: Содержит информацию о базе данных (Схема, дамп)
- **scripts**: Хранит скрипты для загрузки/изменения/загрузки информации
- **unrar**: Необходимая утилита для работы с rar архивами

## Необходимые зависимости
- **psycopg2**
- **Beautiful Soup**
- **rarfile**
- **requests**
- **pandas**
- **openpyxl**

```
pip install psycopg2
pip install beautifulSoup4
pip install rarfile
pip install requests
pip install pandas
pip install openpyxl
```

