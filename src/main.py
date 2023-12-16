from DB_writer import DBWriter
from DB_manager import DBManager


if __name__ == '__main__':
    # Вводим названия компаний
    companies = input("Введите названия компаний через пробел: ").split()
    for comp in companies:
        # Парсим и записываем в базу данных
        hh = DBWriter()
        hh.writer(comp)

    user_action = input("База данных создана! Хотите ли вы вывести данные на экран?(Y/N)\n")
    while True:
        manager = DBManager(companies)
        if user_action.lower() == 'n':
            manager.close_conn()
            break
        elif user_action.lower() != 'y' and user_action != '':
            print("Нет такого варианта.")
            user_action = input('Хотите продолжить?\n')
            continue
        # Используем класс DBManager для получения данных
        try:
            users_choose = int(input('Введите число от 1 до 5 где:\n'
                                     '1. Получение всех компаний и количество их вакансий.\n'
                                     '2. Все вакансии с указанием компании, зарплаты и ссылки.\n'
                                     '3. Средняя зарплата по вакансиям компаний.\n'
                                     '4. Все вакансии зарплата которых выше средней по вакансиям.\n'
                                     '5. Вакансии по ключевому слову.\n'))
        except ValueError:
            print("Нет такого варианта.")
            user_action = input('Хотите продолжить?\n')
            continue

        match users_choose:
            case 1:
                manager.get_companies_and_vacancies_count()
            case 2:
                manager.get_all_vacancies()
            case 3:
                manager.get_avg_salary()
            case 4:
                manager.get_vacancies_with_higher_salary()
            case 5:
                keyword = input('Введите ключевое слово: ').lower()
                manager.get_vacancies_with_keyword(keyword)
            case _:
                print("Нет такого варианта.")
        user_action = input('Хотите продолжить?\n')
