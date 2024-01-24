# Проект по базе данных: Информация о компаниях и вакансиях

## Описание проекта
Этот проект включает в себя инструменты для сбора информации о компаниях и вакансиях с использованием API HeadHunter, а также для хранения и анализа этих данных в базе данных PostgreSQL.

## Требования
- Python 3.x
- PostgreSQL
- Библиотеки Python: psycopg2, requests, dateutil

## Установка и настройка
1. Клонировать репозиторий:
git clone https://github.com/TheFimerHub/db-coursework
cd headhunter-db-project

2. Установить необходимые библиотеки:
pip install -r requirements.txt

3. Настроить файл `implemented.py`:
- Заполните переменные `dbname`, `user`, `password`, `host`, `port` согласно вашей конфигурации PostgreSQL.
  (Можете сделать .env)

## Использование

### 1. Сбор данных
- Запустите скрипт `main.py` для сбора данных о компаниях и вакансиях с использованием API HeadHunter. Выберите опцию использования данных по умолчанию или введите свои id компаний.

### 2. Анализ данных
- Запустите скрипт `main.py` для выполнения различных функций анализа:
   - Получение списка всех компаний и количества вакансий в каждой компании.
   - Получение списка всех вакансий.
   - Получение средней зарплаты по вакансиям.
   - Получение списка вакансий с зарплатой выше средней.
   - Поиск вакансий по ключевому слову в заголовке.

## Структура проекта
- `DBManager.py`: Класс для управления базой данных (создание таблиц, вставка данных, выполнение анализа).
- `HeadHunterApi.py`: Класс для взаимодействия с API HeadHunter (сбор данных о компаниях и вакансиях).
- `implemented.py`: Конфигурационный файл с данными для подключения к PostgreSQL.
- `main.py`: Основной скрипт для запуска проекта.

## Автор
Michael Stepanov