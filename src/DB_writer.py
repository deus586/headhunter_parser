import psycopg2
from HH_parser import HeadHunter
import os


class DBWriter:

    def __init__(self):
        self.hh = HeadHunter()
        self.conn = psycopg2.connect(
            host='localhost',
            database='headhunter_parser',
            user='postgres',
            password=os.getenv('PASSWORD')
        )

    def writer(self, company_name):

        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    # Запускаем скрипты создания таблиц
                    vacancy_name, salary, description, url, area, company, schedule = self.hh.parser(company_name)
                    cur.execute(f"CREATE TABLE {company_name} (vacancy varchar(100), salary int,"
                                f" description varchar, url varchar(100), area varchar(100),"
                                f" schedule varchar(100))")

                    for i in range(len(vacancy_name)):
                        cur.execute(f"INSERT INTO {company_name} VALUES(%s, %s, %s, %s, %s, %s)",
                                    (vacancy_name[i], salary[i], description[i], url[i], area[i], schedule[i]))
        finally:
            self.conn.close()
