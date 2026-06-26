import json
import pathlib
from pathlib import Path

from src.model.aeroplane import Aeroplane


class JSONSaver:
    file_name: pathlib.Path

    def __init__(self, file_name: str = "airplanes.json"):
        path_data = Path.cwd() / "data"
        self.file_name = path_data / file_name
        try:
            with open(self.file_name, "x", encoding="utf-8") as f:
                f.write("{}")
        except FileExistsError:
            pass

    def add_aeroplane(self, vacancy:Aeroplane):
        with open(self.file_name, "r", encoding='utf-8') as file:
            aeroplanes = json.load(file)

        aeroplanes.update(vacancy.to_dict())

        with open(self.file_name, "w", encoding='utf-8') as file:
            file.write(json.dumps(aeroplanes, indent=4, ensure_ascii=False))

    def delete_aeroplane(self, vacancy) -> bool:
        with open(self.file_name, "r", encoding='utf-8') as file:
            aeroplanes = json.load(file)

        try:
            aeroplanes.pop(vacancy.icao24)
        except KeyError:
            return False

        with open(self.file_name, "w", encoding='utf-8') as file:
            file.write(json.dumps(aeroplanes, indent=4, ensure_ascii=False))
        return True

    def load(self) -> list[Aeroplane]:
        aeroplanes = []
        with open(self.file_name, "r", encoding='utf-8') as file:
            aeroplanes_json = json.load(file)
        for key, value in aeroplanes_json.items():
            aeroplanes.append(
                Aeroplane(
                    key,
                    value["callsign"],
                    value["country"],
                    value["velocity"],
                    value["geo_altitude"],
                )
            )
        return aeroplanes
