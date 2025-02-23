from dataclasses import dataclass


@dataclass
class NovelDocument:
    title: str
    sections: list[str]


@dataclass
class NovelMeta:
    name: str
    author: str
    link: str


@dataclass
class Novel:
    meta: NovelMeta
    documents: list[NovelDocument]
