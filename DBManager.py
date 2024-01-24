from HeadHunterApi import HHJobSearchAPI
from dateutil import parser
import psycopg2
from implemented import dbname, user, password, host, port

class DBManager:
    """
    Класс для управления базой данных и взаимодействия с API HeadHunter для загрузки данных о компаниях и вакансиях.

    Атрибуты:
    - conn: Объект соединения с базой данных.
    - cur: Объект курсора для выполнения SQL-запросов.
    """

    def __init__(self):
        """
        Инициализация объекта DBManager, устанавливает соединение с базой данных.
        """
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def create_tables(self):
        """
        Создает таблицы в базе данных.
        """
        self.cur.execute("""
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                industry VARCHAR(255),
                location VARCHAR(100),
                website_url VARCHAR(255)
            )
        """)

        self.cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(company_id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                location VARCHAR(100),
                salary_rub DECIMAL(10, 2),
                posted_date DATE,
                vacancy_url VARCHAR(50),
                CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def insert_data(self):
        """
        Извлекает данные о компаниях и вакансиях с использованием API HeadHunter и вставляет их в базу данных.
        """
        try:
            hh_api = HHJobSearchAPI()

            # Извлечение данных о компаниях
            companies = hh_api.get_all_company_data()
            for company in companies:
                site = company['site_url'] if company['site_url'] else company['alternate_url']
                industry = company['industries'][0]['name'] if company['industries'] else None

                self.cur.execute(
                    "INSERT INTO companies (company_id, name, industry, location, website_url) VALUES (%s, %s, %s, %s, %s)",
                    (company['id'],
                     company.get('name', 'None')[:255],
                     industry[:255],
                     company['area']['name'][:100],
                     site)
                )

            # Извлечение данных о вакансиях
            vacancies = hh_api.get_all_vacancies_from_companies()
            for i in range(len(vacancies)):
                for vacancy in vacancies[i]['items']:
                    active_salary = 0
                    salary_in_rubles = None
                    date = parser.parse(vacancy['published_at']).strftime("%Y-%m-%d %H:%M:%S")

                    # Поиск зарплаты
                    if vacancy['salary'] is not None:
                        if vacancy['salary']['to'] is not None:
                            active_salary = vacancy['salary']['to']
                        elif vacancy['salary']['from'] is not None:
                            active_salary = vacancy['salary']['from']

                        # Конвертация зарплаты в рубли, если в другой валюте
                        if vacancy['salary']['currency'] in ['AZN', 'BYR', 'EUR', 'GEL', 'KGS', 'KZT', 'USD', 'UAH',
                                                             'UZS']:
                            salary_value: float = active_salary
                            salary_in_rubles: int = self._convert_to_rubles(salary_value, vacancy['salary']['currency'])
                        else:
                            salary_in_rubles = active_salary

                    self.cur.execute(
                        "INSERT INTO vacancies (vacancy_id, company_id, title, description, location, salary_rub, posted_date, vacancy_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (vacancy['id'],
                         vacancy['employer']['id'],
                         vacancy['name'][:255],
                         vacancy['snippet']['requirement'],
                         vacancy['area']['name'],
                         salary_in_rubles,
                         date,
                         vacancy['alternate_url']
                         ))

            self.conn.commit()

        except Exception as e:
            sql_query = f"DROP TABLE IF EXISTS vacancies; DROP TABLE IF EXISTS companies;"
            self.cur.execute(sql_query)
            self.conn.commit()
            print(e)

    def drop_tables(self):
        """
        Удаляет таблицы из базы данных.
        """
        sql_query = f"DROP TABLE IF EXISTS vacancies; DROP TABLE IF EXISTS companies;"
        self.cur.execute(sql_query)
        self.conn.commit()

    def _convert_to_rubles(self, amount: float, currency: str):
        """
        Конвертирует сумму из заданной валюты в рубли.

        Аргументы:
        - amount (float): Сумма в заданной валюте.
        - currency (str): Код валюты.

        Возвращает:
        - rubles (int): Сумма в рублях.
        """
        exchange_rates = {
            'AZN': 52.25,
            'BYR': 26.98,
            'EUR': 97.16,
            'GEL': 32.84,
            'KGS': 0.99,
            'KZT': 0.19,
            'USD': 88.8,
            'UZS': 0.0072,
            'UAH': 2.44
        }

        if currency in exchange_rates:
            rate: float = exchange_rates[currency]
            rubles: int = amount * rate

            return int(rubles)
        else:
            return None

    def get_companies_and_vacancies_count(self):
        """
        Получает количество вакансий для каждой компании.
        """
        self.cur.execute("""
        SELECT companies.company_id, companies.name, COUNT(vacancies.vacancy_id) 
        FROM companies 
        LEFT JOIN vacancies ON companies.company_id = vacancies.company_id 
        GROUP BY companies.company_id, companies.name;
        """)
        response =  self.cur.fetchall()
        for row in response:
            print(row)

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с дополнительной информацией о компании.
        """
        self.cur.execute("""
        SELECT vacancies.vacancy_id, vacancies.title, companies.name, companies.industry, vacancies.vacancy_url 
        FROM vacancies
        LEFT JOIN companies ON vacancies.company_id = companies.company_id
        """)
        response =  self.cur.fetchall()
        for row in response:
            print(row)

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по всем вакансиям с указанной зарплатой.
        """
        self.cur.execute("""
            SELECT AVG(salary_rub) AS average_salary
            FROM vacancies
            WHERE salary_rub IS NOT NULL
        """)
        response = self.cur.fetchone()

        if response[0] is not None:
            average_salary = round(response[0], 2)
            print(f"{average_salary} RUB")
        else:
            print("Нет данных о зарплате")


    def get_vacancies_with_higher_salary(self):
        """
        Получает вакансии с зарплатой выше средней.
        """
        self.cur.execute("""
            SELECT AVG(salary_rub) AS average_salary
            FROM vacancies
            WHERE salary_rub IS NOT NULL
        """)
        average_salary_response = self.cur.fetchone()

        if average_salary_response[0] is not None:
            average_salary = round(average_salary_response[0], 2)

            self.cur.execute("""
                SELECT v.vacancy_id, v.title, c.name AS company_name, c.industry, v.salary_rub, v.vacancy_url
                FROM vacancies v
                LEFT JOIN companies c ON v.company_id = c.company_id
                WHERE v.salary_rub > %s
            """, (average_salary,))

            vacancies_response = self.cur.fetchall()

            if vacancies_response:
                for row in vacancies_response:
                    print(row)
            else:
                print("Нет вакансий с зарплатой выше средней")
        else:
            print("Данных о зарплате нет.")

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает вакансии с заданным ключевым словом в заголовке.

        Аргументы:
        - keyword (str): Ключевое слово для поиска в заголовках вакансий.
        """
        try:
            self.cur.execute("""
                SELECT v.vacancy_id, v.title, c.name AS company_name, c.industry, v.salary_rub, v.vacancy_url
                FROM vacancies v
                LEFT JOIN companies c ON v.company_id = c.company_id
                WHERE LOWER(v.title) LIKE %s
            """, ('%' + keyword.lower() + '%',))

            vacancies_response = self.cur.fetchall()

            if vacancies_response:
                for row in vacancies_response:
                    print(row)
            else:
                print(f"По ключевому слову вакансий не найдено '{keyword}' в заголовке.")

        except Exception as e:
            print(f"Error: {e}")
