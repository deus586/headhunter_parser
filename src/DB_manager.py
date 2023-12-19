import psycopg2
import json
from config import config


class DBManager:
    """
    Класс для получения данных по фильтрам
    """
    def __init__(self, companies, database_name):
        params = config()
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.companies = companies

    def get_companies_and_vacancies_count(self):
        """

        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT COUNT(*), company_name
                            FROM companies
                            INNER JOIN vacancies
                            USING(company_id)
                            GROUP BY company_id""")
                record = cur.fetchall()
                for i in record:
                    print(f"{i[1]}: {i[0]}")

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT company_name, vacancy_name, salary, url
                            FROM companies
                            INNER JOIN vacancies
                            USING(company_id)""")
                record = cur.fetchall()

                for i in record:
                    dict_ = {
                        i[0]: {
                            'vacancy': i[1],
                            'salary': i[2],
                            'url': i[3]
                        }
                    }
                    print(json.dumps(dict_, indent=2, ensure_ascii=False))

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT AVG(salary) FROM vacancies WHERE salary != 0")
                record = cur.fetchall()
                print(f"Средняя зарплата: {round(record[0][0])}")

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"""SELECT company_name, vacancy_name, salary 
                            FROM vacancies 
                            INNER JOIN companies
                            USING(company_id)
                            WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary != 0)""")
                record = cur.fetchall()
                for i in record:
                    print(f"{i[0]}: {i[1]}({i[2]})")

    def get_vacancies_with_keyword(self, keyword):
        """

        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"""SELECT company_name, vacancy_name 
                            FROM vacancies 
                            INNER JOIN companies
                            USING(company_id)
                            WHERE LOWER(vacancy_name) LIKE '%{keyword}%'""")
                record = cur.fetchall()
                for i in record:
                    print(f"{i[0]}: {i[1]}")

    def close_conn(self):
        """
        Закрывает соединение с базой данных
        """
        self.conn.close()
