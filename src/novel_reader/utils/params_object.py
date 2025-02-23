from abc import ABCMeta
import importlib
import importlib.util
import inspect
from typing import Dict, List, Optional, Tuple, Type
from pydantic import BaseModel

from ..exceptions import ModuleSearchException, ObjectCreationException


class ParamsObject(metaclass=ABCMeta):
    class Config(BaseModel):
        pass

    class Meta:
        name = "object"
        identifier = "base"
        description = ""

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

    def create_or_none(self, identifier: str, params: str) -> Optional[IST]:
        obj = self.get_object(identifier)
        if obj is None:
            return None
        cfg = obj.Config.model_validate_json(params)
        return obj(cfg)  # type: ignore

    def create(self, identifier: str, params: str) -> IST:
        obj = self.create_or_none(identifier, params)
        if obj is None:
            raise ObjectCreationException(
                self._ptype.Meta.name, identifier, "No such object"
            )
        return obj

    def _list_modules(
        self, mod: str, package: Optional[str] = None
    ) -> List[Tuple[str, T]]:
        try:
            module = importlib.import_module(mod, package=package)
            return list(
                map(
                    lambda obj: (obj[1].Meta.identifier, obj[1]),
                    inspect.getmembers(
                        module,
                        lambda obj: inspect.isclass(obj)
                        and issubclass(obj, self._ptype)
                        and obj is not self._ptype,
                    ),
                )
            )
        except Exception as e:
            raise ModuleSearchException(mod, package, str(e))

    def get_object(self, identifier: str):
        return self._objs.get(identifier)


class ParamsObjectFactory[T: ParamsObject](_ParamsObjectFactory[Type[T], T]):
    pass
