import re
import urllib.parse as URL
from typing import List
from bs4 import BeautifulSoup

from .http_fetcher import HttpFetcher

from ..novel import NovelDocument, NovelMeta


class NcodeSyosetuFetcher(HttpFetcher):
    class Meta(HttpFetcher.Meta):
        identifier = "ncode_syosetu"

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

    def search(self, url: str) -> List[str]:
        page = 1
        final_entries: List[str] = []
        while True:
            prepared_url = self._build_page_url(url, page)
            entries = list(self._search_one_page(prepared_url))
            if len(entries) == 0:
                break

            final_entries.extend(entries)
            page += 1

        return final_entries

    def fetch_meta(self, url: str) -> NovelMeta:
        content = "".join(super().fetch(url).sections)
        soup = BeautifulSoup(content, "html.parser")

        name_container = soup.select_one(".p-novel__title")
        name = name_container.get_text() if name_container is not None else ""
        author_container = soup.select_one(".p-novel__author >a")
        author = author_container.get_text() if author_container is not None else ""

        return NovelMeta(name=name, author=author, link=url)

    def _build_page_url(self, url: str, page: int) -> str:
        return self.build_url(url, {"p": page})

    def _search_one_page(self, url: str):
        content = "".join(super().fetch(url).sections)
        soup = BeautifulSoup(content, "html.parser")

        entries = soup.find_all("a", class_="p-eplist__subtitle", href=True)

        return map(
            lambda e: URL.urljoin(url, e["href"]),  # type: ignore
            entries,
        )
