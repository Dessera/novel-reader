import json
from dataclasses import dataclass, asdict


@dataclass
class NovelDocument:
    title: str
    sections: list[str]

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass
class NovelMeta:
    name: str
    author: str
    link: str

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass
class Novel:
    meta: NovelMeta
    documents: list[NovelDocument]

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())
