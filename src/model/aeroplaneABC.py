from abc import ABC, abstractmethod


class BaseAeroplane(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    def cast_to_object_list(cls, aeroplanes):
        pass

