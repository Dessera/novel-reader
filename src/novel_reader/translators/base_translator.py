from abc import abstractmethod

from ..utils.params_object import ParamsObject


class BaseTranslator(ParamsObject):
    @abstractmethod
    def translate(self, text: str) -> str:
        raise NotImplementedError
