from concurrent.futures import ThreadPoolExecutor

from database.dbManger import DBManager
from src.services import utils
from src.model.aeroplane import Aeroplane
from src.services.apiAdapter import APIAdapter
from src.model.jsonSaver import JSONSaver


def fetch_aeroplanes(country: str) -> list[Aeroplane]:
    # Создание экземпляра класса для работы с API сайтов с самолетами
    api = APIAdapter()
    aeroplanes = api.get_aeroplanes(country)
    # Преобразование набора данных в список объектов
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)

    # Сохранение информации в файл
    json_saver = JSONSaver()
    for element in aeroplanes:
        # print(element)
        json_saver.add_aeroplane(element)
    return aeroplanes


# Функция для взаимодействия с пользователем
def user_interaction():
    countries = input("Введите страны через пробел: ").split()

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(fetch_aeroplanes, country) for country in countries]

        top_n = int(input("Введите количество самолетов для вывода в топ N: "))
        filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
        altitude_range = input("Введите диапазон высот полета: ")  # Пример: 100000 - 150000

        aeroplanes = []
        for future in futures:
            aeroplanes.extend(future.result())

    db = DBManager()
    db.init_database(aeroplanes)

    filtered_aeroplanes = utils.filter_aeroplanes(aeroplanes, filter_words)
    ranged_aeroplanes = utils.get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
    sorted_aeroplanes = utils.sort_aeroplanes(ranged_aeroplanes)
    top_aeroplanes = utils.get_top_aeroplanes(sorted_aeroplanes, top_n)
    utils.print_aeroplanes(top_aeroplanes)

    print("\nNext work database\n")

    print(db.get_countries_and_aeroplanes_count())

    print(db.get_avg_speed())

    for plane in db.get_aeroplanes_with_higher_speed():
        print(plane)


if __name__ == "__main__":
    user_interaction()
