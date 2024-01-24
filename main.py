from DBManager import DBManager
from HeadHunterApi import HHJobSearchAPI

if __name__ == "__main__":
    # Создание объекта DBManager для управления базой данных
    dbm = DBManager()

    # Удаление существующих таблиц в базе данных (если они существуют)
    dbm.drop_tables()

    # Сценарий 1: Ввод данных о компаниях
    while True:
        print('Приветствую вас в проекте по БД!\nТут вы узнаете информацию о компаниях по их id.')
        print('Хотите ли вы ввести свои собранные компании или использовать по Умолчанию?')
        print('\nВыберете цифру "1" или "2".')
        print('   1. Использвать по Умолчанию')
        print('   2. Ввести свои данные')

        try:
            answer = input()

            if answer == '1':
                break
            elif answer == '2':
                print('Введите id компаний через пробел.\nПо типу: 192 1344 24335 3567')
                companies = list(map(int, input().split(' ')))
                hha = HHJobSearchAPI()
                hha.companies = companies
                break
            else:
                print("Что-то пошло не так. Попробуйте снова!")
                continue
        except Exception:
            print("Что-то пошло не так. Попробуйте снова!")
            continue

    # Создание таблиц в базе данных
    dbm.create_tables()

    # Загрузка данных о компаниях и вакансиях в базу данных
    dbm.insert_data()

    # Сценарий 2: Выбор функции для использования
    while True:
        print('')
        print("Выберете функцию, которую вы хотите использовать:")
        print("   1. Получить список всех компаний и количество вакансий в каждой компании")
        print("   2. Получить список всех вакансий")
        print("   3. Получить среднюю зарплату по вакансиям")
        print("   4. Получает список всех вакансий с зарплатой выше средней по всем вакансиям")
        print("   5. Получить список всех вакансий по ключевому слову")
        print("   6. Выйти")

        answer = input()

        if answer in ['1', '2', '3', '4', '5', '6']:
            if answer == '1':
                print("Список всех компаний и количество вакансий в каждой компании:")
                dbm.get_companies_and_vacancies_count()
                continue

            if answer == '2':
                print("Список всех вакансий:")
                dbm.get_all_vacancies()
                continue

            if answer == '3':
                print("Средняя зарплата по вакансиям:")
                dbm.get_avg_salary()
                continue

            if answer == '4':
                print("Список всех вакансий с зарплатой выше средней:")
                dbm.get_vacancies_with_higher_salary()
                continue

            if answer == '5':
                print("Введите ключевое слово:")
                keyword = input()
                print("Список всех вакансий по ключевому слову:")
                dbm.get_vacancies_with_keyword(keyword)
                continue

            if answer == '6':
                break
