import psycopg2
import os
import json


class DBManager:
    """
    Класс для получения данных по фильтрам
    """
    def __init__(self, companies):
        self.conn = psycopg2.connect(
            host='localhost',
            database='headhunter_parser',
            user='postgres',
            password=os.getenv('PASSWORD')
        )
        self.companies = companies

    def get_companies_and_vacancies_count(self):
        """

        Получает список всех компаний и количество вакансий у каждой компании.
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    for i in self.companies:
                        cur.execute(f"SELECT COUNT(*) FROM {i}")
                        record = cur.fetchall()
                        if len(record) == 0:
                            continue
                        print(f"{i}: {record[0][0]}")

        finally:
            self.conn.close()

    def get_all_vacancies(self):
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    for i in self.companies:
                        cur.execute(f"SELECT vacancy, salary, url FROM {i}")
                        record = cur.fetchall()
                        if len(record) == 0:
                            continue
                        for j in record:
                            dict_ = {
                                i: {
                                    'vacancy': j[0],
                                    'salary': j[1],
                                    'url': j[2]
                                }
                            }
                            print(json.dumps(dict_, indent=2, ensure_ascii=False))
        finally:
            self.conn.close()

    def get_avg_salary(self):
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    for i in self.companies:
                        cur.execute(f"SELECT AVG(salary) FROM {i} WHERE salary != 0")
                        record = cur.fetchall()
                        if len(record) == 0:
                            continue
                        print(f"{i}: {round(record[0][0])}")

        finally:
            self.conn.close()

    def get_vacancies_with_higher_salary(self):
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    for i in self.companies:
                        cur.execute(f"SELECT vacancy, salary FROM {i} WHERE salary > (SELECT AVG(salary) FROM {i} WHERE salary != 0)")
                        record = cur.fetchall()
                        if len(record) == 0:
                            continue
                        for j in record:
                            print(f"{i}: {j[0]}({j[1]})")

        finally:
            self.conn.close()

    def get_vacancies_with_keyword(self, keyword):
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    for i in self.companies:
                        cur.execute(f"SELECT vacancy FROM {i} WHERE LOWER(vacancy) LIKE '%{keyword}%'")
                        record = cur.fetchall()
                        if len(record) == 0:
                            continue
                        for j in record:
                            print(f"{i}: {j[0]}")

        finally:
            self.conn.close()
