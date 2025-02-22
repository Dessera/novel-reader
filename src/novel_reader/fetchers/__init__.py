import importlib
import inspect
import os
from typing import Dict, Iterable, Tuple, Type

from .base_fetcher import BaseFetcher


class FetcherFactory:
    def __init__(self):
        self._fetchers: Dict[str, Type[BaseFetcher]] = {}
        for mod in self._list_modules():
            self._fetchers.update(self.get_fetchers_available(mod))

    @staticmethod
    def _list_modules():
        return filter(
            lambda x: x.endswith(".py") and x != "__init__.py",
            (os.listdir(os.path.dirname(__file__))),
        )

    @staticmethod
    def get_fetchers_available(modfile: str) -> Iterable[Tuple[str, Type[BaseFetcher]]]:
        modname = f".{modfile[:-3]}"
        module = importlib.import_module(modname, package=__package__)
        return map(
            lambda obj: (obj[1].IDENTIFIER, obj[1]),
            filter(
                lambda obj: inspect.isclass(obj[1])
                and issubclass(obj[1], BaseFetcher)
                and obj[1] is not BaseFetcher,
                inspect.getmembers(module),
            ),
        )

    def create_fetcher(self, source_type: str, source_params: str):
        fetcher = self._fetchers.get(source_type)
        if fetcher is None:
            raise ValueError(f"Unknown fetcher {source_type}")
        cfg = fetcher.Config.model_validate_json(source_params)
        return fetcher(cfg)

    @property
    def fetchers(self):
        return self._fetchers
