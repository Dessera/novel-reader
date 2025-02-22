import importlib
import inspect
import os
from typing import Dict, Iterable, Tuple, Type

from .base_translator import BaseTranslator


class TranslatorFactory:
    def __init__(self):
        self._trans: Dict[str, Type[BaseTranslator]] = {}
        for mod in self._list_modules():
            self._trans.update(self.get_translator_available(mod))

    @staticmethod
    def _list_modules():
        return filter(
            lambda x: x.endswith(".py") and x != "__init__.py",
            (os.listdir(os.path.dirname(__file__))),
        )

    @staticmethod
    def get_translator_available(
        modfile: str,
    ) -> Iterable[Tuple[str, Type[BaseTranslator]]]:
        modname = f".{modfile[:-3]}"
        module = importlib.import_module(modname, package=__package__)
        return map(
            lambda obj: (obj[1].IDENTIFIER, obj[1]),
            filter(
                lambda obj: inspect.isclass(obj[1])
                and issubclass(obj[1], BaseTranslator)
                and obj[1] is not BaseTranslator,
                inspect.getmembers(module),
            ),
        )

    def create_translator(self, translator_type: str, translator_params: str):
        trans = self._trans.get(translator_type)
        if trans is None:
            raise ValueError(f"Unknown translator {translator_type}")
        cfg = trans.Config.model_validate_json(translator_params)
        return trans(cfg)

    @property
    def translators(self):
        return self._trans.values()
