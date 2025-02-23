from abc import abstractmethod
from typing import List
from ..utils.params_object import ParamsObject
from ..novel import NovelDocument, NovelMeta, Novel


class BaseFetcher(ParamsObject):
    class Meta(ParamsObject.Meta):
        name = "fetcher"

    @abstractmethod
    def fetch(self, src: str) -> NovelDocument:
        raise NotImplementedError

    @abstractmethod
    def search(self, src: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def fetch_meta(self, src: str) -> NovelMeta:
        raise NotImplementedError

    @abstractmethod
    def fetch_all(self, src: str) -> Novel:
        raise NotImplementedError
