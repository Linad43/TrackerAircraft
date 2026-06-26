from concurrent.futures import ThreadPoolExecutor

from src.services import utils
from src.model.aeroplane import Aeroplane
from src.services.apiAdapter import APIAdapter
from src.model.jsonSaver import JSONSaver

# Создание экземпляра класса для работы с API сайтов с самолетами
# api = APIAdapter()

# Получение информации о самолетах с opensky-network.org
# aeroplanes = api.get_aeroplanes('Spain')
# print(json.dumps(aeroplanes, indent=4, ensure_ascii=False))
# Преобразование набора данных в список объектов
# aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)
# print(json.dumps([el.to_dict() for el in aeroplanes], indent=4, ensure_ascii=False))
# Пример работы конструктора класса с одним самолетом
# aeroplane = Aeroplane("098765", "UAL1621", "United States", 268.79, 10203.18)
# print(json.dumps(aeroplane.to_dict(), indent=4, ensure_ascii=False))
# Сохранение информации в файл
# json_saver = JSONSaver()

# vacancy = Aeroplane("098765","DRAGO66 ","France",67.42,518.16)
# for element in aeroplanes:
#     json_saver.add_aeroplane(element)
# json_saver.add_aeroplane(vacancy)
# json_saver.delete_aeroplane(vacancy)

def fetch_aeroplanes(country: str) -> list[Aeroplane]:
    # Создание экземпляра класса для работы с API сайтов с самолетами
    api = APIAdapter()
    aeroplanes = api.get_aeroplanes(country)
    # Преобразование набора данных в список объектов
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)

    # Сохранение информации в файл
    json_saver = JSONSaver()
    for element in aeroplanes:
        json_saver.add_aeroplane(element)
    return aeroplanes

# Функция для взаимодействия с пользователем
def user_interaction():
    country = input("Введите название страны: ")

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(fetch_aeroplanes, country)

        top_n = int(input("Введите количество самолетов для вывода в топ N: "))
        filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
        altitude_range = input("Введите диапазон высот полета: ") # Пример: 100000 - 150000

        aeroplanes = future.result()

    filtered_aeroplanes = utils.filter_aeroplanes(aeroplanes, filter_words)
    ranged_aeroplanes = utils.get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
    sorted_aeroplanes = utils.sort_aeroplanes(ranged_aeroplanes)
    top_aeroplanes = utils.get_top_aeroplanes(sorted_aeroplanes, top_n)
    utils.print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()