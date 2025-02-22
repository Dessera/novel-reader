from dataclasses import dataclass


@dataclass
class NovelDocument:
    title: str
    sections: list[str]
