from ..fetchers.base_fetcher import BaseFetcher
from ..translators.base_translator import BaseTranslator
from ..utils.params_object import ParamsObjectFactory


class TranslatorFactory(ParamsObjectFactory[BaseTranslator]):
    def __init__(self):
        super().__init__(["..translators"], __package__, BaseTranslator)


class FetcherFactory(ParamsObjectFactory[BaseFetcher]):
    def __init__(self):
        super().__init__(["..fetchers"], __package__, BaseFetcher)
