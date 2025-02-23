from abc import abstractmethod

from ..utils.params_object import ParamsObject


class BaseTranslator(ParamsObject):
    class Meta(ParamsObject.Meta):
        name = "translator"

    @abstractmethod
    def translate(self, text: str) -> str:
        raise NotImplementedError
