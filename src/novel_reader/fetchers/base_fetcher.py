from abc import abstractmethod
from ..utils.params_object import ParamsObject
from ..novel import NovelDocument


class BaseFetcher(ParamsObject):
    @abstractmethod
    def fetch(self, _url: str) -> NovelDocument:
        raise NotImplementedError
