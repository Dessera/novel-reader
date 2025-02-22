from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseTranslator(ABC):
    IDENTIFIER = "base"

    class Config(BaseModel):
        pass

    def __init__(self, cfg: Config):
        self._cfg = cfg

    @abstractmethod
    def translate(self, text: str) -> str:
        raise NotImplementedError

    @property
    def params_info(self):
        return self.Config.model_fields

    @property
    def params(self):
        return self._cfg
