from abc import ABCMeta
import importlib
import importlib.util
import inspect
from typing import Dict, List, Optional, Type
from pydantic import BaseModel


class ParamsObject(metaclass=ABCMeta):
    class Config(BaseModel):
        pass

    class Meta:
        identifier = "base"

    def __init__(self, cfg: Config):
        self._cfg = cfg

    # just for convenience
    @property
    def params(self):
        return self._cfg.model_dump()


class _ParamsObjectFactory[T: Type[ParamsObject], IST: ParamsObject](metaclass=ABCMeta):
    def __init__(
        self,
        top_mods: List[str],
        package: Optional[str] = None,
        ptype: T = ParamsObject,
    ):
        self._top_mods = top_mods
        self._ptype = ptype
        self._objs: Dict[str, T] = {}
        for mod in self._top_mods:
            self._objs.update(self._list_modules(mod, package))

    def create(self, identifier: str, params: str) -> IST:
        obj = self.get_object(identifier)
        if obj is None:
            raise ValueError(f"Unknown module identifier: {identifier}")
        cfg = obj.Config.model_validate_json(params)
        return obj(cfg)  # type: ignore

    def _list_modules(self, mod: str, package: Optional[str] = None):
        module = importlib.import_module(mod, package=package)
        return map(
            lambda obj: (obj[1].Meta.identifier, obj[1]),
            filter(
                lambda obj: inspect.isclass(obj[1])
                and issubclass(obj[1], self._ptype)
                and obj[1] is not self._ptype,
                inspect.getmembers(module),
            ),
        )

    def get_object(self, identifier: str):
        return self._objs.get(identifier)


class ParamsObjectFactory[T: ParamsObject](_ParamsObjectFactory[Type[T], T]):
    pass
