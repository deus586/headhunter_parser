import requests
import json
from parser import Parser


class HeadHunter(Parser):
    """
    Парсер для HeadHunter
    """

    def parser(self, company_name):
        """
        Получение компании и вакансий.
        """
        vacancy_name = []
        salary = []
        description = []
        url = []
        company = []
        area = []
        schedule = []

        for page in range(5):
            params = {
                'search_field': 'company_name',
                'text': company_name,
                'per_page': 50,
                'page': page
            }
            # Посылаем запрос к API
            req = requests.get('https://api.hh.ru/vacancies', params)
            # Декодируем его ответ, чтобы Кириллица отображалась корректно
            data = req.content.decode()
            req.close()

            for i in json.loads(data)['items']:
                try:
                    company.append(i['department']['name'])
                except TypeError:
                    company.append('Компания не указана.')
                schedule.append(i['schedule']['name'])
                area.append(i['area']['name'])
                url.append(i['alternate_url'])
                vacancy_name.append(i['name'])
                if i['snippet']['responsibility'] is not None:
                    description.append(i['snippet']['responsibility'])
                else:
                    description.append('Null')
                if i['salary'] is not None:
                    if i['salary']['from'] is not None:
                        salary.append(i['salary']['from'])
                    else:
                        salary.append(i['salary']['to'])
                else:
                    salary.append(0)
            if json.loads(data)['pages'] - page <= 1:
                break
        data = [{'vacancy name': vacancy_name[j], 'salary': salary[j],
                 'description': description[j], 'url': url[j],
                 'area': area[j], 'company': company[j],
                 'schedule': schedule[j]} for j in range(len(vacancy_name))]
        return data
