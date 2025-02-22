from abc import ABCMeta
from pydantic import BaseModel


class ParamsObject(metaclass=ABCMeta):
    IDENTIFIER = "base"

    class Config(BaseModel):
        pass

    def __init__(self, cfg: Config):
        self._cfg = cfg

    # just for convenience
    @property
    def params(self):
        return self._cfg.model_dump()
