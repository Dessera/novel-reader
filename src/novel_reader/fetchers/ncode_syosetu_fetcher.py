import re
import urllib.parse as URL
from typing import Annotated, List, Optional
from bs4 import BeautifulSoup
from pydantic import Field

from .http_fetcher import HttpFetcher

from ..novel import NovelDocument, NovelMeta


class NcodeSyosetuFetcher(HttpFetcher):
    class Meta(HttpFetcher.Meta):
        identifier = "ncode_syosetu"
        description = "Fetcher for ncode.syosetu.com"

    class Config(HttpFetcher.Config):
        base_url: Annotated[str, Field(description="Base URL of the website")] = (
            "https://ncode.syosetu.com"
        )
        max_pages: Annotated[
            int, Field(description="Max number of pages to search")
        ] = 100

    def fetch(self, src: str):
        url = self._build_page_url(src)
        content = "".join(super().fetch(url).sections)
        soup = BeautifulSoup(content, "html.parser")

        title_container = soup.select_one(".p-novel__title")
        title = title_container.get_text() if title_container is not None else ""

        sections = [
            item.get_text() for item in soup.find_all("p", id=re.compile(r"L\d+"))
        ]

        return NovelDocument(title=title, sections=sections)

    def search(self, src: str) -> List[str]:
        page = 1
        max_pages: int = self.params.get("max_pages", 100)
        final_entries: List[str] = []
        while page <= max_pages:
            entries = list(self._search_one_page(src, page))
            if len(entries) == 0:
                break

            final_entries.extend(entries)
            page += 1

        return final_entries

    def fetch_meta(self, src: str) -> NovelMeta:
        url = self._build_page_url(src)
        content = "".join(super().fetch(url).sections)
        soup = BeautifulSoup(content, "html.parser")

        name_container = soup.select_one(".p-novel__title")
        name = name_container.get_text() if name_container is not None else ""
        author_container = soup.select_one(".p-novel__author >a")
        author = author_container.get_text() if author_container is not None else ""

        return NovelMeta(name=name, author=author, link=url)

    def _build_page_url(self, path: str, page: Optional[int] = None) -> str:
        base: str | None = self.params.get("base_url")
        if base is None:  # never happens
            raise ValueError("base_url is not set")
        query_params = {"p": page} if page is not None else {}
        return self.build_url(base, path, query_params)

    def _search_one_page(self, path: str, page: int):
        url = self._build_page_url(path, page)
        content = "".join(super().fetch(url).sections)
        soup = BeautifulSoup(content, "html.parser")

        entries = soup.find_all("a", class_="p-eplist__subtitle", href=True)

        return map(
            lambda e: URL.urljoin(url, e["href"]),  # type: ignore
            entries,
        )
