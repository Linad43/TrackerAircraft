import json

from src.model.aeroplane import Aeroplane


def filter_aeroplanes(aeroplanes: list[Aeroplane], filter_words: list[str]) -> list[Aeroplane]:
    for index in range(len(filter_words)):
        filter_words[index] = filter_words[index].lower()
    result_aeroplanes = []
    for aeroplane in aeroplanes:
        if aeroplane.country is not None and aeroplane.country.lower() in filter_words:
            result_aeroplanes.append(aeroplane)
    return result_aeroplanes


def get_aeroplanes_by_altitude(aeroplanes: list[Aeroplane], altitude_range: str) -> list[Aeroplane]:
    altitude_range = altitude_range.split()
    correct_altitude_range: list[float] = []
    for altitude in altitude_range:
        try:
            float(altitude)
            correct_altitude_range.append(float(altitude))
        except ValueError:
            pass
    if len(correct_altitude_range) != 2:
        raise ValueError("Некорректный ввод диапазона высот")
    max_range: float = max(correct_altitude_range)
    min_range: float = min(correct_altitude_range)
    result_aeroplanes = []
    for aeroplane in aeroplanes:
        if aeroplane.geo_altitude is not None and min_range < aeroplane.geo_altitude < max_range:
            result_aeroplanes.append(aeroplane)
    return result_aeroplanes


def sort_aeroplanes(ranged_aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    return sorted(
        ranged_aeroplanes,
        key=lambda aeroplane: aeroplane.country.lower()
    )  # Не знаю по какому критерию делать сортировку


def get_top_aeroplanes(sorted_aeroplanes, top_n):
    result_aeroplanes = []
    for index in range(top_n):
        try:
            result_aeroplanes.append(sorted_aeroplanes[index])
        except IndexError:
            return result_aeroplanes
    return result_aeroplanes


def print_aeroplanes(top_aeroplanes: list[Aeroplane]):
    for index in range(len(top_aeroplanes)):
        print(f'{index + 1}. {json.dumps(top_aeroplanes[index].to_dict(), indent=4, ensure_ascii=False)}')
