import psycopg2


def create_database(database_name: str, params: dict) -> None:
    try:
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            exist = cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public'"
                               " AND tablename  = 'companies');")
            exist_companies = cur.fetchone()[0]
            if not exist_companies:
                cur.execute(f"CREATE TABLE companies (company_id SERIAL PRIMARY KEY,"
                            f" company_name varchar(100))")

            exist = cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public'"
                               " AND tablename  = 'vacancies');")
            exist_vacancies = cur.fetchone()[0]
            if not exist_vacancies:
                cur.execute(f"CREATE TABLE vacancies (company_id INT REFERENCES companies(company_id),"
                            f" vacancy_name varchar(100), salary int,"
                            f" description varchar, url varchar(100), area varchar(100),"
                            f" schedule varchar(100))")
        conn.close()

    except psycopg2.OperationalError:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()
        create_database(database_name, params)


def save_data_to_database(data, database_name, params) -> None:
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    company_name = data[0]['company']
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO companies(company_name) VALUES ('{company_name}') RETURNING company_id")

        company_id = cur.fetchone()[0]
        for vacancies in data:
            vacancy_name = vacancies['vacancy name']
            salary = vacancies['salary']
            description = vacancies['description']
            url = vacancies['url']
            area = vacancies['area']
            schedule = vacancies['schedule']
            cur.execute(
                """INSERT INTO vacancies
                VALUES (%s, %s, %s,%s, %s, %s, %s)""",
                (company_id, vacancy_name, salary, description, url, area, schedule)
            )

    conn.close()
