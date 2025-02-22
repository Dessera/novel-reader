import re
from bs4 import BeautifulSoup

from .http_fetcher import HttpFetcher

from ..novel import NovelDocument


class NcodeSyosetuFetcher(HttpFetcher):
    IDENTIFIER = "ncode_syosetu"

    def fetch(self, url: str):
        content = "".join(super().fetch(url).sections)
        soup = BeautifulSoup(content, "html.parser")

        title = soup.find(class_="p-novel__title")
        if title is None:
            title = ""
        else:
            title = title.get_text()

        sections = [
            item.get_text() for item in soup.find_all("p", id=re.compile(r"L\d+"))
        ]

        return NovelDocument(title=title, sections=sections)
