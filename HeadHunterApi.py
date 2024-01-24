import requests

class HHJobSearchAPI():
    """
    Класс для взаимодействия с API HeadHunter для поиска данных о компаниях и вакансиях.

    Атрибуты:
    - companies (list): Список идентификаторов компаний, для которых будут извлекаться данные.
    """

    companies = [1740, 27879, 1122462, 52951, 15848, 78638, 44281, 1417, 1520838, 3529]

    def get_all_company_data(self):
        """
        Получает данные о каждой компании из списка companies, используя API HeadHunter.

        Возвращает:
        - result_data (list): Список с данными о каждой компании в формате JSON.
        """
        result_data = []
        params = {}

        for employer_id in self.companies:
            data = requests.get(f'https://api.hh.ru/employers/{employer_id}', params=params).json()
            result_data.append(data)

        return result_data


    def get_all_vacancies_from_companies(self):
        """
        Получает все вакансии для каждой компании из списка companies, используя API HeadHunter.

        Возвращает:
        - result_data (list): Список с данными о вакансиях для каждой компании в формате JSON.
        """
        result_data = []
        params = {}
        vacancies_url = f'https://api.hh.ru/vacancies'

        for employer_id in self.companies:
            params['employer_id'] = employer_id
            vacancies = requests.get(vacancies_url, params=params).json()
            result_data.append(vacancies)

        return result_data
