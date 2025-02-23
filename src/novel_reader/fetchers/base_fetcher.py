from abc import abstractmethod
from typing import List
from ..utils.params_object import ParamsObject
from ..novel import NovelDocument, NovelMeta, Novel


class BaseFetcher(ParamsObject):
    @abstractmethod
    def fetch(self, _url: str) -> NovelDocument:
        raise NotImplementedError

    @abstractmethod
    def search(self, _url: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def fetch_meta(self, _url: str) -> NovelMeta:
        raise NotImplementedError

    @abstractmethod
    def fetch_all(self, _url: str) -> Novel:
        raise NotImplementedError
