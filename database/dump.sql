-- Создание таблицы Федеральных округов
CREATE TABLE federal_district (
    id_federal_district SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Создание индекса для имени федерального округа
CREATE INDEX idx_federal_district_name ON federal_district(name);

-- Создание таблицы Регионов
CREATE TABLE region (
    id_region SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    id_federal_district INTEGER NOT NULL,
    CONSTRAINT fk_region_federal_district
        FOREIGN KEY (id_federal_district)
        REFERENCES federal_district(id_federal_district)
        ON DELETE CASCADE
);

-- Создание индексов для таблицы регионов
CREATE INDEX idx_region_name ON region(name);
CREATE INDEX idx_region_federal_district ON region(id_federal_district);

-- Создание таблицы Городов
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

-- Создание индексов для таблицы городов
CREATE INDEX idx_city_name ON city(name);
CREATE INDEX idx_city_region ON city(id_region);
CREATE INDEX idx_city_federal_district ON city(id_federal_district);
