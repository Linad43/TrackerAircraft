from abc import ABC, abstractmethod


class AeroplanesAPI(ABC):
    @abstractmethod
    def get_aeroplanes(self, country: str) -> dict:
        pass
